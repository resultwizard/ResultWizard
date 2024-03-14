from dataclasses import dataclass
from typing import Union, List

from domain.result import _Result


@dataclass
class _Column:
    """
    A table column.
    """

    title: str
    cells: List[Union[_Result, str]]
