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

            string += f"{sign}{_Helpers.round_to_n_decimal_places(value.get_abs() * factor, value.get_sig_figs()-1)}"

            for u in uncertainties:
                string += rf" ± {_Helpers.round_to_n_decimal_places(u.uncertainty.get_abs() * factor, u.uncertainty.get_sig_figs()-1)}"
                if len(uncertainties) > 1:
                    string += rf" ({u.name})"

            if len(uncertainties) > 0:
                string += ")"

            string += rf"e{exponent}"
        else:
            if len(uncertainties) > 0:
                string += "("

            string += f"{sign}{_Helpers.round_to_n_decimal_places(value.get_abs(), value.get_decimal_place())}"

            for u in uncertainties:
                string += rf" ± {_Helpers.round_to_n_decimal_places(u.uncertainty.get_abs(), u.uncertainty.get_decimal_place())}"
                if len(uncertainties) > 1:
                    string += rf" ({u.name})"

            if len(uncertainties) > 0:
                string += ")"

        if has_unit:
            string += rf" {unit}"

        return string
