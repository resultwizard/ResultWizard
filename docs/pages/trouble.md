---
layout: default
title: Troubleshooting
permalink: trouble
nav_order: 3
---

# Troubleshooting
{: .no_toc }

<details open markdown="block">
  <summary>
    Content
  </summary>
  {: .text-delta }

- TOC
{:toc}

</details>

There might be several reasons for your LaTeX document not building. **Try to find the root cause** by looking at the **log file** of your LaTeX compiler (sometimes you have to scroll way up to find the error responsible for the failing build). Also open the [exported](/api/export) `results.tex` file to see if your editor/IDE shows any errors there. You might encounter one of the following problems. Please make sure to try the solutions provided here before opening an [issue on GitHub](https://github.com/resultwizard/ResultWizard/issues).



## Package siunitx: Invalid number

{: .tldr}
You have probably specified **multiple uncertainties** in `wiz.res()`, right? If this is the case and you get this error, you have an **old version of `siunitx`** installed. Please update it (recommended) or use the `siunitx_fallback` option in the [`config_init`](/api/config) method.

In version [`v3.1.0 (2022-04-25)`](https://github.com/josephwright/siunitx/blob/main/CHANGELOG.md#v310---2022-04-25), `siunitx` introduced "support for multiple uncertainty values in both short and long form input". We make use of this feature in `ResultWizard` when you specify multiple uncertainties for a result.

Unfortunately, it may be the case that you're using an older version of `siunitx` that doesn't ship with this feature yet. Especially if you've installed LaTeX via a package manager (e.g. you installed `siunitx` via `sudo apt install texlive-science`). To determine your `siunitx` version, include the following line in your LaTeX document:

```latex
\listfiles % add this before \begin{document}, i.e. in your LaTeX preamble
```

Then, compile your document and check the log for the version of `siunitx`.
<br>If it's **older than `v3.1.0 (2022-04-25)`**, don't despair. We have two solutions for you:

### Solution 1: Don't update `siunitx` and stick with your old version

Sure, fine, we won't force you to update `siunitx` (although we'd recommend it). To keep using your old version, specify the following key in the `config_init` method:

```python
wiz.config_init(siunitx_fallback=True)
```

Note that with this "solution", you won't be able to fully customize the output of the result in your LaTeX document. For example, we will use a `±` between the value and the uncertainty, e.g. `3.14 ± 0.02`. You won't be able to change this in your `sisetup` by specifying

```latex
\sisetup{separate-uncertainty=false}
```

to get another format like `3.14(2)`. There are also some other `siunitx` options that won't probably work with `ResultWizard`, e.g. [`exponent-product`](https://texdoc.org/serve/siunitx/0#page=29). If you're fine with this, go ahead and use the `siunitx_fallback` option. If not, consider updating `siunitx` to at least version `v3.1.0`.

### Solution 2: Update `siunitx` (recommended, but more effort)

How the update process works depends on your LaTeX distribution and how you installed it. E.g. you might be using `TeX Live` on `Ubuntu` and installed packages via `apt`, e.g. `sudo apt install texlive-science` (which includes the LaTeX `siunitx`). These pre-built packages are often outdated, e.g. for Ubuntu 22.04 LTS (jammy), the `siunitx` version that comes with the `texlive-science` package is `3.0.4`. Therefore, you might have to update `siunitx` manually. See an overview on how to install individual LaTeX packages on Linux [here](https://tex.stackexchange.com/a/73017/).

A quick solution might be to simply install a new version of `siunitx` manually to your system. There's a great and short Ubuntu guide on how to install LaTeX packages manually [here](https://help.ubuntu.com/community/LaTeX#Installing_packages_manually). The following commands are based on this guide. We will download the version `3.1.11 (2022-12-05)` from GitHub (this is the last version before `3.2` where things might get more complicated to install) and install it locally. Don't be scared, do it one step at a time and use the power of GPTs and search engines in case you're stuck. Execute the following commands in your terminal:

```sh
# Install "unzip", a tool to extract zip files
sudo apt install unzip

# Download v3.1.11 of siunitx from GitHub
curl -L https://github.com/josephwright/siunitx/releases/download/v3.1.11/siunitx-ctan.zip > siunitx-ctan-3.1.11.zip

# Unzip the file
unzip ./siunitx-ctan-3.1.11.zip
cd siunitx/

# Run LaTeX on the .ins file to generate a usable .sty file
# (LaTeX needs the .sty file to know what to do with the \usepackage{siunitx}
# command in your LaTeX preamble.)
latex siunitx.ins

# Create a new directory in your home directory
# to store the new package .sty file
mkdir -p ~/texmf/tex/latex/siunitx  # use any location you want, but this one is common
cp siunitx.sty ~/texmf/tex/latex/siunitx/

# Make LaTeX recognize the new package by pointing it to the new directory
texhash ~/texmf/
```

🙌 Done. Try to recompile your LaTeX document again. You should see version `v3.1.11` of `siunitx` in the log file. And it should build. Don't forget to remove the `\listfiles` from your LaTeX document to avoid cluttering your log file (which is ironic for LaTeX, we know).

In case you don't wan't the new siunitx version anymore, just run the following command to remove the `.sty` file. LaTeX will then use the version of siunitx it finds somewhere else in your system (which is probably the outdated one you had before).
```sh
rm ~/texmf/tex/latex/siunitx/siunitx.sty
```
