## Documentation

**Things we should include in the documentation:**

- an overview of what the goal of the project is with a small illustration where we sketch python code, the `results.tex` file and the LaTeX document and explain how they are connected
- most common ways to use the library, but then also a comprehensive list of all possible ways to call `res` (preferable on a separate page of the documentation). How to guides for most common cases
- ways to use the variable in LaTeX code, e.g. list all keys, tell users they should enter \resMyVariable[test] and then see the error message to find out what the possible keys are
- passing in as string means exact value
- how to specify the name of a variable. Numbers only allowed from 0 up to 1000. Special characters are stripped. Explain camel case etc.
-> Explain that this has the great potential for loops: users can specify variables in a loop and use format strings, e.g. `wiz.res(f"my_variable_{i}", ...)`
- how to pass in uncertainties. How to pass in one? What about systematic and statistical ones. What if I want to add my own name for the uncertainty? How can I control that output.
- a list of all possible keys for `config_init` including their default values, e.g. `identifier`. In-depth explanation especially for sigfigs and decimal places and how they differ from respective fallback options
- a hint that the output is completely customizable and that the user can change it with the `\sisetup{...}`, e.g. `\cdot` vs. `\times` for exponent, `separate-uncertainty=true` (!)
- how to use the unit string. explain that strings from `siunitx` can be passed in, e.g. `\cm \per \N` etc. Explain how python raw strings can help, e.g. `r"\cm \per \N"` instead of having to do `\\cm` etc. all the time. However, `r'\\tesla'` will fail as the double backslash is treated a raw string and not as an escape character. Use `r'\tesla'` instead.
- possible ways to print a result. Recommended: activate `print_auto`. Other way: call `print()` on result object. Users can also call `resVariable.to_latex_str()` to retrieve the LaTeX representation. This can be useful to plot the result in a matplotlib figure, e.g. the fit parameter of a curve fit.
- Suggest some good initial configuration for Jupyter notebook, e.g. `print_auto=True` and `ignore_result_overwrite=True`.
- Naming: we call it "uncertainty". Give a hint that others might also call it "error" interchangeably.
- Jupyter Notebook tip to avoid
- Add warning that users should not rely on console stringified output for further processing since that might change more often in the future, e.g. better formatting of units or whitespaces etc. Only rely on the final LaTeX output written to the external file.


```
<api.printable_result.PrintableResult at 0x7f35beb20510>
```
as output. Instead append a `;` to the `wiz.res(...)` call and the output will be suppressed.

- Use fuzzy search in IntelliSense to search for result names.



## Other

- Setup issue template and contribution guide. Clean up `DEVELOPMENT.md`.
- Long-term: Ask real users what they really need in the scientific day-to-day life, see [here](https://github.com/resultwizard/ResultWizard/issues/9).
- If user enters an uncertainty of `0.0`, don't just issue warning "Uncertainty must be positive", but also give a hint that the user might want to use a different caller syntax for `res` which does not even have the uncertainty as argument.
