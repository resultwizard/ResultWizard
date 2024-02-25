from api.printable_result import PrintableResult
from application.cache import _res_cache
from domain.result import _Result
from domain.value import _Value
from domain.uncertainty import _Uncertainty

from plum import dispatch, overload
from typing import Tuple


# TODO: import types from typing to ensure backwards compatibility down to Python 3.8

# TODO: use pydantic instead of manual and ugly type checking
# see: https://docs.pydantic.dev/latest/
# This way we can code as if the happy path is the only path, and let pydantic
# handle the error checking and reporting.


@overload
def res(name: str, value: float | str, unit: str) -> PrintableResult:
    return res(name, value, [], unit)


@overload
def res(
    name: str,
    value: float | str,
    uncert: float | str | Tuple[float | str, str] | list[float | str | Tuple[float | str, str]],
    unit: str,
) -> PrintableResult:
    # Parse user input
    name_res = _parse_name(name)
    value_res = _parse_value(value)
    uncertainties_res = _parse_uncertainties(uncert)
    unit_res = _parse_unit(unit)

    # Assemble the result
    result = _Result(name_res, value_res, unit_res, uncertainties_res)
    _res_cache.add(name, result)

    return PrintableResult(result)


# Hack for method "overloading" in Python
# see https://beartype.github.io/plum/integration.html
# This is a good writeup: https://stackoverflow.com/a/29091980/
@dispatch
def res(*args, **kwargs) -> object:
    # Final method without an implementation. This scans for all `overload`-decorated
    # methods and properly adds them as Plum methods.
    pass


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


def _parse_uncertainties(
    uncertainties: (
        float | str | Tuple[float | str, str] | list[float | str | Tuple[float | str, str]]
    )
) -> list[_Uncertainty]:
    """Converts the uncertainties to a list of _Uncertainty objects."""
    uncertainties_res = []

    if isinstance(uncertainties, (float, str, Tuple)):
        uncertainties = [uncertainties]

    for uncert in uncertainties:
        if isinstance(uncert, (float, str)):
            if isinstance(uncert, str):
                _check_if_number_string(uncert)
            uncertainties_res.append(_Uncertainty(str(uncert), _is_exact(uncert)))

        elif isinstance(uncert, Tuple):
            if not isinstance(uncert[0], (float, str)):
                raise TypeError(
                    f"First argument of uncertainty-tuple must be a float or a string, not {type(uncert[0])}"
                )
            if isinstance(uncert[0], str):
                _check_if_number_string(uncert[0])
            uncertainties_res.append(_Uncertainty(str(uncert[0]), _is_exact(uncert[0]), uncert[1]))

        else:
            raise TypeError(f"Each uncertainty must be a tuple or a float/str, not {type(uncert)}")

    return uncertainties_res
