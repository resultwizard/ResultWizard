import os
import numpy as np


class ExportConfig:
    def __init__(
        self,
        identifier="result",
        error_identifier="error",
        unit_identifier="unit",
        sig_figs_identifier="sigfigs",
        min_exponent_for_non_scientific_notation=-2,
        max_exponent_for_non_scientific_notation=3,
        default_sig_figs=2,
    ) -> None:
        self.identifier = identifier
        self.error_identifier = error_identifier
        self.unit_identifier = unit_identifier
        self.sig_figs_identifier = sig_figs_identifier
        self.min_exponent_for_non_scientific_notation = (
            min_exponent_for_non_scientific_notation
        )
        self.max_exponent_for_non_scientific_notation = (
            max_exponent_for_non_scientific_notation
        )
        self.default_sig_figs = default_sig_figs

    def complete_identifier(self):
        return self.identifier + "_"

    def complete_error_identifier(self):
        return self.identifier + "_" + self.error_identifier + "_"

    def complete_unit_identifier(self):
        return self.identifier + "_" + self.unit_identifier + "_"

    def complete_sig_figs_identifier(self):
        return self.identifier + "_" + self.sig_figs_identifier + "_"


def snake_case_to_camel_case(snake_case_name: str):
    name_parts = snake_case_name.split("_")
    camel_case_name = name_parts[0]
    for name_part in name_parts[1:]:
        camel_case_name += name_part[0].upper() + name_part[1:]
    return camel_case_name


def round_to_n_decimal_places(v: float, n: int):
    return "{:.{}f}".format(v, int(n))


def export(variables: dict[str, any], config=ExportConfig()):
    # Get relevant keys:
    keys = [
        key
        for key in variables.keys()
        if key.startswith(config.complete_identifier())
        and not key.startswith(config.complete_error_identifier())
        and not key.startswith(config.complete_unit_identifier())
        and not key.startswith(config.complete_sig_figs_identifier())
    ]

    # Create export string:
    export = ""

    # Iterate through keys:
    for key in keys:
        # Get variable name:
        name = key[key.index("_") + 1 :]
        camel_case_name = snake_case_to_camel_case(key)

        # Create output string:
        output = "\\newcommand*{\\" + camel_case_name + "}{"

        # Read variable:
        if type(variables[key]) is tuple:
            value = variables[key][0]

            if len(variables[key]) > 1:
                error = variables[key][1]
            else:
                error = 0
            has_error = error != 0

            if len(variables[key]) > 2:
                unit = variables[key][2]
            else:
                unit = ""
            has_unit = unit != ""

            if len(variables[key]) > 3:
                sig_figs = variables[key][3]
            else:
                sig_figs = -1
            has_sig_figs = sig_figs != -1
        else:
            value = variables[key]

            error_key = f"{config.complete_error_identifier()}{name}"
            has_error = error_key in variables.keys()
            if has_error:
                error = variables[error_key]
            else:
                error = 0

            unit_key = f"{config.complete_unit_identifier()}{name}"
            has_unit = unit_key in variables.keys()
            if has_unit:
                unit = variables[unit_key]
            else:
                unit = ""

            sig_figs_key = f"{config.complete_sig_figs_identifier()}{name}"
            has_sig_figs = sig_figs_key in variables.keys()
            if has_sig_figs:
                sig_figs = variables[sig_figs_key]
            else:
                sig_figs = -1

        is_negative = value < 0
        value = np.abs(value)

        # Check for faulty values:
        is_not_faulty = (
            isinstance(value, (int, float))
            and value != float("inf")
            and value != float("-inf")
            and isinstance(error, (int, float))
            and error != float("inf")
            and error != float("-inf")
        )
        if not is_not_faulty:
            export += "\\newcommand*{\\" + camel_case_name + "}{ERROR}\n"
            print(f"There was an error with the variable {camel_case_name}.")
            continue

        # Deal with the case that the user specified neither error nor sig figs:
        if not has_sig_figs and not has_error:
            sig_figs = config.default_sig_figs
            has_sig_figs = True

        # Get exponents:
        if value == 0:
            value_exponent = 0
        else:
            value_exponent = np.floor(np.log10(value))
        if has_error:
            error_exponent = np.floor(np.log10(error))

        # Should use scientific notation?
        use_scientific_notation = (
            value_exponent < config.min_exponent_for_non_scientific_notation
            or value_exponent > config.max_exponent_for_non_scientific_notation
        )

        # Set min exponents:
        if has_sig_figs:
            value_min_exponent = value_exponent - sig_figs + 1
            error_min_exponent = value_min_exponent
        elif has_error:
            # Get error sig figs:
            error_first_digit = np.round(error / 10**error_exponent)
            if error_first_digit <= 2:
                error_sig_figs = 2
            else:
                error_sig_figs = 1

            error_min_exponent = error_exponent - error_sig_figs + 1
            value_min_exponent = error_min_exponent

            # Get number of sig figs:
            sig_figs = value_exponent - value_min_exponent + 1

        # Additional calculations if there is an error:
        if has_error:
            # Use scientific for errors like 120
            if error_min_exponent > 0:
                use_scientific_notation = True

            # Round and normalize error:
            error_rounded_normalized = (
                np.round(error / 10**error_min_exponent) / 10**sig_figs * 10
            )
        else:
            if value_min_exponent > 0:
                use_scientific_notation = True

        # Round and normalize value:
        value_rounded_normalized = (
            np.round(value / 10**value_min_exponent) / 10**sig_figs * 10
        )

        # Generate output:
        if is_negative:
            sign = "-"
        else:
            sign = ""

        if use_scientific_notation:
            if has_error:
                output += (
                    "("
                    + sign
                    + round_to_n_decimal_places(value_rounded_normalized, sig_figs - 1)
                    + " \\pm "
                    + round_to_n_decimal_places(error_rounded_normalized, sig_figs - 1)
                    + ") \\cdot 10^{"
                    + round_to_n_decimal_places(value_exponent, 0)
                    + "}"
                )
            else:
                output += (
                    sign
                    + round_to_n_decimal_places(value_rounded_normalized, sig_figs - 1)
                    + "\\cdot 10^{"
                    + round_to_n_decimal_places(value_exponent, 0)
                    + "}"
                )
        else:
            decimal_places = max(0, -value_min_exponent)
            if has_error:
                if has_unit:
                    output += "("
                output += (
                    sign
                    + round_to_n_decimal_places(
                        value_rounded_normalized * 10**value_exponent, decimal_places
                    )
                    + " \\pm "
                    + round_to_n_decimal_places(
                        error_rounded_normalized * 10**value_exponent, decimal_places
                    )
                )
                if has_unit:
                    output += ")"
            else:
                output += sign + round_to_n_decimal_places(
                    value_rounded_normalized * 10**value_exponent, decimal_places
                )

        # Add unit:
        if has_unit:
            output += "\\ \\unit{" + unit + "}"

        # Add to export:
        export += output + "}\n"

    # Delete current file:
    try:
        os.remove("../results.tex")
    except:
        pass

    # Write file:
    with open("../results.tex", "w") as f:
        f.write(export)
