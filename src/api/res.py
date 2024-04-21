from decimal import Decimal
from typing import Union, List, Tuple
from plum import dispatch, overload

from api.printable_result import PrintableResult
from api import parsers
from application.cache import ResultsCache
from application.rounder import Rounder
from application import error_messages
from domain.result import Result

_res_cache = ResultsCache()

# "Wrong" import position to avoid circular imports
from api.export import _export  # pylint: disable=wrong-import-position,ungrouped-imports
import api.config as c  # pylint: disable=wrong-import-position,ungrouped-imports


@overload
def res(
    name: str,
    value: Union[float, int, str, Decimal],
    unit: str = "",
    sigfigs: Union[int, None] = None,
    decimal_places: Union[int, None] = None,
) -> PrintableResult:
    return res(name, value, [], unit, sigfigs, decimal_places)


@overload
def res(
    name: str,
    value: Union[float, int, str, Decimal],
    uncert: Union[
        float,
        str,
        Decimal,
        Tuple[Union[float, int, str, Decimal], str],
        List[Union[float, int, str, Decimal, Tuple[Union[float, int, str, Decimal], str]]],
        None,
    ] = None,
    sigfigs: Union[int, None] = None,
    decimal_places: Union[int, None] = None,
) -> PrintableResult:
    return res(name, value, uncert, "", sigfigs, decimal_places)


@overload
def res(
    name: str,
    value: Union[float, int, str, Decimal],
    sigfigs: Union[int, None] = None,
    decimal_places: Union[int, None] = None,
) -> PrintableResult:
    return res(name, value, [], "", sigfigs, decimal_places)


@overload
# pylint: disable=too-many-arguments
def res(
    name: str,
    value: Union[float, int, str, Decimal],
    sys: Union[float, Decimal],
    stat: Union[float, Decimal],
    unit: str = "",
    sigfigs: Union[int, None] = None,
    decimal_places: Union[int, None] = None,
) -> PrintableResult:
    return res(name, value, [(sys, "sys"), (stat, "stat")], unit, sigfigs, decimal_places)


@overload
# pylint: disable=too-many-arguments,redefined-builtin,too-many-locals
def res(
    name: str,
    value: Union[float, int, str, Decimal],
    uncert: Union[
        float,
        str,
        Decimal,
        Tuple[Union[float, int, str, Decimal], str],
        List[Union[float, int, str, Decimal, Tuple[Union[float, int, str, Decimal], str]]],
        None,
    ] = None,
    unit: str = "",
    sigfigs: Union[int, None] = None,
    decimal_places: Union[int, None] = None,
    print: Union[bool, None] = None,
) -> PrintableResult:
    if uncert is None:
        uncert = []

    if sigfigs is not None and decimal_places is not None:
        raise ValueError(error_messages.SIGFIGS_AND_DECIMAL_PLACES_AT_SAME_TIME)

    if sigfigs is not None and isinstance(value, str):
        raise ValueError(error_messages.SIGFIGS_AND_EXACT_VALUE_AT_SAME_TIME)

    if decimal_places is not None and isinstance(value, str):
        raise ValueError(error_messages.DECIMAL_PLACES_AND_EXACT_VALUE_AT_SAME_TIME)

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
    if (c.configuration.print_auto and print is not False) or print is True:
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
