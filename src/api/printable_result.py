from domain.result import _Result
from api.stringifier import Stringifier


class PrintableResult:
    def __init__(self, result: _Result):
        self._result = result

    def print(self):
        """Prints the result to the console."""
        print(Stringifier.result_to_str(self._result))
