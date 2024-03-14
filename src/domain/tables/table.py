from dataclasses import dataclass
from typing import List

from domain.tables.column import _Column


@dataclass
class _Table:
    """
    A table.
    """

    name: str
    columns: List[_Column]
    caption: str
    resize_to_fit_page: bool
    horizontal: bool
    concentrate_units_if_possible: bool