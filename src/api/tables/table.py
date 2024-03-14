from typing import List

from application.cache import _res_cache
import api.parsers as parsers
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

    # Check if columns are valid:
    if len(columns) == 0:
        raise ValueError("A table must have at least one column.")

    length = None
    for column in columns:
        if length is None:
            length = len(column.cells)
        elif length != len(column.cells):
            raise ValueError("All columns must have the same number of cells.")

    if length == 0:
        raise ValueError("All columns must have at least one cell.")

    # Concentrate units:
    if concentrate_units_if_possible:
        for column in columns:
            column.concentrate_units()

    # Assemble the table
    _table = _Table(
        name_res, columns, caption, resize_to_fit_page_, horizontal, concentrate_units_if_possible
    )
    _res_cache.add_table(name, _table)

    return
