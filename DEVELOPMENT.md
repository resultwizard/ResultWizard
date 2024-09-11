# Development Guideline/Conventions/Installation

Just a dump for right now. In construction... Maybe a wiki would also be a good place for this.


## Checklist
Getting ready:
- [ ] GPG key setup to sign commits
- [ ] Recommended VSCode extensions installed (especially the formatter. It should automatically format on every save!)
- [ ] on branch `value-wizard` with latest commit pulled
- [ ] Work through the `Setup` section below (especially to install the necessary dependencies)
- [ ] Read the [`README.md`](https://github.com/paul019/ResultWizard/tree/value-wizard/src#code-structure) in the `src` folder (to get to know the code structure) & see our [feature list](https://github.com/paul019/ResultWizard/issues/16)

Verify that everything worked:
- [ ] try to run the tests, see the instructions in [`tests/playground.py`](./tests/playground.py)

Then start working on the code:
- [ ] search for "TODO"s in the code, they will guide you to the next steps
- [ ] document and append to `tests/playground.py` what we expect as user when using this library (we will use this as a reference to test the library later on)
- [ ] try to add doc-strings early on (in relevant places), so that I know what you are doing (and you know what I'm doing :))
- [ ] discuss when you want to restructure `domain` objects (e.g. `_Value`), e.g. if you are annoyed of having to deal with strings instead of floats (but I think with strings we are more flexible)


## Setup

- Install the recommended VSCode extensions. This includes `pylint` (Python linting) and `black` (Python formatting). VSCode is setup via the `settings.json` to format on save.

> [!Tip]
> I've specified recommended extensions, you can install them in VSCode by using [the "recommended" filter](https://code.visualstudio.com/docs/editor/extension-marketplace#_extensions-view-filter-and-commands).

- Install [pipenv](https://pipenv.pypa.io/en/latest/installation.html). I added this to my `.bashrc`:
  ```bash
  alias python3=python3.11
  export PATH="$PATH:~/.local/bin"
  ```
- Install the dependencies: `pipenv install`
- Type in `pipenv` to see available commands, e.g. `pipenv shell` etc.


## TODO
- Setup `.editorconfig` for non-VSCode users. At least provide very basic setup like max line length etc.
- A [`justfile`](https://github.com/casey/just) would also be beneficial.



## Testing ❌✅

As always, make sure you are in the `pipenv shell`.

Make sure you have all (dev) dependencies installed:

```
pipenv install -d
```

Then you can run the tests via the command line:

```
pytest
```

But with VSCode, you get direct integration into the **Test Explorer UI**. You will have to install the recommended extensions first. Then switch to the Testing tab and you will find the tests there. You can run them from there, jump to the file where they are defined and even start debugging them. You can also do the same via the code lens (it shows a little menu "Run | Debug | ..." over every test method) in the test files themselves. Try to set a breakpoint and debug it by clicking "Debug" in the code lens. While debugging, go the debug panel and see some variables there or enter one in the watch tab. Try to modify a test such that it fails and get to know where you see the error.

Also try adding `import pytest` as first line of a test file. Does it give you a warning? If so, you have selected the wrong VSCode Python interpreter. Choose the one provided by the pipenv virtual environment where all dependencies are installed.

Note that tests are also run on every commit via a GitHub action.

In order to learn how to write the tests with pytest, start with the [`Get Started` guide](https://docs.pytest.org/en/8.0.x/getting-started.html#create-your-first-test). Probably also relevant: ["How to use fixtures"](https://docs.pytest.org/en/8.0.x/how-to/fixtures.html). There are lots of [How-to guides](https://docs.pytest.org/en/8.0.x/how-to/index.html) available.


## Release to PyPI

To release a new version to [PyPI](https://pypi.org/project/resultwizard/), do the following:

- Create a PR that is going to get merged into `main`. Name it "Continuous Release <version number, e.g. 1.0.0-alpha.42>".
- Make sure all tests pass and review the PR. Merge it into `main` via a *Merge commit*
<br>(from `dev` to `main` always via *Merge commit*, not *Rebase* or *Squash and merge*).
- On `main`, create a new release on GitHub. In this process (via the GitHub UI), create a new tag named "v<version number>", e.g. "v1.0.0-alpha.42".
- The tag creation will trigger a GitHub action that builds and uploads the package to PyPI. As this action uses a special "release" environment, code owners have to approve this step.
- Make sure the new version is available on PyPI [here](https://pypi.org/project/resultwizard/).
