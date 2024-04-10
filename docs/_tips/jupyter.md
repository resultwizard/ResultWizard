---
layout: default
title: Jupyter Notebook
nav_order: 1
---

# Jupyter Notebook
{: .no_toc }

<details markdown="block">
  <summary>
    Content
  </summary>
  {: .text-delta }

- TOC
{:toc}

</details>

{: .warning }
Note that using a Jupyter Notebook **in a browser** won't make much sense in conjunction with `ResultWizard` as you won't be able to directly include the results in your LaTeX document. However, you can still use `ResultWizard` to export the `results.tex` file and copy the contents manually into your LaTeX document. But this is not the originally intended workflow and might be tedious
<br>Note that VSCode offers great support for Jupyter Notebook natively, see [this guide](https://code.visualstudio.com/docs/datascience/jupyter-notebooks).

## Useful configuration

In the context of a [*Python Jupyter Notebook*](https://jupyter.org/), you might find this `ResultWizard` configuration useful:
```py
wiz.config_init(print_auto=True, export_auto_to="./results.tex", ignore_result_overwrite=True)
```
- With the `print_auto` option set to `True`, you will see the results printed to the console automatically without having to call `.print()` on them.
- The `export_auto_to` option will automatically export the results to a file each time you call `.res()`. That is, you don't have to scroll down to the end of your notebook to call `wiz.export()`. Instead, just execute the cell where you call `.res()` and the results will be exported to the file you specified automatically.
- With the `ignore_result_overwrite` option you won't see a warning if you overwrite a result with the same name. This is useful in Jupyter notebooks since cells are often executed multiple times.


## Cell execution order & cache

Watch out if you use [`wiz.config()`](/api/config) in a Jupyter Notebook. The order of the cell execution is what matters, not where they appear in the document. E.g. you might call `wiz.config()` somewhere at the end of your notebook. Then go back to the top and execute a cell with `wiz.res()`. The configuration will be applied to this cell as well. This is an inherent limitation/feature of Jupyter Notebooks, just be aware of it.

It might be useful to reset the kernel and clear all outputs from time to time. This way, you can also check if your notebook still runs as expected from top to bottom and exports the results correctly. It can also help get rid of any clutter in `results.tex`, e.g. if you have exported a variable that you deleted later on in the code. This variable will still be in `results.tex` as deleting the `wiz.res()` line in the code doesn't remove the variable from the cache.
