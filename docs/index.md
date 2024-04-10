---
layout: home
title: Home
nav_order: 1
---
<div>
    <img src="https://github.com/resultwizard/ResultWizard/assets/37160523/cf0ccf2c-f110-42a4-a6f6-5d29c51466b8"
        alt="ResultWizard Header Image">
</div>

# ResultWizard
{: .fs-9 }

Think of ResultWizard as the glue<br>
between Python code & your LaTeX work.
<!-- Intelligent interface between Python-computed values<br>and your LaTeX work. -->
{: .fs-6 .fw-300 }

```
pip install resultwizard
```

{% capture intro_link %}{{ site.baseurl }}{% link pages/quickstart.md %}{% endcapture %}
[Quickstart]({{intro_link}}){: .btn .btn-primary .fs-5 .mb-4 .mb-md-0 .mr-2 }
[Source Code (GitHub)](https://github.com/resultwizard/ResultWizard){: .btn .fs-5 .mb-4 .mb-md-0 }
[PyPI](https://pypi.org/project/resultwizard/){: .btn .fs-5 .mb-4 .mb-md-0 }


{: .warning }
ResultWizard is currently fully functional but still in its **alpha stage**, i.e. the API might change. We're happy to receive your feedback until the first stable release.
<br>Please report any issues on [GitHub](https://github.com/resultwizard/ResultWizard/issues). To get the latest alpha version, you have to install it via `pip install resultwizard==1.0.0a2` (otherwise you end up using the older version `0.1`).

---


## 💥 The problem ResultWizard tries to solve

Various scientific disciplines deal with huge amounts of experimental data on a daily basis. Oftentimes, this data is processed in Python to calculate important quantities. In the end, these quantities will get published in scientific papers written in LaTeX. You may have manually copied values from the Python console or a Jupyter notebook to a LaTeX document. This **lack of a programmatic interface between Python code & LaTeX** is what `ResultWizard` is addressing.

## 💡 How does ResultWizard help?

In a nutshell, export any variables from Python including possible uncertainties and their units.

```py
# Your Python code
import resultwizard as wiz
wiz.res("Tour Eiffel Height", 330.0, 0.5, "\m")
wiz.res("g", 9.81, 0.01, "\m/\s^2")
wiz.export("./results.tex")
```

This will generate a LaTeX file `results.tex`. Add this file to your LaTeX preamble:

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
    g &= \resG
\end{align}
Therefore, the height of the Eiffel Tower is given by $h = \resTourEiffelHeight$.
```

That's the gist of `ResultWizard`. Of course, there are many more features and customizations available.


## Why shouldn't I continue to manually copy-paste values?

Here's a few reasons why you should consider using `ResultWizard` as programmatic interface instead:

- _Sync_: By manually copying values, you risk getting your LaTeX document out of sync with your Python code. The latter might have to be adjusted even during the writing process of your paper. And one line of code might change multiple variables that you have to update in your LaTeX document. With `ResultWizard`, you can simply re-export the variables and you're good to go:
- _Significant figures_: `ResultWizard` takes care of significant figures rounding for you, e.g. a result `9.81 ± 0.78` will be rendered as `9.8 ± 0.8` in LaTeX (customizable).

`ResultWizard` allows you to have your variables in one place: your Python code where you calculated them anyways. **Focus on your research, not on copying values around**. 

[Get started now]({{intro_link}}){: .btn .btn-primary .fs-5 .mb-4 .mb-md-0 .mr-2 }
