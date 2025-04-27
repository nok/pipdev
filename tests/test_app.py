import pytest

from pip_dev.app import check_version, generate_versions_table


def test_check_version():
    assert check_version("1.2", "==1.2") is True
    assert check_version("1.2", "==1.3") is False


@pytest.mark.parametrize("specifier_set", ["~=1.2b,<=1.3a,!=1.2.0", "~=1.2b10"])
def test_generate_versions_table(specifier_set):
    assert "<table>" not in generate_versions_table(specifier_set)
    assert "<table>" not in generate_versions_table(specifier_set, fmt="github")
    assert "<table>" in generate_versions_table(specifier_set, fmt="html")
