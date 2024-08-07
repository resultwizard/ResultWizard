from api.console_stringifier import ConsoleStringifier
import api.config as c
from api.latexer import get_latexer
from domain.result import Result
from application import error_messages


class PrintableResult:
    def __init__(self, result: Result):
        self._result = result

    def print(self):
        """Prints the result to the console."""
        stringifier = ConsoleStringifier(c.configuration.to_stringifier_config())
        print(stringifier.result_to_str(self._result))

    def get_str(self) -> str:
        stringifier = ConsoleStringifier(c.configuration.to_stringifier_config())
        return stringifier.create_str(self._result)

    def get_str_value(self) -> str:
        stringifier = ConsoleStringifier(c.configuration.to_stringifier_config())
        return stringifier.create_str_value(self._result)

    def get_str_without_uncert(self) -> str:
        stringifier = ConsoleStringifier(c.configuration.to_stringifier_config())
        return stringifier.create_str_without_uncert(self._result)

    def get_uncerts(self) -> list[dict[str, str]]:
        stringifier = ConsoleStringifier(c.configuration.to_stringifier_config())
        return [
            {
                "name": u.name,
                "string": stringifier.create_str_uncert(u, self._result.unit),
            }
            for u in self._result.uncertainties
        ]

    def get_str_uncert_total(self) -> str:
        stringifier = ConsoleStringifier(c.configuration.to_stringifier_config())
        short_result = self._result.get_short_result()
        if short_result is None:
            raise RuntimeError(error_messages.SHORT_RESULT_IS_NONE)
        return stringifier.create_str_uncert(short_result.uncertainties[0], self._result.unit)

    def get_str_short(self) -> str:
        stringifier = ConsoleStringifier(c.configuration.to_stringifier_config())
        short_result = self._result.get_short_result()
        if short_result is None:
            raise RuntimeError(error_messages.SHORT_RESULT_IS_NONE)
        return stringifier.create_str(short_result)

    def get_str_without_unit(self) -> str:
        stringifier = ConsoleStringifier(c.configuration.to_stringifier_config())
        return stringifier.create_str_without_unit(self._result)

    def to_latex_str(self) -> str:
        """Converts the result to a string that can be used in LaTeX documents.

        Note that you might also want to use the `export` method to export
        all your results to a file, which can then be included in your LaTeX
        document.
        """
        latexer = get_latexer()
        return latexer.result_to_latex_str(self._result)
