from typing import Union, List, Tuple
from plum import dispatch, overload

from api.printable_result import PrintableResult
from api.config import configuration
from application.cache import _ResultsCache
from application.rounder import _Rounder
import api.parsers as parsers
from domain.result import _Result


# TODO: import types from typing to ensure backwards compatibility down to Python 3.8

# TODO: use pydantic instead of manual and ugly type checking
# see: https://docs.pydantic.dev/latest/
# This way we can code as if the happy path is the only path, and let pydantic
# handle the error checking and reporting.

_res_cache = _ResultsCache()


@overload
def res(
    name: str,
    value: Union[float, str],
    unit: str = "",
    sigfigs: Union[int, None] = None,
    decimal_places: Union[int, None] = None,
) -> PrintableResult:
    return res(name, value, [], unit, sigfigs, decimal_places)


@overload
def res(
    name: str,
    value: Union[float, str],
    uncert: Union[
        float,
        str,
        Tuple[Union[float, str], str],
        List[Union[float, str, Tuple[Union[float, str], str]]],
        None,
    ] = None,
    sigfigs: Union[int, None] = None,
    decimal_places: Union[int, None] = None,
) -> PrintableResult:
    return res(name, value, uncert, "", sigfigs, decimal_places)


@overload
def res(
    name: str,
    value: Union[float, str],
    sigfigs: Union[int, None] = None,
    decimal_places: Union[int, None] = None,
) -> PrintableResult:
    return res(name, value, [], "", sigfigs, decimal_places)


@overload
def res(
    name: str,
    value: Union[float, str],
    sys: float,
    stat: float,
    unit: str = "",
    sigfigs: Union[int, None] = None,
    decimal_places: Union[int, None] = None,
) -> PrintableResult:
    return res(name, value, [(sys, "sys"), (stat, "stat")], unit, sigfigs, decimal_places)


@overload
def res(
    name: str,
    value: Union[float, str],
    uncert: Union[
        float,
        str,
        Tuple[Union[float, str], str],
        List[Union[float, str, Tuple[Union[float, str], str]]],
        None,
    ] = None,
    unit: str = "",
    sigfigs: Union[int, None] = None,
    decimal_places: Union[int, None] = None,
) -> PrintableResult:
    if uncert is None:
        uncert = []

    # Parse user input
    name_res = parsers.parse_name(name)
    value_res = parsers.parse_value(value)
    uncertainties_res = parsers.parse_uncertainties(uncert)
    unit_res = parsers.parse_unit(unit)
    sigfigs_res = parsers.parse_sigfigs(sigfigs)
    decimal_places_res = parsers.parse_decimal_places(decimal_places)

    # Assemble the result
    result = _Result(
        name_res, value_res, unit_res, uncertainties_res, sigfigs_res, decimal_places_res
    )
    _Rounder.round_result(result, configuration.sigfigs)
    _res_cache.add(name, result)

    return PrintableResult(result)


# Hack for method "overloading" in Python
# see https://beartype.github.io/plum/integration.html
# This is a good writeup: https://stackoverflow.com/a/29091980/
@dispatch
def res(*args, **kwargs) -> object:
    # This method only scans for all `overload`-decorated methods
    # and properly adds them as Plum methods.
    pass
