from decimal import Decimal
from typing import Union, List, Tuple

from domain.result import Result
from api.res import _res


def table_res(
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
) -> Result:
    """
    Declares your result. Give it a name and a value. You may also optionally provide
    uncertainties (via `uncert` or `sys`/`stat`) and a unit in `siunitx` format.

    You may additionally specify the number of significant figures or decimal places
    to round this specific result to, irrespective of your global configuration.

    TODO: provide a link to the docs for more information and examples.
    """
    _, result = _res(None, value, uncerts, unit, sys, stat, sigfigs, decimal_places)

    return result
