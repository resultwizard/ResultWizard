from dataclasses import dataclass
from typing import List

from domain.result import _Result
from domain.value import _Value
from domain.uncertainty import _Uncertainty
from application.helpers import _Helpers
from application.latexer_ifelse import LatexIfElseBuilder


@dataclass
class LaTeXConfig:
    min_exponent_for_non_scientific_notation: int
    max_exponent_for_non_scientific_notation: int
    identifier: str


class _LaTeXer:
    """
    Provides methods to convert results to LaTeX commands.

    We assume the result to already be correctly rounded at this point.
    """

    def __init__(self, config: LaTeXConfig):
        self.config = config

    def result_to_latex_cmd(self, result: _Result) -> str:
        """
        Returns the result as LaTeX command to be used in a .tex file.
        """
        builder = LatexIfElseBuilder()

        cmd_name = f"{self.config.identifier}{_Helpers.capitalize(result.name)}"
        latex_str = rf"\newcommand*{{\{cmd_name}}}[1][]{{" + "\n"

        # Default case (full result) & value
        builder.add_branch("", self.result_to_latex_str(result))
        builder.add_branch("value", self.result_to_latex_str_value(result))

        # Without error
        if len(result.uncertainties) > 0:
            builder.add_branch("withoutError", self.result_to_latex_str_without_error(result))

        # Single uncertainties
        for i, u in enumerate(result.uncertainties):
            if len(result.uncertainties) == 1:
                uncertainty_name = "error"
            else:
                uncertainty_name = u.name if u.name != "" else _Helpers.number_to_word(i + 1)
                uncertainty_name = f"error{_Helpers.capitalize(uncertainty_name)}"
            error_latex_str = self._create_latex_str(u.uncertainty, [], result.unit)
            builder.add_branch(uncertainty_name, error_latex_str)

        # Total uncertainty and short result
        if len(result.uncertainties) >= 2:
            short_result = result.get_short_result()
            if short_result is None:
                raise RuntimeError(
                    "Short result is None, but there should be at least two uncertainties."
                )
            error_latex_str = self._create_latex_str(
                short_result.uncertainties[0].uncertainty, [], result.unit
            )
            builder.add_branch("errorTotal", error_latex_str)
            builder.add_branch("short", self.result_to_latex_str(short_result))

        # Unit
        if result.unit != "":
            builder.add_branch("unit", rf"\unit{{{result.unit}}}")

        # Error message
        keywords = builder.keywords
        if len(keywords) > 0:
            error_message = "Please specify one of the following keywords: "
            error_message += ", ".join([rf"\texttt{{{k}}}" for k in keywords])
            error_message += " or don't use any keyword at all."
        else:
            error_message = "This variable can only be used without keywords."
        builder.add_else(rf"\scriptsize{{\textbf{{{error_message}}}}}")

        latex_str += builder.build()
        latex_str += "\n}"

        return latex_str

    def result_to_latex_str(self, result: _Result) -> str:
        """
        Returns the result as LaTeX string making use of the siunitx package.
        """
        return self._create_latex_str(result.value, result.uncertainties, result.unit)

    def result_to_latex_str_value(self, result: _Result) -> str:
        """
        Returns only the value as LaTeX string making use of the siunitx package.
        """
        return self._create_latex_str(result.value, [], "")

    def result_to_latex_str_without_error(self, result: _Result) -> str:
        """
        Returns the result without error as LaTeX string making use of the siunitx package.
        """
        return self._create_latex_str(result.value, [], result.unit)

    def _create_latex_str(self, value: _Value, uncertainties: List[_Uncertainty], unit: str) -> str:
        """
        Returns the result as LaTeX string making use of the siunitx package.

        This string does not yet contain "\newcommand*{}".
        """
        latex_str = ""

        use_scientific_notation = self._should_use_scientific_notation(value, uncertainties)
        has_unit = unit != ""
        should_use_parentheses = len(uncertainties) > 0 and (use_scientific_notation or has_unit)

        sign = "-" if value.get() < 0 else ""
        exponent = value.get_exponent()
        factor = 10 ** (-exponent) if use_scientific_notation else 1.0
        value_normalized = value.get_abs() * factor
        decimal_places = (
            value.get_sig_figs() - 1 if use_scientific_notation else value.get_decimal_place()
        )

        if should_use_parentheses:
            latex_str += r"\left("
        latex_str += sign
        latex_str += _Helpers.round_to_n_decimal_places(value_normalized, decimal_places)

        for u in uncertainties:
            uncertainty_normalized = u.uncertainty.get_abs() * factor
            decimal_places = (
                exponent - u.uncertainty.get_min_exponent()
                if use_scientific_notation
                else u.uncertainty.get_decimal_place()
            )
            latex_str += r" \pm "
            latex_str += _Helpers.round_to_n_decimal_places(uncertainty_normalized, decimal_places)
            if len(uncertainties) > 1:
                latex_str += rf"_{{\text{{{u.name}}}}}"

        if should_use_parentheses:
            latex_str += r"\right)"
        if use_scientific_notation:
            latex_str += rf" \cdot 10^{{{exponent}}}"
        if has_unit:
            latex_str += rf"\, \unit{{{unit}}}"

        return latex_str

    def _should_use_scientific_notation(
        self, value: _Value, uncertainties: List[_Uncertainty]
    ) -> bool:
        """
        Returns whether scientific notation should be used for the given value and uncertainties.
        """
        exponent = value.get_exponent()
        if (
            exponent < self.config.min_exponent_for_non_scientific_notation
            or exponent > self.config.max_exponent_for_non_scientific_notation
        ):
            return True

        if value.get_min_exponent() > 0:
            return True

        for u in uncertainties:
            if u.uncertainty.get_min_exponent() > 0:
                return True

        return False
