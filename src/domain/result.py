from dataclasses import dataclass, field
from typing import Union
from copy import copy
from decimal import Decimal

from domain.uncertainty import Uncertainty
from domain.value import Value


@dataclass
class Result:
    """
    A general-purpose result, i.e. a value that was somehow measured or calculated,
    along with a unit and optional uncertainties (list might be empty).
    """

    name: str
    value: Value
    unit: str
    uncertainties: list[Uncertainty]
    sigfigs: Union[int, None]
    decimal_places: Union[int, None]

    total_uncertainty: Union[Uncertainty, None] = field(init=False)

    def __post_init__(self):
        if len(self.uncertainties) >= 2:
            self.total_uncertainty = self._calculate_total_uncertainty()
        else:
            self.total_uncertainty = None

    def _calculate_total_uncertainty(self) -> Uncertainty:
        total = Decimal("0")
        for u in self.uncertainties:
            total += u.uncertainty.get() ** 2
        return Uncertainty(Value(total.sqrt()))

    def get_short_result(self) -> Union["Result", None]:
        if self.total_uncertainty is None:
            return None

        return Result(
            self.name,
            copy(self.value),
            self.unit,
            [copy(self.total_uncertainty)],
            self.sigfigs,
            self.decimal_places,
        )
