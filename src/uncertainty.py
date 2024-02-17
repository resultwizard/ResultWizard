from value import Value


class _Uncertainty:
    def __init__(self, uncertainty: float | str, name: str):
        if not isinstance(uncertainty, (float, str)):
            raise TypeError(f"`uncertainty` must be a float or string, not {type(uncertainty)}")
        if not isinstance(name, str):
            raise TypeError(f"`name` must be a string, not {type(name)}")

        self.uncertainty = Value(uncertainty)
        self.name = name

    def __str__(self):
        if self.name == "":
            return f"{self.uncertainty.extract()}"
        return f"{self.uncertainty.extract()} ({self.name})"
