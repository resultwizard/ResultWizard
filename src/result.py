from uncertainty import _Uncertainty
from value import Value


class PrintableResult:
    def __init__(self, result):
        self._result = result

    def print(self):
        self._result.print()


class _Result:
    def __init__(self, name, value: Value, unit, uncertainties: list[_Uncertainty] = []):
        self.name = name
        self.value = value
        self.uncertainties = uncertainties
        self.unit = unit

    def to_printable(self) -> PrintableResult:
        return PrintableResult(self)

    def print(self):
        uncertainties_str = ", ".join([str(u) for u in self.uncertainties])
        print(f"{self.name}: {self.value.extract()} ± {uncertainties_str} {self.unit}")
