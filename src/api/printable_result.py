from domain.result import _Result
from api.stringifier import Stringifier
from application.latexer import _LaTeXer


class PrintableResult:
    def __init__(self, result: _Result):
        self._result = result

    def print(self):
        """Prints the result to the console."""
        print(Stringifier.result_to_str(self._result))

    def get_latex_str(self) -> str:
        """Returns LaTeX string."""
        return _LaTeXer.result_to_latex_str(self._result)
