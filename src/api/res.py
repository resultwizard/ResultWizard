from decimal import Decimal
from typing import Union, List, Tuple

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


# pylint: disable-next=too-many-arguments, too-many-locals
def res(
    name: str,
    value: Union[float, int, str, Decimal],
    uncerts: Union[
        float,
        int,
        str,
        Decimal,
        Tuple[Union[float, int, str, Decimal], str],
        List[Union[float, int, str, Decimal, Tuple[Union[float, int, str, Decimal], str]]],
        None,
    ] = None,
    unit: str = "",
    sys: Union[float, int, str, Decimal, None] = None,
    stat: Union[float, int, str, Decimal, None] = None,
    sigfigs: Union[int, None] = None,
    decimal_places: Union[int, None] = None,
) -> PrintableResult:
    """
    Declares your result. Give it a name and a value. You may also optionally provide
    uncertainties (via `uncert` or `sys`/`stat`) and a unit in `siunitx` format.

    You may additionally specify the number of significant figures or decimal places
    to round this specific result to, irrespective of your global configuration.

    TODO: provide a link to the docs for more information and examples.
    """
    # Verify user input
    if sigfigs is not None and decimal_places is not None:
        raise ValueError(error_messages.SIGFIGS_AND_DECIMAL_PLACES_AT_SAME_TIME)

    if sigfigs is not None and isinstance(value, str):
        raise ValueError(error_messages.SIGFIGS_AND_EXACT_VALUE_AT_SAME_TIME)

    if decimal_places is not None and isinstance(value, str):
        raise ValueError(error_messages.DECIMAL_PLACES_AND_EXACT_VALUE_AT_SAME_TIME)

    sys_or_stat_specified = sys is not None or stat is not None
    if uncerts is not None and sys_or_stat_specified:
        raise ValueError(error_messages.UNCERT_AND_SYS_STAT_AT_SAME_TIME)

    if sys_or_stat_specified:
        uncerts = []
        if sys is not None:
            uncerts.append((sys, "sys"))
        if stat is not None:
            uncerts.append((stat, "stat"))

    if uncerts is None:
        uncerts = []

    # Parse user input
    name_res = parsers.parse_name(name)
    value_res = parsers.parse_value(value)
    uncertainties_res = parsers.parse_uncertainties(uncerts)
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
