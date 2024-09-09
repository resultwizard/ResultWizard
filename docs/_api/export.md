---
layout: default
title: wiz.export()
nav_order: 3
---

# `wiz.export()`
{: .no_toc }

<details markdown="block">
  <summary>
    Content
  </summary>
  {: .text-delta }

- TOC
{:toc}

</details>


## Purpose

Call `wiz.export()` after you have defined your results with `wiz.res()`. `wiz.export()` will generate a LaTeX file containing all your results. This file can be included in your LaTeX document with `\input{./path/to/results.tex}` in the LaTeX preamble (see [here]({{site.baseurl}}/quickstart#2-include-results-in-latex)).

## Usage

```py
wiz.export(filepath: str)
```

- `filepath` (str): The (relative or absolute) path to the LaTeX file to be generated, e.g. `./results.tex`.


## Tips

- The `filepath` should end with `.tex` to be recognized as a LaTeX file by your IDE / LaTeX editor.
- For a convenient setup, have Python code reside next to your LaTeX document. This way, you can easily reference the generated LaTeX file. For example, you could have two folders `latex/` & `code/` in your project. Then export the results to `../latex/results.tex` from your python code residing in the `code` folder. In LaTeX, you can then include the file with `\input{./results.tex}`.
- Especially for Jupyter Notebooks, we recommend to use the [`export_auto_to` config option]({{site.baseurl}}/api/config#export_auto_to). This way, you can automatically export the results to a file after each call to `wiz.res()`. See [this page]({{site.baseurl}}/tips/jupyter) for a suitable configuration of `ResultWizard` in Jupyter Notebooks.
