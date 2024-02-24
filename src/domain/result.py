from domain.uncertainty import _Uncertainty
from domain.value import _Value


class _Result:
    """
    A general-purpose result, i.e. a value that was somehow measured or calculated,
    along with a unit and optional uncertainties.
    """

    def __init__(self, name, value: _Value, unit: str, uncertainties: list[_Uncertainty] = []):
        self.name = name
        self.value = value
        self.uncertainties = uncertainties
        self.unit = unit

    # def print(self):
    #     uncertainties_str = ", ".join([str(u) for u in self.uncertainties])
    #     print(f"{self.name}: {self.value.extract()} ± {uncertainties_str} {self.unit}")

    def __str__(self):
        uncertainties_str = ", ".join([str(u) for u in self.uncertainties])
        return f"{self.name}: ({self.value.extract()} ± {uncertainties_str}) {self.unit}"
