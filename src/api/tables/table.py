from typing import List

from application.cache import _res_cache
import application.parsers as parsers
from domain.tables.column import _Column
from domain.tables.table import _Table


def table(
    name: str,
    columns: List[_Column],
    caption: str,
    resize_to_fit_page_: bool = False,
    horizontal: bool = False,
    concentrate_units_if_possible: bool = True,
):
    # Parse user input
    name_res = parsers.parse_name(name)

    # Assemble the table
    _table = _Table(
        name_res, columns, caption, resize_to_fit_page_, horizontal, concentrate_units_if_possible
    )
    _res_cache.add_table(name, _table)

    return
