from src.helpers import round_to_n_decimal_places
from src.config import ExportConfig
from src.helpers import snake_case_to_camel_case, snake_case_to_kebab_case
from src.var_to_latex import var_to_latex
import numpy as np


def table_to_latex_newcommand(
    name: str,
    columns: list,
    caption: str = "",
    float_mode: str = "h!",
    resize_to_fit_page: bool = False,
    config: ExportConfig = ExportConfig(),
):
    # Create name:
    if not name.startswith(config.table_identifier):
        name = config.complete_table_identifier() + name
    camel_case_name = snake_case_to_camel_case(name)

    return (
        "\\newcommand*{\\"
        + camel_case_name
        + "}{%\n"
        + table_to_latex(name, columns, caption, float_mode, resize_to_fit_page, config)
        + "}\n"
    )


def table_to_latex(
    name: str,
    columns: list,
    caption: str = "",
    float_mode: str = "h!",
    resize_to_fit_page: bool = False,
    config: ExportConfig = ExportConfig(),
) -> str:
    # Create name:
    if not name.startswith(config.table_identifier):
        name = config.complete_table_identifier() + name
    kebab_case_name = snake_case_to_kebab_case(name)

    # Check for faulty things:
    is_faulty = False

    if is_faulty:
        print(f"There was an error with the table {name}.")
        return "ERROR"

    # Create output string:
    output = ""

    # Table header:
    output += "\\begin{" + "table" + "}[" + float_mode + "]\n"
    output += "\\begin{" + "center" + "}\n"
    if resize_to_fit_page:
        output += "\\resizebox{\\textwidth}{!}{"
    output += "\\begin{" + "tabular" + "}{|"
    for i in range(len(columns)):
        output += "c|"
    output += "}\n"
    output += "\\hline\n"

    # Header row:
    is_first_column = True
    for column in columns:
        if not is_first_column:
            output += "&"
        is_first_column = False

        output += "\\textbf{" + column[0] + "}"

    # Unit row:
    exist_units = False
    for column in columns:
        if column[1] != "":
            exist_units = True
    if exist_units:
        output += "\\\\\n"
        is_first_column = True
        for column in columns:
            if not is_first_column:
                output += "&"
            is_first_column = False

            if column[1] != "":
                output += "$[\\unit{" + column[1] + "}]$"
    output += "\\\\ \\hline \n"

    # Value rows:
    for i in range(len(columns[0][2])):
        is_first_column = True
        for column in columns:
            if not is_first_column:
                output += "&"
            is_first_column = False

            if type(column[2][i]) is str or type(column[2][i]) is np.str_:
                output += column[2][i]
            else:
                value = column[2][i]
                try:
                    error = column[3][i]
                except:
                    error = 0
                try:
                    sig_figs = column[4]
                    if type(sig_figs) is list:
                        sig_figs = sig_figs[i]
                except:
                    sig_figs = -1
                try:
                    unit = column[5]
                    if type(unit) is list:
                        unit = unit[i]
                except:
                    unit = ""

                output += "$" + var_to_latex(value, error, unit, sig_figs, config) + "$"

        output += "\\\\\n"

    # Table footer:
    output += "\\hline\n"
    output += "\\end{" + "tabular" + "}\n"
    if resize_to_fit_page:
        output += "}"
    if caption != "":
        output += "\\caption{" + caption + "}\n"
    output += "\\label{" + kebab_case_name + "}\n"
    output += "\\end{" + "center" + "}\n"
    output += "\\end{" + "table" + "}\n"

    return output
