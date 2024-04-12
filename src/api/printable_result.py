from api.console_stringifier import ConsoleStringifier
import api.config as c
from api.latexer import get_latexer
from domain.result import Result


class PrintableResult:
    def __init__(self, result: Result):
        self._result = result
        self.has_printed = False

    def print(self):
        """Prints the result to the console."""
        if not self.has_printed:
            stringifier = ConsoleStringifier(c.configuration.to_stringifier_config())
            print(stringifier.result_to_str(self._result))
            self.has_printed = True

    def to_latex_str(self) -> str:
        """Converts the result to a string that can be used in LaTeX documents.

        Note that you might also want to use the `export` method to export
        all your results to a file, which can then be included in your LaTeX
        document.
        """
        latexer = get_latexer()
        return latexer.result_to_latex_str(self._result)
