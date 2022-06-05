import dataclasses
import re
from typing import List, Iterator, Optional

from packaging.specifiers import SpecifierSet
from packaging.version import Version

from tabulate import tabulate
from colorama import init, Fore


@dataclasses.dataclass
class VersionCheck:
    version: Version
    specifier_set: SpecifierSet
    is_valid: bool

    def print(self, fmt: str) -> str:
        if fmt == 'html':
            return f'<span style="color: {"green" if self.is_valid else "red"}">' \
                   f'{self.version.public}' \
                   f'</span>'
        return f'{Fore.GREEN if self.is_valid else Fore.RED}' \
               f'{self.version.public}' \
               f'{Fore.RESET}'


def _get_num_neighbours(num: int):
    yield num
    if num > 1:
        yield num - 1
    yield num + 1


def _get_phases_of_version(version: str,
                           suffix_nums: List[int]) -> Iterator[Version]:
    yield Version(f'{version}')
    for n in suffix_nums:
        yield Version(f'{version}dev{n}')
        for pre in ('a', 'b', 'rc'):
            yield Version(f'{version}{pre}{n}')
        yield Version(f'{version}post{n}')


def _generate_versions_for_version(
        majors: List[int],
        minors: List[int],
        micros: List[int],
        suffix_num: Optional[int] = None) -> Iterator[Version]:
    if suffix_num:
        suffix_nums = [suffix_num - 1, suffix_num, suffix_num + 1]
        suffix_nums = list(filter(lambda x: x > 0, suffix_nums))
    else:
        suffix_nums = [1]

    for major in majors:
        if major > 0:
            for ver in _get_phases_of_version(str(major), suffix_nums):
                yield ver
        for minor in minors:
            if sum([major, minor]) > 0:
                base_ver = f'{major}.{minor}'
                for ver in _get_phases_of_version(base_ver, suffix_nums):
                    yield ver
            for micro in micros:
                if sum([major, minor, micro]) > 0:
                    base_ver = f'{major}.{minor}.{micro}'
                    for ver in _get_phases_of_version(base_ver, suffix_nums):
                        yield ver


def _generate_versions_for_specifier_set(specifier_set: str) -> List[Version]:
    generated_versions = []
    pattern = r'^([~>=<!]{1,3})(\d+(=?\.(\d+(=?\.(\d+)*)*)*)*)(([a-zA-Z]+)(\d+))?'
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

            generated_versions += list(
                _generate_versions_for_version(majors, minors, micros,
                                               suffix_num))

    return generated_versions


def _check_generated_versions_for_specifier_set(
        specifier_set: str) -> Iterator[VersionCheck]:
    versions = _generate_versions_for_specifier_set(specifier_set)
    specifier_set = SpecifierSet(specifiers=specifier_set)
    for version in versions:
        is_valid = version.public in specifier_set
        yield VersionCheck(version=version,
                           specifier_set=specifier_set,
                           is_valid=is_valid)


def print_similar_versions(specifier_set: str, fmt: str = 'github') -> str:
    init()

    version_checks = _check_generated_versions_for_specifier_set(specifier_set)
    base_versions = {}
    index = set()
    for version_check in version_checks:
        if version_check.version.public in index:
            continue
        else:
            index.add(version_check.version.public)

        base_version = version_check.version.base_version
        if base_version not in base_versions.keys():
            base_versions[base_version] = dict(dev=[],
                                               pre=[],
                                               final=[],
                                               post=[])
        if version_check.version.is_devrelease:
            base_versions[base_version]['dev'].append(version_check)
        elif version_check.version.is_prerelease:
            base_versions[base_version]['pre'].append(version_check)
        elif version_check.version.is_postrelease:
            base_versions[base_version]['post'].append(version_check)
        else:
            base_versions[base_version]['final'].append(version_check)

    base_versions = dict(sorted(base_versions.items()))

    rows = []
    for base_version in base_versions.values():
        # Sort versions:
        for phase, versions in base_version.items():
            base_version[phase] = sorted(versions,
                                         key=lambda x: x.version.public)
        # Colorize versions:
        rows.append([
            ' - '.join([
                version_check.print(fmt=fmt) for version_check in base_version
            ]) for base_version in base_version.values()
        ])

    tablefmt = 'unsafehtml' if fmt == 'html' else fmt
    output = tabulate(rows,
                      headers=('dev', 'pre', 'final', 'post'),
                      tablefmt=tablefmt)
    print(output)
    return output


def check(version: str, specifier_set: str):
    specifier_set = SpecifierSet(specifier_set)
    return version in specifier_set


def main():
    print_similar_versions('>=0.1b2,<=0.2')


if __name__ == '__main__':
    main()

__version__ = '0.1.0'
