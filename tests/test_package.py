from pip_dev import __version__


def test_package_version():
    assert all(map(lambda x: x.isnumeric(), __version__.split(".")))
