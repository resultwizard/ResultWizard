from domain.uncertainty import _Uncertainty
from domain.value import _Value

from dataclasses import dataclass
from typing import Union


@dataclass
class _Result:
    """
    A general-purpose result, i.e. a value that was somehow measured or calculated,
    along with a unit and optional uncertainties (list might be empty).
    """

    name: str
    value: _Value
    unit: Union[str, None]
    uncertainties: list[_Uncertainty]
    sigfigs: Union[int, None]
    decimal_places: Union[int, None]

    def __str__(self):
        # TODO: Do it properly.
        if len(self.uncertainties) == 0:
            return f"{self.name}: {self.value.extract()} {self.unit}"

        uncertainties_str = " ± ".join([str(u) for u in self.uncertainties])
        return f"{self.name}: ({self.value.extract()} ± {uncertainties_str}) {self.unit}"
