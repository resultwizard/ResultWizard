from domain.result import _Result
from application.helpers import _Helpers

# Config values:
min_exponent_for_non_scientific_notation = -2
max_exponent_for_non_scientific_notation = 3
identifier = "res"


class Stringifier:
    @classmethod
    def result_to_str(cls, result: _Result):
        """
        Returns the result as human-readable string.
        """

        value = result.value
        uncertainties = result.uncertainties
        unit = result.unit

        string = f"{result.name} = "
        use_scientific_notation = False
        has_unit = unit != ""

        # Determine if scientific notation should be used:
        if (
            value.get_exponent() < min_exponent_for_non_scientific_notation
            or value.get_exponent() > max_exponent_for_non_scientific_notation
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
                string += "("

            value_normalized = value.get_abs() * factor
            decimal_places = value.get_sig_figs()-1
            string += sign
            string += _Helpers.round_to_n_decimal_places(value_normalized, decimal_places)

            for u in uncertainties:
                value_normalized = u.uncertainty.get_abs() * factor
                decimal_places = exponent-u.uncertainty.get_min_exponent()
                string += " ± "
                string += _Helpers.round_to_n_decimal_places(value_normalized, decimal_places)
                if len(uncertainties) > 1:
                    string += rf" ({u.name})"

            if len(uncertainties) > 0:
                string += ")"

            string += rf"e{exponent}"
        else:
            if len(uncertainties) > 0 and unit != "":
                string += "("

            value_normalized = value.get_abs()
            decimal_places = value.get_decimal_place()
            string += sign
            string += _Helpers.round_to_n_decimal_places(value_normalized, decimal_places)

            for u in uncertainties:
                value_normalized = u.uncertainty.get_abs()
                decimal_places = u.uncertainty.get_decimal_place()
                string += " ± "
                string += _Helpers.round_to_n_decimal_places(value_normalized, decimal_places)
                if len(uncertainties) > 1:
                    string += rf" ({u.name})"

            if len(uncertainties) > 0 and unit != "":
                string += ")"

        if has_unit:
            unit = (
                unit.replace(r"\per", "/")
                .replace(r"\squared", "^2")
                .replace(r"\cubed", "^3")
                .replace("\\", "")
            )
            if unit[0] == "/":
                unit = "1" + unit
            string += rf" {unit}"

        return string
