import dataclasses
import enum
import re
from typing import List, Iterator, Dict, Optional

from packaging.specifiers import SpecifierSet
from packaging.version import Version


class ReleasePhase(enum.Enum):
    PRE = 'pre'
    DEV = 'dev'
    FINAL = 'final'
    POST = 'post'

    def __str__(self):
        return str(self.value).lower()


@dataclasses.dataclass
class Release:
    version: str
    phase: ReleasePhase


r = Release(version='1', phase=ReleasePhase.DEV)


def _get_num_neighbours(num: int):
    yield num
    if num > 1:
        yield num - 1
    yield num + 1


def _get_phases_of_version(version: str, suffix_nums: List[int]) -> Iterator[Release]:
    yield Release(version=str(version), phase=ReleasePhase.FINAL)
    for n in suffix_nums:
        yield Release(version=f'{version}dev{n}', phase=ReleasePhase.DEV)
        for pre in ('a', 'b', 'rc'):
            yield Release(version=f'{version}{pre}{n}', phase=ReleasePhase.PRE)
        yield Release(version=f'{version}post{n}', phase=ReleasePhase.POST)


def _create_checks_for_version(majors: List[int], minors: List[int], micros: List[int], suffix_num: Optional[int] = None) -> Iterator[Release]:
    if suffix_num:
        suffix_nums = [suffix_num - 1, suffix_num, suffix_num + 1]
        suffix_nums = list(filter(lambda x: x > 0, suffix_nums))
    else:
        suffix_nums = [1]

    for major in majors:
        if major > 0:
            for version in _get_phases_of_version(str(major), suffix_nums):
                yield version
        for minor in minors:
            if sum([major, minor]) > 0:
                for version in _get_phases_of_version(f'{major}.{minor}', suffix_nums):
                    yield version
            for micro in micros:
                if sum([major, minor, micro]) > 0:
                    for version in _get_phases_of_version(f'{major}.{minor}.{micro}', suffix_nums):
                        yield version


def _create_checks_for_specifier(specifier_set: str) -> List[Release]:
    releases = []
    pattern = r'^([~>=<!]{2,3})(\d+(=?\.(\d+(=?\.(\d+)*)*)*)*)(([a-zA-Z]+)(\d+))?'
    for specifier in specifier_set.split(','):
        match = re.search(pattern, specifier)
        if match:
            version_str = match.group(2).strip('.')
            versions = Version(version_str).base_version.split('.')
            # suffix_word = match.group(8)
            suffix_num = match.group(9)
            if suffix_num:
                suffix_num = int(suffix_num)

            versions = list(filter(lambda x: str.isnumeric(x), versions))
            versions = list(map(int, versions))
            versions += (3 - len(versions)) * [0]
            major, minor, micro = versions

            majors = list(_get_num_neighbours(major))
            minors = list(_get_num_neighbours(minor))
            micros = list(_get_num_neighbours(micro))

            releases += list(_create_checks_for_version(majors, minors, micros, suffix_num))

    return releases


def check(specifier: str) -> Dict[str, Dict[str, bool]]:
    checks = _create_checks_for_specifier(specifier)
    specifier = SpecifierSet(specifier)
    groups = {
        str(ReleasePhase.DEV): {r.version: r.version in specifier for r in filter(lambda r: r.phase == ReleasePhase.DEV, checks)},
        str(ReleasePhase.PRE): {r.version: r.version in specifier for r in filter(lambda r: r.phase == ReleasePhase.PRE, checks)},
        str(ReleasePhase.FINAL): {r.version: r.version in specifier for r in filter(lambda r: r.phase == ReleasePhase.FINAL, checks)},
        str(ReleasePhase.POST): {r.version: r.version in specifier for r in filter(lambda r: r.phase == ReleasePhase.POST, checks)},
    }
    return groups


def main():
    output = check('>=0.2a2')
    for group, releases in output.items():
        print(f'{group}')
        for release, valid in filter(lambda x: x[1], releases.items()):
            print(f'{release} : {valid}')


if __name__ == '__main__':
    main()


__version__ = '0.1.0'
