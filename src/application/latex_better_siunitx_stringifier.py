from typing import List

from application.helpers import Helpers
from application.stringifier import Stringifier


class LatexBetterSiunitxStringifier(Stringifier):
    """
    Provides methods to convert results to LaTeX commands.

    We assume the result to already be correctly rounded at this point.
    """

    # pylint: disable=duplicate-code
    plus_minus = r"\pm"
    negative_sign = "-"
    positive_sign = ""

    left_parenthesis = r"\left("
    right_parenthesis = r"\right)"

    value_prefix = ""
    value_suffix = ""

    error_name_prefix = r"\Uncert"
    error_name_suffix = ""

    scientific_notation_prefix = "e"
    scientific_notation_suffix = ""

    unit_prefix = ""
    unit_suffix = ""
    # pylint: enable=duplicate-code

    def _modify_uncertainty_name(self, name) -> str:
        return Helpers.capitalize(name)

    # pylint: disable-next=too-many-arguments
    def _assemble_str_parts(
        self,
        sign: str,
        value_rounded: str,
        uncertainties_rounded: List[str],
        should_use_parentheses: bool,
        use_scientific_notation: bool,
        exponent: int,
        unit: str,
    ):
        num_part = f"{sign}{value_rounded}{''.join(uncertainties_rounded)}"

        if use_scientific_notation:
            num_part += f" e{str(exponent)}"

        if unit != "":
            string = rf"\qty{{{num_part}}}{{{unit}}}"
        else:
            string = rf"\num{{{num_part}}}"

        return string
