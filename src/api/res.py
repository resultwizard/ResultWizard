from typing import Union, List, Tuple
from plum import dispatch, overload

from api.printable_result import PrintableResult
from api import parsers
import api.config as c
from application.cache import ResultsCache
from application.rounder import Rounder
from domain.result import Result

_res_cache = ResultsCache()

# "Wrong" import position to avoid circular imports (export needs the _res_cache)
from api.export import _export  # pylint: disable=wrong-import-position,ungrouped-imports


@overload
def res(
    name: str,
    value: Union[float, int, str],
    unit: str = "",
    sigfigs: Union[int, None] = None,
    decimal_places: Union[int, None] = None,
) -> PrintableResult:
    return res(name, value, [], unit, sigfigs, decimal_places)


@overload
def res(
    name: str,
    value: Union[float, int, str],
    uncert: Union[
        float,
        str,
        Tuple[Union[float, int, str], str],
        List[Union[float, int, str, Tuple[Union[float, int, str], str]]],
        None,
    ] = None,
    sigfigs: Union[int, None] = None,
    decimal_places: Union[int, None] = None,
) -> PrintableResult:
    return res(name, value, uncert, "", sigfigs, decimal_places)


@overload
def res(
    name: str,
    value: Union[float, int, str],
    sigfigs: Union[int, None] = None,
    decimal_places: Union[int, None] = None,
) -> PrintableResult:
    return res(name, value, [], "", sigfigs, decimal_places)


@overload
# pylint: disable=too-many-arguments
def res(
    name: str,
    value: Union[float, int, str],
    sys: float,
    stat: float,
    unit: str = "",
    sigfigs: Union[int, None] = None,
    decimal_places: Union[int, None] = None,
) -> PrintableResult:
    return res(name, value, [(sys, "sys"), (stat, "stat")], unit, sigfigs, decimal_places)


@overload
# pylint: disable=too-many-arguments
def res(
    name: str,
    value: Union[float, int, str],
    uncert: Union[
        float,
        str,
        Tuple[Union[float, int, str], str],
        List[Union[float, int, str, Tuple[Union[float, int, str], str]]],
        None,
    ] = None,
    unit: str = "",
    sigfigs: Union[int, None] = None,
    decimal_places: Union[int, None] = None,
) -> PrintableResult:
    if uncert is None:
        uncert = []

    if sigfigs is not None and decimal_places is not None:
        raise ValueError(
            "You can't set both sigfigs and decimal places at the same time. "
            "Please choose one or the other."
        )

    if sigfigs is not None and isinstance(value, str):
        raise ValueError(
            "You can't set sigfigs and supply an exact value. Please do one or the other."
        )

    if decimal_places is not None and isinstance(value, str):
        raise ValueError(
            "You can't set decimal places and supply an exact value. Please do one or the other."
        )

    # Parse user input
    name_res = parsers.parse_name(name)
    value_res = parsers.parse_value(value)
    uncertainties_res = parsers.parse_uncertainties(uncert)
    unit_res = parsers.parse_unit(unit)
    sigfigs_res = parsers.parse_sigfigs(sigfigs)
    decimal_places_res = parsers.parse_decimal_places(decimal_places)

    # Assemble the result
    result = Result(
        name_res, value_res, unit_res, uncertainties_res, sigfigs_res, decimal_places_res
    )
    Rounder.round_result(result, c.configuration.to_rounding_config())
    _res_cache.add(name_res, result)

    # Print automatically
    printable_result = PrintableResult(result)
    if c.configuration.print_auto:
        printable_result.print()

    # Export automatically
    immediate_export_path = c.configuration.export_auto_to
    if immediate_export_path != "":
        _export(immediate_export_path, print_completed=False)

    return printable_result


# Hack for method "overloading" in Python
# see https://beartype.github.io/plum/integration.html
# This is a good writeup: https://stackoverflow.com/a/29091980/
@dispatch
def res(*args, **kwargs) -> object:  # pylint: disable=unused-argument
    # This method only scans for all `overload`-decorated methods
    # and properly adds them as Plum methods.
    pass
