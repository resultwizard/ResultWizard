class Value:
    def __init__(self, value: float | str):
        self.value = value
        self.is_exact = isinstance(value, str)

    def extract(self) -> float:
        return self.value
