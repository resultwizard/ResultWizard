from typing import List, Union

from domain.tables.column import _Column
from domain.result import _Result


def column(
    title: str,
    cells: List[Union[_Result, str]],
) -> _Column:
    return _Column(title, cells)