# Python to LaTeX

This package uses reflections to read the values of your global python variables and export them to LaTeX. This makes possible a seamless integrated workflow between Jupyter notebooks and LaTeX documents.

## 1. Use case

For your LaTeX document, you might use a Jupyter notebook to calculate some values. For example, you might have calculated the acceleration of gravity as well as its error:

```
g = 9.810173743
error_g = 0.014193993
# notebook.ipynb
```

Instead of copying and pasting those values to your LaTeX code by hand, this package can do this automatically reading your variables in python. It generates LaTeX code like this:

```
\newcommand*{\resultG}{9.810 \pm 0.014\ \unit{\meter\per\second\squared}}
% results.tex
```

You can reference this value in your LaTeX code as easy as follows:

```
We measured the acceleration of gravity to be $\resultG$.
% main.tex
```

You can even use autocompletion in LaTeX to reference your python variables!

To see how it works in details, read through the following sections.


## 2. Setup and folder structure

This package was designed to be used in the following folder structure setup:

```
src
│   main.tex
│   main.pdf
│   results.tex
│   
└───python
        notebook.ipynb
        python_to_latex.py

```

Here is a quick overview:

- `main.tex` is your entry point to your LaTeX document.
- `main.pdf` is the pdf of your LaTeX document.
- `results.tex` is automatically generated by this package.
- `notebook.ipynb` is your Jupyter notebook.
- `python_to_latex.py` is where the magic takes place. Download and copy this file from this package.

## 3. How to export variables from python

For this package to work, you need to make slight modifications both in your python code and at the end of it.

### 3.1 In your code

Let's say you calculated the acceleration of gravity $g$ and its error $\Delta g$ in your Jupyter notebook:

```
g = 9.810173743
error_g = 0.014193993
# notebook.ipynb
```

Now, there are two possibilities to export these variables:

#### 3.1.1 Possibility 1

Write:

```
result_g = 9.810173743
result_error_g = 0.014193993
result_unit_g = '/meters/per/second/squared'
# notebook.ipynb
```

Explanation:

- Variables that start with `result_` automatically get exported.
- Variables that start with `result_error_` are assumed to carry the corresponding error value.
- Variables that start with `result_unit_` are assumed to carry the corresponding unit. Unit strings have to be in the language of the LaTeX package `siunitx`.

This package automatically does the correct rounding for you! To be precise, it uses one or two significant digits for the error value depending on whether the first error digit is less than or equal to 2.

If you want to overwrite this behavior, you can set the desired number of significant figures for the value itself:

```
result_sigfigs_g = 3
# notebook.ipynb
```

#### 3.1.2 Possibility 2

Instead of using separate global variables for a value, its error and its unit, you can use a tuple:

```
result_g = (9.810173743, 0.014193993, '/meters/per/second/squared')
# notebook.ipynb
```

### 3.2 At the end of your code

At the end of your Jupyter notebook, you have to put (and run!) the following code block:

```
from python_to_latex import export
export(globals())
# notebook.ipynb
```

This will automatically export your desired global variables to python.

## 4. How to import variables in LaTeX

For the units to work, you need to import the package `siunitx` in your `main.tex`:

```
\usepackage{siunitx}
% main.tex
```

Next, you have to import the file generated by this package:

```
\input{./results}
% main.tex
```

Now, you can use the variables that you exported from the Jupyter notebook:

```
We measured the acceleration of gravity to be $\resultG$.
% main.tex
```

Note, that the variable names are converted from snake case in python to camel case in LaTeX.

## 5. Disclaimer

The author of this package does not take any responsibility for errors done by this package.