# Contribute to httpdomain

-   Report issues in the [issue tracker](https://github.com/sphinx-contrib/httpdomain/issues).
-   Comment on and resolve issues.
-   Submit pull requests from your fork of the httpdomain repository.
-   Extend the [documentation](https://sphinxcontrib-httpdomain.readthedocs.io/en/stable/).
-   Sponsor development of httpdomain through [GitHub Sponsors](https://github.com/sponsors/stevepiercy).


## Prerequisites

-   uv
-   GNU Make


### uv

Install uv using the [standalone installer method](https://docs.astral.sh/uv/getting-started/installation/#standalone-installer) for your system.


### GNU Make

GNU Make comes installed on most Linux distributions.
On macOS, you must first [install Xcode](https://developer.apple.com/xcode/resources/), then install its command line tools.
On Windows, it is strongly recommended to [Install Linux on Windows with WSL](https://learn.microsoft.com/en-us/windows/wsl/install), which will include `make`.

Finally, it is a good idea to update your system's version of `make`, because some distributions, especially macOS, have an outdated version.
Use your favorite search engine or trusted online resource for how to update `make`.


## Install httpdomain for development

Begin by cloning the httpdomain repository from GitHub.

```shell
git clone https://github.com/sphinx-contrib/httpdomain.git
```

Change your working directory to the cloned repository.

```shell
cd httpdomain
```

Then install a supported Python version for development, create a Python virtual environment, install requirements for development, and install the package in development mode with a single command.

```shell
make dev
```

uv tool install tox --with tox-uv


## Pull request requirements

Before submitting your pull request, ensure you have met the following requirements.

1.  Add a changelog entry to `docs/changelog.rst`.
1.  Add a test which proves your fix and passes.
1.  Run all tests to ensure your changes don't break any existing functionality.
1.  Add or edit documentation, both as docstrings and narrative documentation, as necessary.

