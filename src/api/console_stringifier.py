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

    uncertainty_name_prefix = " ("
    uncertainty_name_suffix = ")"

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

        # Remove all whitespace characters (space, tab, newline etc.)
        unit = "".join(unit.split())

        # Detect "\squared" etc.
        unit = unit.replace(r"\squared", "^2").replace(r"\cubed", "^3")

        # Detect special units
        unit = unit.replace(r"\percent", r"\%").replace(r"\degree", r"\°")

        # Detect "/"
        unit = unit.replace("/", " / ")

        # Iterate over unit parts
        unit_parts = re.split(r"[\\|\s]+", unit)
        numerator_parts = []
        denominator_parts = []
        is_next_part_in_denominator = False

        for unit_part in unit_parts:
            # Skip empty parts
            if unit_part == "":
                continue

            # If next part is a denominator part
            if unit_part in ("/", "per"):
                is_next_part_in_denominator = True
                continue

            # Add part to numerator or denominator
            if is_next_part_in_denominator:
                denominator_parts.append(unit_part)
                is_next_part_in_denominator = False
            else:
                numerator_parts.append(unit_part)

        # Assemble unit
        modified_unit = ""

        # Handle empty unit
        if not numerator_parts and not denominator_parts:
            return ""

        # Numerator
        if not numerator_parts:
            modified_unit += "1"
        elif len(numerator_parts) == 1 or not denominator_parts:
            modified_unit += " ".join(numerator_parts)
        else:
            modified_unit += f"({' '.join(numerator_parts)})"

        # Denominator
        if denominator_parts:
            modified_unit += "/"
            if len(denominator_parts) == 1:
                modified_unit += denominator_parts[0]
            else:
                modified_unit += f"({' '.join(denominator_parts)})"

        modified_unit = self.strip_whitespaces_around_parentheses(modified_unit)
        modified_unit = self.replace_per_by_symbol(modified_unit)

        return modified_unit

    def strip_whitespaces_around_parentheses(self, string: str) -> str:
        return string.replace(" (", "(").replace("( ", "(").replace(" )", ")").replace(") ", ")")

    def replace_per_by_symbol(self, string: str) -> str:
        """
        Replaces all occurrences of `per` with `/`.

        This might be necessary due to limitations of the above parsing method
        where `per(` is recognized as a single token. For a proper parser, we
        would have to deal with parentheses in a more sophisticated way. As this
        is not the scope of this project for now, we just do a simple replacement
        of the `per` that slipped through the above logic.

        Note that at this point, `percent` was already replaced by `%`, so
        we can safely replace all occurrences of "per" with "/".
        """
        return string.replace("per", " / ")
