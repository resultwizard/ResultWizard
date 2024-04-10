---
layout: default
title: Quickstart
permalink: quickstart
nav_order: 2
---

# Quickstart
{: .no_toc }

<details open markdown="block">
  <summary>
    Content
  </summary>
  {: .text-delta }

- TOC
{:toc}

</details>



## 💻 Installation & prerequisites

{: .tldr }
> Have a LaTeX toolchain including [`siunitx`] set up and Python `>=3.8` installed.<br>Then install the `ResultWizard` package via [`pip`]:
> ```
pip install resultwizard    # use `pip install resultwizard==1.0.0a2` in the current alpha stage
```
> Move on to [Basic usage](#-basic-usage).



### Python package

You can install `ResultWizard` via [`pip`]:

```
pip install resultwizard
```

{: .warning }
ResultWizard is currently fully functional but still in its **alpha stage**, i.e. the API might change. We're happy to receive your feedback until the first stable release.
<br>Please report any issues on [GitHub](https://github.com/resultwizard/ResultWizard/issues). To get the latest alpha version, you have to install it via
<br>`pip install resultwizard==1.0.0a2` (otherwise you end up using the older version `0.1`).

Verify you're using the version you intended to install:

```
pip show resultwizard | grep Version
```

### LaTeX toolchain

To compile the LaTeX document, you need a working LaTeX toolchain. If you don't have one yet, there are many guides available online for different OS, e.g. the [LaTeX project website](https://www.latex-project.org/get/).
- For MacOS, you might want to use [MacTex](https://www.tug.org/mactex/).
- For Windows, we recommend [MikTex](https://miktex.org/).
- For Linux (Ubuntu, e.g. also in WSL), we recommend [Tex Live](https://www.tug.org/texlive/)[^1]:
```
sudo apt install texlive texlive-latex-extra texlive-science
```


No matter what LaTeX distribution you're using, you will have to install the [`siunitx`] LaTeX package. This package is used to format numbers and units in LaTeX, e.g. for units you can use strings like `\kg\per\cm`. In the Tex Live distribution, this package is already included if you have installed `sudo apt texlive-science`.


### Checklist

- [x] Python `>=3.8` installed & `ResultWizard` installed via [`pip`]
- [x] LaTeX toolchain set up, e.g. TeX Live
- [x] [`siunitx`] LaTeX package installed








## 🌟 Basic usage

{: .tldr }
> 1. Import the library in your Python code, declare your results and export them:
>```py
# In your Python code
import resultwizard as wiz
wiz.res("Tour Eiffel Height", 330.362019, 0.5, "\m")  # units must be `siunitx` compatible
wiz.export("./results.tex")
```
> 2. Include the results in your LaTeX document:
>```latex
% In your LaTeX document
\input{./results.tex}
\begin{document}
    The height of the Eiffel Tower is given by $h = \resultTourEiffelHeight$.
    % also try out: $h = \resultTourEiffelHeight[value]$
\end{document}
```


### 1. Declare & export variables in Python

In your Python code, import `ResultWizard` and use the `wiz.res` function to declare your results. Then, export them to a LaTeX file by calling `wiz.export`. For the unit, you must use a [`siunitx`] compatible string, e.g. `\m` for meters or `\kg\per\s^2`. See the [siunitx docs](https://ftp.tu-chemnitz.de/pub/tex/macros/latex/contrib/siunitx/siunitx-code.pdf#page=31) for more information.

```py
import resultwizard as wiz

# your complex calculations
# ...
value = 330.362019  # decimal places are made up
uncertainty = 0.5
wiz.res("Tour Eiffel Height", value, uncertainty, "\m").print()
# will print: TourEiffelHeight = (330.4 ± 0.5) m

wiz.export("./results.tex")
```
There are many [more ways to call `wiz.res()`](TODO), try to use IntelliSense (`Ctrl + Space`) in your IDE to see all possibilities. If you want to omit any rounding, pass in values as string, e.g.:
```py
wiz.res("pi", "3.1415").print() # congrats, you found an exact value for pi!
# will print: pi = 3.1415
wiz.res("Tour Eiffel Height", str(value), str(uncertainty), "\m").print()
# will print: TourEiffelHeight = (330.362019 ± 0.5) m
```

You can also use the `wiz.config_init` function to set some defaults for the whole program. See many more [configuration options here](config).
```py
wiz.config_init(sigfigs_fallback=3, identifier="customResult")
# default to 2 and "result" respectively
```

If you're working in a *Jupyter Notebook*, please see [this page](tips/jupyter) for a suitable configuration of `ResultWizard` that doesn't annoy you with warnings and prints/exports the results automatically.


### 2. Include results in LaTeX

You have either called `wiz.export(.results.tex)` or set up automatic exporting with `wiz.config_init(export_auto_to="./results.tex")`. In any case, you end up with a LaTeX file `./results.tex`. Import it in your LaTeX preamble (you only have to do this once for every new document you create):

```latex
% Your LaTeX preamble
\input{./results.tex}
\begin{document}
...
```

Then, you can reference the variables in your LaTeX document:

```latex
% Your LaTeX document
This allowed us to calculate the acceleration due to gravity $g$ as
\begin{align}
    g &= \resultG
\end{align}
Therefore, the height of the Eiffel Tower is given by $h = \resultTourEiffelHeight$.
```

It will render as follows (given respective values for `g` and `Tour Eiffel Height` are exported):

![result rendered in LaTeX](https://github.com/resultwizard/ResultWizard/assets/37160523/d2b5fcce-fa99-4b6f-b32a-26125e5c6d9b)

If you set up your IDE or your LaTeX editor properly, you can use IntelliSense (`Ctrl + Space`) here as well to see all available results, e.g. type `\resultTo`. Changing the value in Python and re-exporting will automatically update the value in your LaTeX document[^2].

Also try out the following syntax:

```latex
% Your LaTeX document
The unit of $h$ is $\resultTourEiffelHeight[unit]$ and its value is $\resultTourEiffelHeight[value]$.
```

Use `\resultTourEiffelHeight[x]` to get a message printed in your LaTeX document informing you about the possible strings you can use instead of `x` (e.g. `withoutUnit`, `value` etc.).

---

[^1]: For differences between texlive packages, see [this post](https://tex.stackexchange.com/a/504566/). For Ubuntu users, there's also an installation guide available [here](https://wiki.ubuntuusers.de/TeX_Live/#Installation). If you're interested to see how Tex Live can be configured in VSCode inside WSL, see [this post](https://github.com/Splines/vscode-latex-wsl-setup).
[^2]: You have to recompile your LaTeX document, of course. But note that you can set up your LaTeX editor / IDE to recompile the PDF automatically for you as soon as any files, like `results.tex` change. For VSCode, you can use the [LaTeX Workshop extension](https://marketplace.visualstudio.com/items?itemName=James-Yu.latex-workshop) for this purpose, see a guide [here](https://github.com/Splines/vscode-latex-wsl-setup). In the best case, you only have to update a variable in your Python code (and run that code) and see the change in your PDF document immediately.

[`siunitx`]: https://ctan.org/pkg/siunitx
[`pip`]: https://pypi.org/project/resultwizard
