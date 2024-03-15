from api.stringifier import Stringifier
import api.config as c
from application.latexer import _LaTeXer
from domain.result import _Result


class PrintableResult:
    def __init__(self, result: _Result):
        self._result = result

    def print(self):
        """Prints the result to the console."""
        print(Stringifier(c.configuration.to_stringifier_config()).result_to_str(self._result))

    def to_latex_str(self) -> str:
        """Converts the result to a string that can be used in LaTeX documents.

        Note that you might also want to use the `export` method to export
        all your results to a file, which can then be included in your LaTeX
        document.
        """
        latexer = _LaTeXer(c.configuration.to_stringifier_config())
        return latexer.result_to_latex_str(self._result)
