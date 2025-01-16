[![Bandit](https://img.shields.io/badge/security-bandit-yellow.svg)](https://bandit.readthedocs.io/en/latest/)
[![Docker Build and Release](https://github.com/elixircloud/jupyterhub/actions/workflows/release_docker.yaml/badge.svg)](https://github.com/elixircloud/jupyterhub/actions/workflows/release_docker.yaml)
[![License](https://img.shields.io/github/license/elixircloud/jupyterhub)](LICENSE)
[![Latest Release](https://img.shields.io/github/v/release/elixircloud/jupyterhub)](https://github.com/elixircloud/jupyterhub/releases)
[![Python 3.13.0](https://img.shields.io/badge/python-3.13.0-blue.svg)](https://www.python.org/)
[![Ruff](https://img.shields.io/badge/linter%20&%20formatter-ruff-000000.svg)](https://docs.astral.sh/ruff/)
[![Safety](https://img.shields.io/badge/security-safety-orange.svg)](https://safetycli.com/product/safety-cli)

# Jupyterhub

All configurations, images, and scripts for the `Jupyterhub` deployment.

## Table of Contents

- [Basic Usage](#basic-usage)
- [Installation](#installation)
- [Development](#development)
  - [Makefile](#makefile)
  - [Environment reproducibility](#environment-reproducibility)
    - [asdf](#asdf)
    - [Dev containers](#dev-containers)
    - [Editor config](#editor-config)
    - [Setting environment variables (direnv)](#setting-environment-variables-direnv)
- [Releases and versioning](#releases-and-versioning)
- [License](#license)

## Basic Usage

## Installation

## Development

### Makefile

For ease of use, certain scripts have been abbreviated in `Makefile`, make sure
that you have installed the dependencies before running the commands.

> **Note**: `make` commands are only available for `Unix-based` systems or
> inside `Dev container`.

To view the commands available, run:

```sh
make
```

Here are certain commands that you might find useful:

- Make a virtual environment

```sh
make v
```

- Install all dependencies including optional dependencies

```sh
make i
```

> **Note**: This project uses optional dependency groups such as `types`,
> `code_quality`, `vulnerability`, `test`, and `misc`. To install stubs or types
> for the dependencies, you **must** use the following command:
>
> ```sh
> poetry add types-foo --group types
> ```
>
> Replace `types-foo` with the name of the package for the types. All runtime
> dependencies should be added to the `default` group. For example, to install
> `requests` and its type stubs, run:
>
> ```sh
> poetry add requests
> poetry add types-requests --group types
> ```
>
> This ensures that the type checker functions correctly.
>
> **Note**: Since the dependencies are segregated into groups, if you add a new
> group make sure to add it in `make install` command in [Makefile](Makefile).

- Run tests

```sh
make t
```

- Run linter, formatter and spell checker

```sh
make fl
```

- Build the documentation

```sh
make d
```

> **Note**: If you make changes to the code, make sure to generate and push the
> documentation using above command, else the documentation check CI will fail.
> Do NOT edit auto-generated documentation manually.

- Run type checker

```sh
make tc
```

- Run all pre-commit checks

```sh
make pc
```

- Update the cookiecutter template

```sh
make u
```

> **Note**: This is not the complete list of commands, run `make` to find out if
> more have been added.

### Environment reproducibility

Below mentioned are some tools and configuration that you can use to make your
environment development-ready. This is optional and opinionated but can help you
set up your environment quickly.

#### asdf

We recommend using [asdf] to manage your development environment efficiently.
This tool allows you to handle multiple language versions and tools seamlessly.
You can install asdf by following the
[official installation guide][asdf-install]. If you are working within
[dev containers](#dev-containers), asdf will come pre-installed. The project
includes a `.tool-versions` file, which lists the specific versions of tools
used. This ensures consistency across environments. To streamline the
installation process, use the following command to install the required tools
defined in the `.tool-versions` file:

```sh
make asdfi
```

> **Note:** The `make asdfi` command might not install every tool listed in the
> `.tool-versions` file. After running the command, verify that all necessary
> tools are installed. If any tools are missing, install them manually using
> asdf.

Example manual installation command:

```sh
asdf install <tool-name> <version>
```

#### Dev Containers

Our project supports [Dev Containers][devcontainers] for an easy and
reproducible setup of development environments via containers. To make use of
it, install the Dev Containers extension in one of the supported editors/IDEs.

For example, for VS Code, do the following to have Dev Containers provision a
container-based development environment for you:

- Make sure [Docker is installed][docker-install] on your machine.
- To install the official Microsoft extension, open the Extensions view
  (<kbd>Ctrl</kbd> + <kbd>Shift</kbd> + <kbd>x</kbd>), enter
  `ms-vscode-remote.remote-containers` in the query box, press <kbd>Enter</kbd>,
  select the "Dev Containers" extension and hit the "Install" button;
  alternatively, use [this direct link][devcontainers-download]
- After reloading VS Code and opening the project folder, you should be prompted
  by the Dev Containers extension to open the workspace in a container. If not,
  press <kbd>Ctrl</kbd> + <kbd>Shift</kbd> + <kbd>g</kbd> to open the command
  panel, search for "Dev Containers: Open Workspace in Container..." and hit
  <kbd>Enter</kbd>

The development environment will now be installed and activated.

> **Note:** The initial process will take some time, as multiple container
> images need to be pulled and dependencies installed. However, once set up,
> activating the environment is fast.

#### Editor Config

To ensure a consistent code style across the project, we include an
`.editorconfig` file that defines the coding styles for different editors and
IDEs. Most modern editors support this file format out of the box, but you might
need to install a plugin for some editors. Please refer to the
[EditorConfig website][editor-config].

#### Setting environment variables (direnv)

Our project uses [.envrc files][direnv] to manage environment variables.
Wherever such a file is required across the project tree, you will find a
`.envrc.template` file that contains the necessary variables and helps you
create your own personal copy of each file. You can find the locations of all
`.envrc.template` files by executing `find . -type f -name \.envrc\.template` in
the root directory. For each, create a copy named `.envrc` in the same
directory, open it in a text editor and replace the template/example values with
your own personal and potentially confidential values.

**Warning:** Be careful not to leak sensitive information! In particular,
**never** add your secrets to the `.envrc.template` files directly, as these are
committed to version control and will be visible to anyone with access to the
repository. Always create an `.envrc` copy first (capitalization and punctuation
matter!), as these (along with `.env` files) are ignored from version control.

Once you have filled in all of your personal information, you can have the
`direnv` tool manage setting your environment variables automatically (depending
on the directory you are currently in and the particular `.envrc` file defined
for that directory) by executing the following command:

```sh
direnv allow
```

> **Note**: Make sure you have `direnv` installed on your system. Follow the
> instructions on the [official website][direnv] to install it. If you are using
> [Dev Containers](#dev-containers), your development environment will have
> `direnv` available and ready to use.

## Releases and versioning

This repository manages two Docker images for JupyterHub deployment: the `hub`
(jupyterhub/hub/hub.Dockerfile) and `notebook`
(jupyterhub/notebook/notebook.Dockerfile) images. Each image has its own version
file and changelog (CHANGELOG.hub.md and CHANGELOG.notebook.md), following
[semantic versioning][semver] (MAJOR.MINOR.PATCH).

To create a release, use the provided `manage_release.py` script:

```bash
python manage_release.py [hub|notebook] --bump [patch|minor|major] --changes "changelog message"
```

Example:

```bash
python manage_release.py hub --bump minor --changes "#### Added
- New authentication plugin support
- Updated base image to Ubuntu 22.04

#### Fixed
- Permission issues in home directory"
```

The script will bump the version, update the changelog and create a git tag. On
pushing the tag to Github a workflow will be triggered that builds
multi-architecture images (amd64, arm64), pushes them to Docker Hub and creates
a GitHub release with the changelog.

> **Note**: Administrators need to configure Docker Hub credentials
> (DOCKERHUB_USERNAME and DOCKERHUB_TOKEN) in the repository secrets.

## License

[asdf]: https://asdf-vm.com/
[asdf-install]: https://asdf-vm.com/guide/getting-started.html
[devcontainers]: https://code.visualstudio.com/docs/devcontainers/containers
[devcontainers-download]: https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers
[direnv]: https://direnv.net/
[docker-install]: https://docs.docker.com/engine/install/
[editor-config]: https://editorconfig.org/
[semver]: https://semver.org/
