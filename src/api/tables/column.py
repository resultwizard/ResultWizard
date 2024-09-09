from typing import List, Union

from domain.tables.column import Column
from domain.result import Result


def column(
    title: str,
    cells: List[Union[Result, str]],
    concentrate_units_if_possible: Union[bool, None] = None,
) -> Column:
    return Column(title, cells, concentrate_units_if_possible)
