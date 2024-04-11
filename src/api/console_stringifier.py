from domain.result import Result
from application.stringifier import Stringifier


class ConsoleStringifier(Stringifier):
    plus_minus = "±"
    negative_sign = "-"
    positive_sign = ""

    left_parenthesis = "("
    right_parenthesis = ")"

    value_prefix = ""
    value_suffix = ""

    error_name_prefix = " ("
    error_name_suffix = ")"

    scientific_notation_prefix = "e"
    scientific_notation_suffix = ""

    unit_prefix = " "
    unit_suffix = ""

    def result_to_str(self, result: Result):
        """
        Returns the result as human-readable string.
        """

        return f"{result.name} = {self.create_str(result.value, result.uncertainties, result.unit)}"

    def _modify_unit(self, unit: str) -> str:
        """
        Returns the modified unit.
        """
        unit = (
            unit.replace(" ", "")
            .replace(r"\squared", "^2")
            .replace(r"\cubed", "^3")
            .replace("\\per\\", "/")
            .replace(r"\per", "/")
            .replace("\\", " ")
            .strip()
        )

        if unit[0] == "/":
            unit = f"1{unit}"

        return unit
