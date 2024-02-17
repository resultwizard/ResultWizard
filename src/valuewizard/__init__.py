from result import _Result, PrintableResult
from cache import _ResultsCache
from value import Value
from uncertainty import _Uncertainty

_res_cache = _ResultsCache()

# Public facing API


def res(name: str, value: float | str, *args) -> PrintableResult:
    # Type checks
    if not isinstance(name, str):
        raise TypeError(f"`name` must be a string, not {type(name)}")
    if not isinstance(value, (float, str)):
        raise TypeError(f"`value` must be a float or string, not {type(value)}")
    if len(args) == 0:
        raise ValueError("You must provide a unit as last argument")
    if not isinstance(args[-1], str):
        raise TypeError(f"Last argument must be a unit string, not {type(args[0])}")

    # Main value
    value = Value(value)

    # Uncertainties
    uncertainties = []
    for uncert in args[:-1]:
        if not isinstance(uncert, tuple) and not isinstance(uncert, (float, str)):
            raise TypeError(f"Uncertainties must be a tuple OR a float/str, not {type(uncert)}")

        if isinstance(uncert, tuple):
            uncertainties.append(_Uncertainty(*uncert))
        else:
            uncertainties.append(_Uncertainty(uncert, ""))

    # Unit
    unit = args[-1]

    # Create result
    result = _Result(name, value, unit, uncertainties)
    _res_cache.add(name, result)

    return result.to_printable()


def export(filepath):
    print()
    print(f"Exporting to .tex file at {filepath}")
    all_results = _res_cache.get_all_results()
    for _, result in all_results:
        result.print()
