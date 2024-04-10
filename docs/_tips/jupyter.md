---
layout: default
title: Jupyter Notebook
nav_order: 1
---

# Jupyter Notebook
{: .no_toc }

<details open markdown="block">
  <summary>
    Content
  </summary>
  {: .text-delta }

- TOC
{:toc}

</details>

{: .warning}
This page is currently in construction.


## Useful defaults

In the context of a *Jupyter Notebook*, you might find this configuration at the beginning useful:
```py
wiz.config_init(print_auto=True, export_auto_to="../results.tex", ignore_result_overwrite=True)
```
With the `print_auto` option set to `True`, you will see the results printed to the console automatically without having to call `.print()` on them. The `export_auto_to` option will automatically export the results to a file each time you call `.res()`. With the `ignore_result_overwrite` option you won't see a warning if you overwrite a result with the same name. This is useful in Jupyter notebooks where you might run the same cell multiple times.
