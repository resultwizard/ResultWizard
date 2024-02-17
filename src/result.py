class PrintableResult:
    def __init__(self, formatstring):
        self._formatstring = formatstring

    def print(self):
        print(self._formatstring)


class _Result:
    def __init__(self, name, value, uncertainty, unit):
        self.name = name
        self.value = value
        self.error = uncertainty
        self.unit = unit

    def to_printable(self) -> PrintableResult:
        return PrintableResult(f"{self.name}: {self.value} ± {self.error} {self.unit}")
