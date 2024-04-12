import re
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

        # Detect "\squared" etc.:
        unit = unit.replace(r"\squared", "^2").replace(r"\cubed", "^3")
        unit = re.sub(r"(\s+)\^", "^", unit)

        # Detect special units:
        unit = unit.replace(r"\percent", r"\%").replace(r"\degree", "°")

        # Detect "/":
        unit = unit.replace("/", " / ")

        # Iterate over unit parts:
        unit_parts = re.split(r"\\|\s", unit)
        numerator_parts = []
        denominator_parts = []
        is_next_part_in_denominator = False

        for unit_part in unit_parts:
            # Skip empty parts:
            if unit_part == "":
                continue

            # If next part is a denominator part:
            if unit_part in ("/", "per"):
                is_next_part_in_denominator = True
                continue

            # Add part to numerator or denominator:
            if is_next_part_in_denominator:
                denominator_parts.append(unit_part)
                is_next_part_in_denominator = False
            else:
                numerator_parts.append(unit_part)

        # Assemble unit:
        unit = ""

        # Handle empty unit:
        if len(numerator_parts) == 0 and len(denominator_parts) == 0:
            return ""

        # Numerator:
        if len(numerator_parts) == 0:
            unit += "1"
        elif len(numerator_parts) == 1 or len(denominator_parts) == 0:
            unit += " ".join(numerator_parts)
        else:
            unit += f"({' '.join(numerator_parts)})"

        # Denominator:
        if len(denominator_parts) > 0:
            unit += "/"
            if len(denominator_parts) == 1:
                unit += denominator_parts[0]
            else:
                unit += f"({' '.join(denominator_parts)})"

        return unit
