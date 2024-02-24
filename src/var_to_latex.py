import numpy as np
from src.config import ExportConfig
from src.helpers import (
    snake_case_to_camel_case,
    get_exponent,
    round_to_n_decimal_places,
)


def var_to_latex_newcommand(
    name: str,
    value: float | int,
    error: float = 0,
    unit: str = "",
    sig_figs: int = -1,
    config: ExportConfig = ExportConfig(),
):
    # Create name:
    if not name.startswith(config.identifier):
        name = config.complete_identifier() + name
    camel_case_name = snake_case_to_camel_case(name)

    latex_str = var_to_latex(value, error, unit, sig_figs, config)

    if latex_str == "ERROR":
        print(f"There was an error with the variable {name}.")

    return "\\newcommand*{\\" + camel_case_name + "}{" + latex_str + "}\n"


def var_to_latex(
    value: float | int,
    error: float = 0,
    unit: str = "",
    sig_figs: int = -1,
    config: ExportConfig = ExportConfig(),
) -> str:
    has_error = error != 0
    has_unit = unit != ""
    has_sig_figs = sig_figs != -1

    # Allow for int values:
    if type(value) is int:
        value = float(value)
        if not has_error and not has_sig_figs:
            sig_figs = int(get_exponent(value)) + 1
            has_sig_figs = True

    # Create output string:
    output = ""

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
        return "ERROR"

    # Deal with the case that the user specified neither error nor sig figs:
    if not has_sig_figs and not has_error:
        sig_figs = config.default_sig_figs
        has_sig_figs = True

    # Get exponents:
    if value == 0:
        value_exponent = 0
    else:
        value_exponent = get_exponent(value)
    if has_error:
        error_exponent = get_exponent(error)

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

    # Round and normalize error:
    if has_error:
        error_rounded_normalized = (
            np.round(error / 10**error_min_exponent) / 10**sig_figs * 10
        )

    # Round and normalize value:
    value_rounded_normalized = (
        np.round(value / 10**value_min_exponent) / 10**sig_figs * 10
    )

    # Account for rounding like 0.999 -> 1.000 that change value exponent:
    if has_error:
        if get_exponent(error_rounded_normalized) > 0:
            error_exponent += 1
            error_min_exponent += 1
            error_rounded_normalized = (
                np.round(error / 10**error_min_exponent) / 10**sig_figs * 10
            )

        # Use scientific for errors like 120
        if error_min_exponent > 0:
            use_scientific_notation = True
    else:
        if get_exponent(value_rounded_normalized) > 0:
            value_exponent += 1
            value_min_exponent += 1
            value_rounded_normalized = (
                np.round(value / 10**value_min_exponent) / 10**sig_figs * 10
            )

        if value_min_exponent > 0:
            use_scientific_notation = True

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

    return output
