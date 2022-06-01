import dataclasses
import enum
import re
from typing import List, Iterator, Dict

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


def _create_checks_for_version(majors: List[int], minors: List[int], micros: List[int]) -> Iterator[Release]:
    pres = ('a', 'b', 'r', 'rc')
    for major in majors:
        if major > 0:
            yield Release(version=str(major), phase=ReleasePhase.FINAL)
            for n in range(1, 3):
                yield Release(version=f'{major}dev{n}', phase=ReleasePhase.DEV)
                for pre in pres:
                    yield Release(version=f'{major}{pre}{n}', phase=ReleasePhase.PRE)
                yield Release(version=f'{major}post{n}', phase=ReleasePhase.POST)
        for minor in minors:
            if sum([major, minor]) > 0:
                yield Release(version=f'{major}.{minor}', phase=ReleasePhase.FINAL)
                for n in range(1, 3):
                    yield Release(version=f'{major}.{minor}dev{n}', phase=ReleasePhase.DEV)
                    for pre in pres:
                        yield Release(version=f'{major}.{minor}{pre}{n}', phase=ReleasePhase.PRE)
                    yield Release(version=f'{major}.{minor}post{n}', phase=ReleasePhase.POST)
            for micro in micros:
                if sum([major, minor, micro]) > 0:
                    yield Release(version=f'{major}.{minor}.{micro}', phase=ReleasePhase.FINAL)
                    for n in range(1, 3):
                        yield Release(version=f'{major}.{minor}.{micro}dev{n}', phase=ReleasePhase.DEV)
                        for pre in pres:
                            yield Release(version=f'{major}.{minor}.{micro}{pre}{n}', phase=ReleasePhase.PRE)
                        yield Release(version=f'{major}.{minor}.{micro}post{n}', phase=ReleasePhase.POST)


def _create_checks_for_specifier(specifier_set: str) -> List[Release]:
    releases = []
    pattern = r'^([~>=<!]+)(\d+(=?\.(\d+(=?\.(\d+)*)*)*)*)'
    for specifier in specifier_set.split(','):
        match = re.search(pattern, specifier)
        if match:
            parts = Version(match.group(2).strip('.')).base_version.split('.')
            parts = list(filter(lambda x: str.isnumeric(x), parts))
            parts = list(map(int, parts))
            parts += (3 - len(parts)) * [0]
            major, minor, micro = parts

            majors = list(_get_num_neighbours(major))
            minors = list(_get_num_neighbours(minor))
            micros = list(_get_num_neighbours(micro))

            releases += list(_create_checks_for_version(majors, minors, micros))

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
    output = check('==0.2.*')
    for group, releases in output.items():
        print(f'{group}')
        for release, valid in filter(lambda x: x[1], releases.items()):
            print(f'{release} : {valid}')


if __name__ == '__main__':
    main()


__version__ = '0.1.0'
