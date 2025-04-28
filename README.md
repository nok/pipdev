<p align="center">
  <img src="assets/pip-dev-logo.png" alt="pip-dev logo" height="130">
</p>

<h1 align="center">pip-dev</h1>

<p align="center">An interactive tool for testing Python version specifiers.</p>

<div align="center">

![GitHub Repo stars](https://img.shields.io/github/stars/nok/pip-dev)
[![Ko-fi](https://img.shields.io/badge/Ko--fi-FF5E5B?logo=ko-fi&logoColor=white)](https://ko-fi.com/nok)

</div>

<a href="https://nok.github.io/pip-dev?spec=~=1.2b,<=1.3a,!=1.2&vers=1.2.1" target="_demo"><img src="assets/pip-dev-screenshot.png" alt="pip-dev screenshot"></a>


## Description

**​pip-dev** is an interactive tool for testing Python version specifiers as defined by [PEP 440](https://peps.python.org/pep-0440/). It allows developers to input constraints like `>=1.4.5` or `~=1.4.5` and see which versions match, aiding in dependency management. Built on the [pypa/packaging](https://github.com/pypa/packaging) library, it helps ensure compatibility across Python projects.


## Examples

Do you know the difference between `>=1.4.5`, `~=1.4.5` and `==1.4.*`?

- [nok.github.io/pip-dev?spec=>=1.4.5&vers=1.4.5](https://nok.github.io/pip-dev?spec=>=1.4.5&vers=1.4.5)
- [nok.github.io/pip-dev?spec=~=1.4.5&vers=1.4.5](https://nok.github.io/pip-dev?spec=~=1.4.5&vers=1.4.5)
- [nok.github.io/pip-dev?spec===1.4.*&vers=1.4.5](https://nok.github.io/pip-dev?spec=~=1.4.*&vers=1.4.5)

Do you know the difference between `~=1.4.5` and `>=1.4.5,==1.4.*`?

- [nok.github.io/pip-dev?spec=~=1.4.5&vers=1.4.5](https://nok.github.io/pip-dev?spec=~=1.4.5&vers=1.4.5)
- [nok.github.io/pip-dev?spec=>=1.4.5,==1.4.*&vers=1.4.5](https://nok.github.io/pip-dev?spec=>=1.4.5,==1.4.*&vers=1.4.5)

And what about `~=1.2b,<=1.3a,!=1.2`?

- [nok.github.io/pip-dev?spec=~=1.2b,<=1.3a,!=1.2&vers=1.2.1](https://nok.github.io/pip-dev?spec=~=1.2b,<=1.3a,!=1.2&vers=1.2.1)


## License

The package is Open Source Software released under the [BSD 3-Clause License](LICENSE).
