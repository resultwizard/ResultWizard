from src.config import ExportConfig
from src.helpers import snake_case_to_camel_case
from src.var_to_latex import var_to_latex


def globals_to_latex(variables: dict[str, any], config=ExportConfig()) -> str:
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

        # Read variable:
        if type(variables[key]) is tuple:
            value = variables[key][0]

            if len(variables[key]) > 1:
                error = variables[key][1]
            else:
                error = 0

            if len(variables[key]) > 2:
                unit = variables[key][2]
            else:
                unit = ""

            if len(variables[key]) > 3:
                sig_figs = variables[key][3]
            else:
                sig_figs = -1
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

        export += var_to_latex(camel_case_name, value, error, unit, sig_figs, config)

    return export
