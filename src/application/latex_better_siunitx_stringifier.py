from typing import List

from application.stringifier import Stringifier
from domain.uncertainty import Uncertainty


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

    uncertainty_name_prefix = ""
    uncertainty_name_suffix = ""

    scientific_notation_prefix = "e"
    scientific_notation_suffix = ""

    unit_prefix = ""
    unit_suffix = ""
    # pylint: enable=duplicate-code

    def _modify_uncertainty_name(self, _name) -> str:
        return ""

    # pylint: disable-next=too-many-arguments
    def _assemble_str_parts(
        self,
        sign: str,
        value_rounded: str,
        uncertainties: List[Uncertainty],
        uncertainties_rounded: List[str],
        _should_use_parentheses: bool,
        use_scientific_notation: bool,
        exponent: int,
        unit: str,
    ):
        num_part = f"{sign}{value_rounded}{''.join(uncertainties_rounded)}"

        if use_scientific_notation:
            num_part += f" e{str(exponent)}"

        uncert_descriptors = [u.name for u in uncertainties if u.name != ""]
        uncert_descriptors_str = ""
        if len(uncert_descriptors) > 0:
            uncert_descriptors_str = f"[uncertainty-descriptors={{{','.join(uncert_descriptors)}}}]"

        if unit != "":
            string = rf"\qty{uncert_descriptors_str}{{{num_part}}}{{{unit}}}"
        else:
            string = rf"\num{uncert_descriptors_str}{{{num_part}}}"

        return string
