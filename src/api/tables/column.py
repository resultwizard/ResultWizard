from typing import List, Union

from domain.tables.column import _Column
from domain.result import _Result


def column(
    title: str,
    cells: List[Union[_Result, str]],
    concentrate_units_if_possible: Union[bool, None] = None,
) -> _Column:
    return _Column(title, cells, concentrate_units_if_possible)
