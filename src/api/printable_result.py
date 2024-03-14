from api.stringifier import Stringifier
from api.config import configuration
from application.latexer import _LaTeXer
from domain.result import _Result


class PrintableResult:
    def __init__(self, result: _Result):
        self._result = result

    def print(self):
        """Prints the result to the console."""
        print(Stringifier.result_to_str(self._result))

    def get_latex_str(self) -> str:
        """Returns LaTeX string."""
        latexer = _LaTeXer(configuration.to_latex_config())
        return latexer.result_to_latex_str(self._result)
