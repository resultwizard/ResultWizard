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
    unit: str

    def __init__(self, title: str, cells: List[Union[_Result, str]]):
        self.title = title
        self.cells = cells
        self.unit = ""

    def concentrate_units(self):
        """
        Concentrates the units of the cells in this column if possible.
        """

        unit = None
        should_concentrate_units = True

        for cell in self.cells:
            if isinstance(cell, _Result):
                if unit is None:
                    unit = cell.unit
                elif unit != cell.unit:
                    should_concentrate_units = False
                    break
            else:
                should_concentrate_units = False
                break

        if should_concentrate_units and unit is not None:
            self.unit = unit
