from api.printable_result import PrintableResult
from application.cache import _res_cache
from domain.result import _Result
from domain.value import _Value
from domain.uncertainty import _Uncertainty


def res(name: str, value: float | str, unit: str, uncert=[]) -> PrintableResult:
    # Parse user input
    name_res = _parse_name(name)
    value_res = _parse_value(value)
    uncertainties_res = _parse_uncertainties(uncert)
    unit_res = _parse_unit(unit)

    # Assemble the result
    result = _Result(name_res, value_res, unit_res, uncertainties_res)
    _res_cache.add(name, result)

    return PrintableResult(result)


def _is_exact(value: float | str) -> bool:
    """Returns True if the value is a str, False otherwise.

    This is just a choice of how we let the user specify whether their value
    should be treated as exact (no significant figures rounding) or inexact.
    Therefore, this belongs to the public API and *not* to the domain.
    """
    return isinstance(value, str)


def _check_if_number_string(value: str) -> None:
    """Raises a ValueError if the string is not a valid number."""
    try:
        float(value)
    except ValueError:
        raise ValueError(f"String value must be a valid number, not {value}")


def _parse_name(name: str) -> str:
    """Parses the name."""
    if not isinstance(name, str):
        raise TypeError(f"`name` must be a string, not {type(name)}")
    return name


def _parse_unit(unit: str) -> str:
    """Parses the unit."""
    if not isinstance(unit, str):
        raise TypeError(f"`unit` must be a string, not {type(unit)}")

    # TODO: maybe add some basic checks to catch siunitx errors, e.g.
    # unsupported symbols etc. But maybe leave this to LaTeX and just return
    # the LaTeX later on. But catching it here would be more user-friendly,
    # as the user would get immediate feedback and not only once they try to
    # export the results.
    return unit


def _parse_value(value: float | str) -> _Value:
    """Converts the value to a _Value object."""
    if not isinstance(value, (float, str)):
        raise TypeError(f"`value` must be a float or string, not {type(value)}")

    if isinstance(value, str):
        _check_if_number_string(value)

    return _Value(str(value), _is_exact(value))


def _parse_uncertainties(uncertainties) -> list[_Uncertainty]:
    """Converts the uncertainties to a list of _Uncertainty objects."""
    uncertainties_res = []

    for uncert in uncertainties:
        if isinstance(uncert, (float, str)):
            if isinstance(uncert, str):
                _check_if_number_string(uncert)
            uncertainties_res.append(_Uncertainty(str(uncert), _is_exact(uncert)))
        elif isinstance(uncert, tuple):
            if not isinstance(uncert[0], (float, str)):
                raise TypeError(
                    f"First argument of uncertainty-tuple must be a string, not {type(uncert[0])}"
                )
            if isinstance(uncert[0], str):
                _check_if_number_string(uncert[0])
            uncertainties_res.append(_Uncertainty(str(uncert[0]), _is_exact(uncert[0]), uncert[1]))

        else:
            raise TypeError(f"Each uncertainty must be a tuple OR a float/str, not {type(uncert)}")

    return uncertainties_res
