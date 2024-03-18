from application.stringifier import Stringifier


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

    unit_prefix = r" \, \unit{"
    unit_suffix = "}"
