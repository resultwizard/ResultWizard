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
    concentrate_units_if_possible: Union[bool, None]

    def __init__(
        self,
        title: str,
        cells: List[Union[_Result, str]],
        concentrate_units_if_possible: Union[bool, None] = None,
    ):
        """
        Init method.

        The parameter `concentrate_units_if_possible` is `None` by default and only overwrites the
        master setting from the table object if it is manually set to `True` or `False`.
        """
        self.title = title
        self.cells = cells
        self.unit = ""
        self.concentrate_units_if_possible = concentrate_units_if_possible

    def concentrate_units(self, concentrate_units_if_possible_master: bool):
        """
        Concentrates the units of the cells in this column if possible and if desired.
        """

        # Check if concentration of units is desired:
        if self.concentrate_units_if_possible is not None:
            should_concentrate_units = self.concentrate_units_if_possible
        else:
            should_concentrate_units = concentrate_units_if_possible_master

        # Check if concentration of units is possible given the cell values:
        unit = None
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
