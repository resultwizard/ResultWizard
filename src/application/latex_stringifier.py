from typing import List
from domain.result import Result
from application.helpers import Helpers
from application.latex_ifelse import LatexIfElseBuilder
from application.stringifier import Stringifier, StringifierConfig
from domain.uncertainty import Uncertainty
from domain.value import Value


class LatexStringifier(Stringifier):
    """
    Provides methods to convert results to LaTeX commands.

    We assume the result to already be correctly rounded at this point.
    """

    plus_minus = r"\pm"
    negative_sign = "-"
    positive_sign = ""

    left_parenthesis = r"\left("
    right_parenthesis = r"\right)"

    value_prefix = r"\num{"
    value_suffix = r"}"

    error_name_prefix = r"_{\text{"
    error_name_suffix = r"}}"

    scientific_notation_prefix = r" \cdot 10^{"
    scientific_notation_suffix = "}"

    unit_prefix = r"\, \unit{"
    unit_suffix = "}"

    siunitx_fallback: bool

    def __init__(self, config: StringifierConfig, siunitx_fallback: bool):
        super().__init__(config)
        self.siunitx_fallback = siunitx_fallback

    @classmethod
    def uncertainty_name_to_cmd_name(cls, name: str) -> str:
        return f"\\Uncert{Helpers.capitalize(name)}"

    def result_to_latex_cmd(self, result: Result) -> str:
        """
        Returns the result as LaTeX command to be used in a .tex file.
        """
        builder = LatexIfElseBuilder()

        cmd_name = f"{self.config.identifier}{Helpers.capitalize(result.name)}"
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
                uncertainty_name = u.name if u.name != "" else Helpers.number_to_word(i + 1)
                uncertainty_name = f"error{Helpers.capitalize(uncertainty_name)}"
            error_latex_str = self.create_str(u.uncertainty, [], result.unit)
            builder.add_branch(uncertainty_name, error_latex_str)

        # Total uncertainty and short result
        if len(result.uncertainties) >= 2:
            short_result = result.get_short_result()
            if short_result is None:
                raise RuntimeError(
                    "Short result is None, but there should be at least two uncertainties."
                )
            error_latex_str = self.create_str(
                short_result.uncertainties[0].uncertainty, [], result.unit
            )
            builder.add_branch("errorTotal", error_latex_str)
            builder.add_branch("short", self.result_to_latex_str(short_result))

        # Unit
        if result.unit != "":
            builder.add_branch("unit", rf"\unit{{{result.unit}}}")
            builder.add_branch("withoutUnit", self.result_to_latex_str_without_unit(result))

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

    def create_str_tailored_to_siunitx(
        self, value: Value, uncertainties: List[Uncertainty], unit: str
    ) -> str:
        """
        Returns the result as LaTeX string making use of the siunitx package.

        This string does not yet contain "\newcommand*{}".
        """
        has_unit = unit != ""
        use_scientific_notation = self._should_use_scientific_notation(value, uncertainties)

        sign = self._value_to_sign_str(value)
        value_rounded, exponent, factor = self._value_to_str(value, use_scientific_notation)

        uncertainties_rounded = []
        for u in uncertainties:
            u_rounded = self._uncertainty_to_str(u, use_scientific_notation, exponent, factor)
            u_rounded = f" {self.plus_minus} {u_rounded}"
            if u.name != "":
                u_rounded += self.uncertainty_name_to_cmd_name(u.name)
            uncertainties_rounded.append(u_rounded)

        # Assemble everything together
        num_part = f"{sign}{value_rounded}{''.join(uncertainties_rounded)}"
        if use_scientific_notation:
            num_part += f" e{str(exponent)}"

        if has_unit:
            string = rf"\qty{{{num_part}}}{{{unit}}}"
        else:
            string = rf"\num{{{num_part}}}"

        return string

    def create_str_possible_fallback(
        self, value: Value, uncertainties: List[Uncertainty], unit: str
    ) -> str:
        """
        Returns the result as LaTeX string making use of the siunitx package.

        This string does not yet contain "\newcommand*{}".
        """
        if self.siunitx_fallback:
            return self.create_str(value, uncertainties, unit)
        return self.create_str_tailored_to_siunitx(value, uncertainties, unit)

    def result_to_latex_str(self, result: Result) -> str:
        """
        Returns the result as LaTeX string making use of the siunitx package.
        """
        return self.create_str_possible_fallback(result.value, result.uncertainties, result.unit)

    def result_to_latex_str_value(self, result: Result) -> str:
        """
        Returns only the value as LaTeX string making use of the siunitx package.
        """
        return self.create_str_possible_fallback(result.value, [], "")

    def result_to_latex_str_without_error(self, result: Result) -> str:
        """
        Returns the result without error as LaTeX string making use of the siunitx package.
        """
        return self.create_str_possible_fallback(result.value, [], result.unit)

    def result_to_latex_str_without_unit(self, result: Result) -> str:
        """
        Returns the result without unit as LaTeX string making use of the siunitx package.
        """
        return self.create_str_possible_fallback(result.value, result.uncertainties, "")
