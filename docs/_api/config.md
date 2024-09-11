---
layout: default
title: wiz.config_init() & wiz.config()
nav_order: 1
---

# `wiz.config_init` & `wiz.config()`
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

The methods `wiz.config_init()` and `wiz.config()` allow you to configure `ResultWizard` to your needs. Note that this mainly affects the rounding mechanism as well as convenience features. How the results are formatted in the LaTeX document is mainly controlled by the `siunitx` package and how you set it up in your LaTeX preamble. If this is what you want to configure, then you should take a look [here]({{site.baseurl}}/tips/siunitx).

## Usage

With `config_init()` you set the initial configuration for `ResultWizard`. With later calls to `config()`, you can update individual settings without having to reconfigure every parameter.

{: .warning }
Some options are only available in `config_init()` and cannot be changed later with `config()`.
<br>TODO: Do we really want that?

Here is the list of available options:

{: .warning }
TODO: sort options alphabetically? Make clearer what the difference between `sigfigs` and `sigfigs_fallback` is. Maybe even rename/unify these options? Same for `decimal_places` and `decimal_places_fallback`. We also need better explanations for `min_exponent_...` and `max_exponent_...`.

| Option | Default | Available in<br>`config_init()` | Available in <br>`config()` | Description |
|:---|:---:|:---:|:---:|:---|
| `sigfigs` (int) | `-1` | ✔ | ✔ | The number of significant figures to round to.<br>TODO: explain what a sigfig is. |
| `decimal_places` (int) | `-1` | ✔ | ✔ | The number of decimal places to round to. |
| `sigfigs_fallback` (int) | `2` | ✔ | ✔ | The number of significant figures to use as a fallback if other rounding rules don't apply. |
| `decimal_places_fallback` (int) | `-1` | ✔ | ✔ | The number of decimal places to use as a fallback if other rounding rules don't apply. |
| `identifier` (str) | `"result"` | ✔ | | The identifier that will be used in the LaTeX document to reference the result. |
| `print_auto` (bool) | `False` | ✔ | ✔ | If `True`, every call to `wiz.res()` will automatically print the result to the console, such that you don't have to use `.print()` on every single result. |
| `export_auto_to` (str) | `""` | ✔ |  | If set to a path, every call to `wiz.res()` will automatically export the result to the specified file. This is especially useful for Jupyter notebooks where every execution of a cell that contains a call to `wiz.res()` will automatically export to the file. |
| `siunitx_fallback` (bool) | `False` | ✔ | | If `True`, `ResultWizard` will use a fallback for the `siunitx` package if you have an old version installed. See [here]({{site.baseurl}}/trouble#package-siunitx-invalid-number) for more information. We don't recommend to use this option and instead upgrade your `siunitx` version to exploit the full power of `ResultWizard`. |
`precision` (int) | `100` | ✔ | | The precision `ResultWizard` uses internally to handle the floating point numbers. You may have to increase this number if you encounter the error "Your precision is set too low". |
| `ignore_result_overwrite` (bool) | `False` | ✔ | | If `True`, `ResultWizard` will not raise a warning if you overwrite a result with the same identifier. This is especially useful for Jupyter notebooks where cells are oftentimes run multiple times. |
| `min_exponent_for_`<br>`non_scientific_notation` (int) | `-2` | ✔ | | The minimum exponent for which `ResultWizard` will use non-scientific notation. If the exponent is smaller than this value, scientific notation will be used. TODO: explain better. |
| `max_exponent_for_`<br>`non_scientific_notation` (int) | `3` | ✔ | | The maximum exponent for which `ResultWizard` will use non-scientific notation. If the exponent is larger than this value, scientific notation will be used. TODO: explain better. |

If you're using a Jupyter Notebook, you might find [this configuration]({{site.baseurl}}/tips/jupyter) useful.
