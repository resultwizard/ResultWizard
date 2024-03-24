<div align="center">
  <img src="https://github.com/paul019/ResultWizard/assets/37160523/8576038a-3867-470b-8f42-90b60ea92042" width="120px" />
  <div align="center">
    <h3 align="center">ResultWizard</h3>
    <p><strong>Intelligent interface between Python-computed values and your LaTeX work</strong></p>
  </div>
</div>

> **Warning ⚠**
> ResultWizard is currently fully functional but still in its *alpha* stage. We're happy to receive your feedback. Basic usage is as follows. A more comprehensive documentation will be available as soon as the package is stable.


## Installation & basic usage
Install the package via pip.

```sh
pip install resultwizard
```

Then you can use `ResultWizard` in your Python code:

```python
import resultwizard as wiz
wiz.config_init(print_auto=True)

# your complex calculations
# ...
value = 42.0
uncertainty = 3.14
wiz.res("length atom", value, uncertainty, r"\per\mm\cubed")
# There are many more ways to call wiz.res(...), try to use
# IntelliSense in your IDE to see all possibilities.
# A more in-depth documentation will follow in next releases.

# Export the result to a LaTeX file. Provide a path as string
# where the file should be saved.
wiz.export("./results.tex")
```

Now add the following line to your LaTeX document right before `\begin{document}`:

```latex
% assuming that `results.tex` is located in the same directory
% as your LaTeX document
\input{./results.tex}

\begin{document}
...
```

Note that `ResultWizard` requires the following LaTeX packages: [`siunitx`](https://ctan.org/pkg/siunitx) and [`ifthen`](https://ctan.org/pkg/ifthen). They are imported in the `results.tex` file via `\usepackage{...}` statements. The package `ifthen` is always present in a LaTeX distribution. You may have to install the `siunitx` package, which is a widely used package in the scientific community to typeset units, e.g. you can use strings like `\kg\per\cm`.

You can now go ahead and **use the variable in your LaTeX document** in any math environment, e.g.:

```latex
\begin{align}
    \resLengthAtom
\end{align}
```

You can also only use a specific part of the result, e.g. the unit, the value itself etc. (try to use a random key like `\resLengthAtom[x]` and compile your LaTeX document to see more options).

```latex
\begin{align}
    \resLengthAtom[unit]
\end{align}
```

---

If your LaTeX document does not compile, try to set

```python
wiz.config_init(siunitx_fallback=True)
```

in your `ResultWizard` configuration. If the LaTeX document compiles after this, you have an older version of `siunitx` installed. We recommend to upgrade the package to at least version `v3.1.0` to be able to fully customize the output of the result in your LaTeX document via `\sisetup{...}`. See the troubleshooting section down below for more information.


## Troubleshooting: LaTeX doesn't build

If your LaTeX document doesn't build, there might be several reasons. Try to find out what's wrong by looking at the log file of your LaTeX compiler (sometimes you have to scroll way up to find the error responsible for the failing build). Also open the `results.tex` file to see if your editor/IDE shows any errors there. You might encounter one of the following errors:

<details>

<summary><strong>Package siunitx: Invalid number.</strong></summary>

TL;DR: You have an **old version of `siunitx`**. Please update it or use the `siunitx_fallback` option in the `config_init` method.

In version [`v3.1.0 (2022-04-25)`](https://github.com/josephwright/siunitx/blob/main/CHANGELOG.md#v310---2022-04-25), `siunitx` introduced "support for multiple uncertainty values in both short and long form in input". We make use of this feature in `ResultWizard`.

Unfortunately, it may be the case that you're using an older version of `siunitx`. Especially if you've installed LaTeX via a package manager (e.g. you installed `siunitx` via `sudo apt install texlive-science`). To determine your version, include the following line in your LaTeX document:

```latex
\listfiles % add this before \begin{document}
```

Then, compile your document and check the log for the version of `siunitx`. If it's older than `v3.1.0 (2022-04-25)`, don't despair. We have two solutions for you:

**Solution 1: Don't update `siunitx` and stick with your old version**

Sure, fine, we won't force you to update `siunitx` (although we'd recommend it). To keep using your old version, specify the following key in the `config_init` method:

```python
wiz.config_init(siunitx_fallback=True)
```

Note that with this "solution", you won't be able to fully customize the output of the result in your LaTeX document. For example, we will use a `±` between the value and the uncertainty, e.g. `3.14 ± 0.02`. You won't be able to change this in your `sisetup` by doing:

```latex
\sisetup{separate-uncertainty=false}
```

to get another format like `3.14(2)`. There are also some [other `siunitx` options](https://texdoc.org/serve/siunitx/0) that won't work with `ResultWizard`, e.g. `exponent-product`. If you're fine with this, go ahead and use the `siunitx_fallback` option. If not, consider updating `siunitx` to at least version `v3.1.0`.

**Solution 2: Update `siunitx` (recommended)**

How the update process works depends on your LaTeX distribution and how you installed it. E.g. you might be using `TeX Live` on `Ubuntu` and installed packages via `apt`, e.g. `sudo apt install texlive-science` (which includes the LaTeX `siunitx`). These pre-built packages are often outdated, e.g. for Ubuntu 22.04 LTS (jammy), the `siunitx` package that comes with the `texlive-science` package is `3.0.4`. Therefore, you might have to update `siunitx` manually. See an overview on how to install individual LaTeX packages on Linux [here](https://tex.stackexchange.com/a/73017/).

A quick solution might be to simply install a new version of `siunitx` manually to your system. There's a great and short Ubuntu guide on how to install LaTeX packages manually [here](https://help.ubuntu.com/community/LaTeX#Installing_packages_manually). The following commands are based on this guide. We will download the version `3.1.11 (2022-12-05)` from GitHub (this is the last version before `3.2` where things might get more complicated to install) and install it locally. Nothing too fancy. Execute the following commands in your terminal:

```sh
# Install "unzip", a tool to extract zip files
sudo apt install unzip

# Download v3.1.11 of siunitx from GitHub
curl -L https://github.com/josephwright/siunitx/releases/download/v3.1.11/siunitx-ctan.zip > siunitx-ctan-3.1.11.zip

# Unzip the file
unzip ./siunitx-ctan-3.1.11.zip
cd siunitx/

# Run LaTeX on the .ins file to produce a usable .sty file
# (The .sty file is needed when you use \usepackage{siunitx}
# in your LaTeX document)
latex siunitx.ins

# Create a new directory in your home directory
# to store the new package .sty file
mkdir -p ~/texmf/tex/latex/siunitx
cp siunitx.sty ~/texmf/tex/latex/siunitx/

# Make LaTeX recognize the new package by pointing it to the new directory
texhash ~/texmf/

# 🙌 Done. Try to rebuild your LaTeX document again.

# If you don't wan't the new siunitx version anymore, just run the following
# command to remove the .sty file. LaTeX will then use the version of siunitx
# it finds somewhere else in your system.
rm ~/texmf/tex/latex/siunitx/siunitx.sty
```

Compiling your latex document again, you should see version `v3.1.11` of `siunitx` in the log file. And it should build, yeah 🎉. Don't forget to remove the `\listfiles` from your LaTeX document to avoid cluttering your log file (which is ironic for LaTeX, we know).

</details>
