import re
from typing import List, Iterator, Dict

from packaging.specifiers import SpecifierSet
from packaging.version import Version


def _get_num_neighbours(num: int):
    yield num
    if num > 1:
        yield num - 1
    yield num + 1


def _create_checks_for_version(major: int, minor: int, micro: int) -> Iterator[str]:
    majors = list(_get_num_neighbours(major))
    minors = list(_get_num_neighbours(minor))
    micros = list(_get_num_neighbours(micro))
    for major in majors:
        if major > 0:
            yield str(major)
        for minor in minors:
            if sum([major, minor]) > 0:
                yield f'{major}.{minor}'
            for micro in micros:
                if sum([major, minor, micro]) > 0:
                    yield f'{major}.{minor}.{micro}'


def _create_checks_for_specifier(specifier_set: str) -> List[str]:
    versions = []
    pattern = r'^([~>=<!]+)(\d+(=?\.(\d+(=?\.(\d+)*)*)*)*)'
    for specifier in specifier_set.split(','):
        match = re.search(pattern, specifier)
        if match:
            parts = Version(match.group(2).strip('.')).base_version.split('.')
            parts = list(filter(lambda x: str.isnumeric(x), parts))
            parts = list(map(int, parts))
            parts += (3 - len(parts)) * [0]
            versions += list(_create_checks_for_version(*parts))
    return list(sorted(set(versions)))


def check(specifier: str) -> Dict[str, bool]:
    checks = _create_checks_for_specifier(specifier)
    specifier = SpecifierSet(specifier)
    return {check_: check_ in specifier for check_ in checks}


def main():
    versions = check('>=0.2,<0.3a')
    for version, in_range in versions.items():
        print(f'{version} : {in_range}')


if __name__ == '__main__':
    main()


__version__ = '0.1.0'
