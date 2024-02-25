# Development Guideline/Conventions/Installation

Just a dump for right now. In construction... Maybe a wiki would also be a good place for this.


## Checklist
Getting ready:
- [ ] GPG key setup to sign commits
- [ ] Recommended VSCode extensions installed (especially the formatter. It should automatically format on every save!)
- [ ] on branch `value-wizard` with latest commit pulled
- [ ] Work through the `Setup` section below (especially to install the necessary dependencies)
- [ ] Read the [`README.md`](https://github.com/paul019/ValueWizard/tree/value-wizard/src#code-structure) in the `src` folder (to get to know the code structure) & see our [feature list](https://github.com/paul019/ValueWizard/issues/16)

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
