---
layout: default
title: wiz.res()
nav_order: 2
---

# `wiz.res()`
{: .no_toc }

<details markdown="block">
  <summary>
    Content
  </summary>
  {: .text-delta }

- TOC
{:toc}

</details>

{: .warning}
The API for `wiz.res()` is not yet finalized as of `v1.0.0a2` and might change before the stable release `1.0.0`. This is due to some issues we are currently experiencing with the multiple dispatch mechanism in [`plum`].


## Purpose

`wiz.res()` is at the heart of `ResultWizard`. With this method, you define your results, i.e. numerical values with uncertaintie(s) (optional) and a unit (optional). See the [basic usage](/quickstart#-basic-usage) for a first example.


When we talk about a **"measurement result"**, we usually refer to these components:

- _Value_: The numerical value of your measurement, i.e. the value you have measured and that you are interested in.
- _Uncertainties_: They denote the precision of your measurement since you can never measure a value exactly in the real world. Another term commonly used for this is "error", but we will use "uncertainty" throughout.
- _Unit_: The SI unit of your measurement, e.g. meters, seconds, kilograms etc.


## Usage


### Define a result

`wiz.res()` is overloaded[^1], i.e. you can call it with different argument types and even different number of arguments. This allows you to define your results in a way that suits you best, e.g. sometimes you might only have the value without any uncertainties, or you don't need a unit etc.

In the following, we use these abbreviations. Refer to the [python docs](https://docs.python.org/3/library/decimal.html) if you're unsure about how `Decimal` works. We recommend using `Decimal` for all numerical values to avoid floating point errors. Also see the [precision page](TODO).
```py
numlike := float | int | str | Decimal
numlike_without_int := float | str | Decimal
uncertainties := Tuple[numlike, str] | List[numlike | Tuple[numlike, str]]
```

These are the possible ways to call `wiz.res()`. Note you can use IntelliSense (`Ctrl + Space`) in your IDE to see all possible signatures and get error messages if you use the arguments incorrectly.
```py
wiz.res(name: str, value: numlike)
wiz.res(name: str, value: numlike, unit: str = "")
wiz.res(name: str, value: numlike, uncert: numlike | uncertainties)
wiz.res(name: str, value: numlike, sys: float | Decimal, stat: float | Decimal, unit: str = "")
wiz.res(name: str, value: numlike, uncert: numlike_without_int | uncertainties | None, unit: str = "")
```

{: .warning }
Some signatures of `wiz.res()` don't allow for an `int` to be passed in. This is currently due to a technical limitation that we are trying to work around before the stable release.

Note that `uncert` stands for "uncertainties" and can be a single value (for symmetric uncertainties) or a list (for asymmetric uncertainties). When you specify a tuple, the first element is the numerical value of the uncertainty, the second element is a string that describes the type of uncertainty, e.g. "systematic", "statistical" etc.
```py
wiz.res("i did it my way", 42.0, [0.22, (0.25, "systematic"), (0.314, "yet another one")])

# These two lines are equivalent (the last line is just a convenient shorthand)
# Note however with the last line, you cannot pass in "0.1" or "0.2" as strings.
wiz.res("atom diameter", 42.0, [(0.1, "sys"), (0.2, "stat")])
wiz.res("atom diameter", 42.0, 0.1, 0.2)
```


### Override the rounding mechanism

Sometimes, you don't want a result to be rounded at all. You can tell `ResultWizard` to not round a numerical value by passing this value as string instead:
```py
calculated_uncert = 0.063
wiz.res("abc", "1.2345", str(calculated_uncert)).print()
# will print: abc = 1.2345 ± 0.063
```

You might also use the following keyword arguments with any signature of `wiz.res()`. They will override whatever you have configured via [`config_init()` or `config()`](/api/config), but just for the specific result.
```py
wiz.res(name, ..., sigfigs: int = None, decimal_places: int = None)
```


### Return type

`wiz.res()` returns a `PrintableResult`. On this object, you can call:

```py
my_res = wiz.res("abc", 1.2345, 0.063)
my_res.print()  # will print: abc = 1.23 ± 0.06
my_latex_str = my_res.to_latex_str()
print(my_latex_str)  # will print: \num{1.23 \pm 0.06}
```

- `print()` will print the result to the console. If you find yourself using this a lot, consider setting the [`print_auto` config option](/api/config#print_auto) to `True`, which will automatically print the result after each call to `wiz.res()`.
- `to_latex_str()` converts the result to a LaTeX string. This might be useful if you want to show the result as label in a `matplotlib` plot. For this to work, you have to tell `matplotlib` that you're using `siunitx` by defining the preamble in your Python script:
```py
import matplotlib.pyplot as plt
plt.rc('text.latex', preamble=r"""
       \usepackage{siunitx}
       \sisetup{locale=US, group-separator={,}, group-digits=integer,
              per-mode=symbol, separate-uncertainty=true}""")
```

---

[^1]: For the technically interested: we use [`plum`] to achieve this "multiple dispatch" in Python. Natively, Python does not allow for method overloading, a concept you might know from other programming languages like Java.


[`plum`]: https://github.com/beartype/plum