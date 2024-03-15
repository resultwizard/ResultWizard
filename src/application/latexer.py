from dataclasses import dataclass
from typing import List

from domain.result import _Result
from domain.value import _Value
from domain.uncertainty import _Uncertainty
from application.helpers import _Helpers


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

        cmd_name = self.config.identifier + result.name[0].upper() + result.name[1:]

        latex_str = rf"\newcommand*{{\{cmd_name}}}[1][]{{" + "\n"
        latex_str += r"    \ifthenelse{\equal{#1}{}}{" + "\n"
        latex_str += f"        {self.result_to_latex_str(result)}"

        number_of_parentheses_to_close = 0
        keywords = []

        # Value:
        latex_str += "\n"
        latex_str += r"    }{\ifthenelse{\equal{#1}{value}}{"
        latex_str += "\n"
        latex_str += rf"        {self.result_to_latex_str_value(result)}"
        keywords.append("value")

        number_of_parentheses_to_close += 1

        # Without error:
        if len(result.uncertainties) > 0:
            latex_str += "\n"
            latex_str += r"    }{\ifthenelse{\equal{#1}{withoutError}}{"
            latex_str += "\n"
            latex_str += rf"        {self.result_to_latex_str_without_error(result)}"
            keywords.append("withoutError")

            number_of_parentheses_to_close += 1

        # Single uncertainties:
        for i, u in enumerate(result.uncertainties):
            if len(result.uncertainties) == 1:
                uncertainty_name = "error"
            else:
                if u.name != "":
                    uncertainty_name = u.name
                else:
                    uncertainty_name = _Helpers.number_to_word(i + 1)
                uncertainty_name = "error" + uncertainty_name[0].upper() + uncertainty_name[1:]
            error_latex_str = self._create_latex_str(u.uncertainty, [], result.unit)

            latex_str += "\n"
            latex_str += rf"    }}{{\ifthenelse{{\equal{{#1}}{{{uncertainty_name}}}}}{{"
            latex_str += "\n"
            latex_str += rf"        {error_latex_str}"
            keywords.append(uncertainty_name)

            number_of_parentheses_to_close += 1

        # Total uncertainty and short result:
        if len(result.uncertainties) >= 2:
            short_result = result.get_short_result()
            if short_result is None:
                raise RuntimeError(
                    "Short result is None, but there should be at least two uncertainties."
                )

            error_latex_str = self._create_latex_str(
                short_result.uncertainties[0].uncertainty, [], result.unit
            )

            latex_str += "\n"
            latex_str += r"    }{\ifthenelse{\equal{#1}{errorTotal}}{"
            latex_str += "\n"
            latex_str += rf"        {error_latex_str}"
            keywords.append("errorTotal")

            number_of_parentheses_to_close += 1

            latex_str += "\n"
            latex_str += r"    }{\ifthenelse{\equal{#1}{short}}{"
            latex_str += "\n"
            latex_str += rf"        {self.result_to_latex_str(short_result)}"
            keywords.append("short")

            number_of_parentheses_to_close += 1

        # Unit:
        if result.unit != "":
            latex_str += "\n"
            latex_str += r"    }{\ifthenelse{\equal{#1}{unit}}{"
            latex_str += "\n"
            latex_str += rf"        \unit{{{result.unit}}}"
            keywords.append("unit")

            number_of_parentheses_to_close += 1

        # Error message:
        if len(keywords) > 0:
            latex_str += (
                "\n"
                + r"    }{\tiny\textbf{Please specify one of the following keywords: "
                + ", ".join([rf"\texttt{{{k}}}" for k in keywords])
                + r" or don't use any keyword at all.}\normalsize}"
            )
        else:
            latex_str += (
                "\n"
                + r"    }{\tiny\textbf{This variable can only be used without keyword.}\normalsize}"
            )

        for _ in range(number_of_parentheses_to_close):
            latex_str += "}"
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
        use_scientific_notation = False
        has_unit = unit != ""

        # Determine if scientific notation should be used:
        if (
            value.get_exponent() < self.config.min_exponent_for_non_scientific_notation
            or value.get_exponent() > self.config.max_exponent_for_non_scientific_notation
        ):
            use_scientific_notation = True

        if value.get_min_exponent() > 0:
            use_scientific_notation = True

        for u in uncertainties:
            if u.uncertainty.get_min_exponent() > 0:
                use_scientific_notation = True

        # Create LaTeX string:
        if value.get() < 0:
            sign = "-"
        else:
            sign = ""

        if use_scientific_notation:
            exponent = value.get_exponent()
            factor = 10 ** (-exponent)

            if len(uncertainties) > 0:
                latex_str += "("

            value_normalized = value.get_abs() * factor
            decimal_places = value.get_sig_figs() - 1
            latex_str += sign
            latex_str += _Helpers.round_to_n_decimal_places(value_normalized, decimal_places)

            for u in uncertainties:
                value_normalized = u.uncertainty.get_abs() * factor
                decimal_places = exponent - u.uncertainty.get_min_exponent()
                latex_str += r" \pm "
                latex_str += _Helpers.round_to_n_decimal_places(value_normalized, decimal_places)
                if len(uncertainties) > 1:
                    latex_str += rf"_{{\text{{{u.name}}}}}"

            if len(uncertainties) > 0:
                latex_str += ")"

            latex_str += rf" \cdot 10^{{{exponent}}}"
        else:
            if len(uncertainties) > 0 and unit != "":
                latex_str += "("

            value_normalized = value.get_abs()
            decimal_places = value.get_decimal_place()
            latex_str += sign
            latex_str += _Helpers.round_to_n_decimal_places(value_normalized, decimal_places)

            for u in uncertainties:
                latex_str += rf" \pm {_Helpers.round_to_n_decimal_places(u.uncertainty.get_abs(), u.uncertainty.get_decimal_place())}"
                if len(uncertainties) > 1:
                    latex_str += rf"_{{\text{{{u.name}}}}}"

            if len(uncertainties) > 0 and unit != "":
                latex_str += ")"

        if has_unit:
            latex_str += rf"\ \unit{{{unit}}}"

        return latex_str
