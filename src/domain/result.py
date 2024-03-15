from dataclasses import dataclass, field
from typing import Union
from copy import copy

from domain.uncertainty import _Uncertainty
from domain.value import _Value


@dataclass
class _Result:
    """
    A general-purpose result, i.e. a value that was somehow measured or calculated,
    along with a unit and optional uncertainties (list might be empty).
    """

    name: str
    value: _Value
    unit: str
    uncertainties: list[_Uncertainty]
    sigfigs: Union[int, None]
    decimal_places: Union[int, None]

    total_uncertainty: Union[_Uncertainty, None] = field(init=False)

    def __post_init__(self):
        if len(self.uncertainties) > 1:
            self.total_uncertainty = self._calculate_total_uncertainty()
        else:
            self.total_uncertainty = None

    def _calculate_total_uncertainty(self) -> _Uncertainty:
        total = 0
        for u in self.uncertainties:
            total += u.uncertainty.get() ** 2
        return _Uncertainty(total**0.5)

    def get_short_result(self) -> Union["_Result", None]:
        if self.total_uncertainty is None:
            return None

        return _Result(
            self.name,
            copy(self.value),
            self.unit,
            [copy(self.total_uncertainty)],
            self.sigfigs,
            self.decimal_places,
        )
