---
layout: default
title: Siunitx Configuration
nav_order: 2
---

# `siunitx` Configuration
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

The [`siunitx`] package offers a wide range of options to configure the formatting of numbers and units in LaTeX. In the exported `results.tex` file, we make use of `siunitx` syntax, e.g. we might transform a `wiz.res()` call into something like `\qty{1.23 \pm 0.05}{\m\per\s^2}` that you also could have written manually. This means, you have full control over how the numbers and units are displayed in your LaTeX document by configuring `siunitx` itself.

If you want to configure `ResultWizard` itself instead, see the [`config_init()` & `config()`](/api/config) methods.


## Important configuration options

All options are specified as `key=value` pairs in `\sisetup{}` inside your LaTeX preamble (before `\begin{document}`), e.g.:
```latex
\usepackage{siunitx}
\sisetup{
	locale=US,
	group-separator={,},
	group-digits=integer,
	per-mode=symbol,
	uncertainty-mode=separate,
}
```

Here, we present just a small (admittedly random) subset of the options of [`siunitx`]. See the **[`siunitx` documentation](https://texdoc.org/serve/siunitx/0).** for more details and all available options.

[Siunitx Documentation](https://texdoc.org/serve/siunitx/0){: .btn .btn-primary .fs-5 .mb-4 .mb-md-0 .mr-2 }

- `locale=UK|US|DE|PL|FR|SI|ZA`. This option sets the locale for the output of numbers and units, e.g. in English speaking countries, the decimal separator is a dot `1.234`, while in Germany it's a comma `1,234`.
- `group-separator={,}`. This option sets the group separator, e.g. `1,234,567`.
- `group-digits=integer=none|decimal|integer`. This option affects how the grouping into blocks of three is taking blace.
- `per-mode=power|fraction|symbol`. This option allows to specify how `\per` is handled (e.g. in the case of this unit: `\joule\per\mole\per\kelvin`). `fraction` uses the `\frac{}` command, while `symbol` uses a `/` symbol per default (can be changed with `per-symbol`).
- `uncertainty-mode=full|compact|compact-marker|separate`. When a single uncertainty is given, it can be printed in parentheses, e.g. `1.234(5)`, or with a `±` sign, e.g. `1.234 ± 0.005` (use `separate` as option to achieve this). In older versions of `siunitx`, there existed the following flag instead: `separate-uncertainty=true|false` (it might still work in newer versions).
- `exponent-product=\times`. This option allows to specify the product symbol between mantissa and exponent, e.g. `1.23 \times 10^3` or `1.23 \cdot 10^3`. The latter is more common in European countries. This is also affected by the `locale` option.





[`siunitx`]: https://ctan.org/pkg/siunitx
