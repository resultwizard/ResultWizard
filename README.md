<div align="center">
  <img src="https://github.com/paul019/ResultWizard/assets/37160523/8576038a-3867-470b-8f42-90b60ea92042" width="120px" />
  <div align="center">
    <h3 align="center">ResultWizard</h3>
    <p><strong>Intelligent interface between Python-computed values and your LaTeX work</strong></p>
  </div>
</div>

> [!important]  
> ResultWizard is currently fully functional but still in its *alpha* stage. We're happy to receive your feedback. Basic usage is as follows:


## Installation & usage

```sh
# Install the package via pip
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

wiz.export("results.tex")
```

Then add the following line to your LaTeX document right before `\begin{document}`:

```
\input{results.tex}
```

You can now go ahead and reference the variable in your LaTeX document in any math environment, e.g.:

```latex
\begin{align}
    \resLengthAtom
\end{align}
```

You can also only use a specific part of the result, e.g. the unit, the value itself etc.

```latex
\begin{align}
    \resLengthAtom[unit]
\end{align}
```

A more comprehensive documentation will be available as soon as the package is stable.
