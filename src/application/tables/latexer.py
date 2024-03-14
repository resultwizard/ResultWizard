from domain.tables.table import _Table
from domain.result import _Result
from application.latexer import _LaTeXer


# Config values:
min_exponent_for_non_scientific_notation = -2
max_exponent_for_non_scientific_notation = 3
table_identifier = "table"


class _TableLaTeXer:
    @classmethod
    def table_to_latex_cmd(cls, table: _Table) -> str:
        """
        Returns the table as LaTeX command to be used in a .tex file.
        """

        cmd_name = table_identifier + table.name[0].upper() + table.name[1:]

        # New command:
        latex_str = rf"\newcommand*{{\{cmd_name}}}[1][]{{" + "\n"

        # Table header:
        latex_str += r"\begin{table}[#1]" + "\n"
        latex_str += r"\begin{center}" + "\n"
        if table.resize_to_fit_page:
            latex_str += r"\resizebox{\textwidth}{!}{"

        if table.horizontal:
            latex_str += cls._table_to_latex_tabular_horizontal(table)
        else:
            latex_str += cls._table_to_latex_tabular_vertical(table)

        # Table footer:
        if table.resize_to_fit_page:
            latex_str += "}"
        if table.caption != "":
            latex_str += rf"\caption{{{table.caption}}}" + "\n"
        latex_str += rf"\label{{{table.label if table.label is not None else cmd_name}}}" + "\n"
        latex_str += "\\end{center}\n"
        latex_str += "\\end{table}\n"
        latex_str += "}"

        return latex_str

    @classmethod
    def _table_to_latex_tabular_vertical(cls, table: _Table) -> str:
        latex_str = r"\begin{tabular}{|"
        for _ in range(len(table.columns)):
            latex_str += r"c|"
        latex_str += "}\n"
        latex_str += r"\hline" + "\n"

        # Header row:
        is_first_column = True
        for column in table.columns:
            if not is_first_column:
                latex_str += "&"
            is_first_column = False

            latex_str += rf"\textbf{{{column.title}}}"

        # Unit row:
        if cls._exist_units(table):
            latex_str += "\\\\\n"
            is_first_column = True
            for column in table.columns:
                if not is_first_column:
                    latex_str += "&"
                is_first_column = False

                if column.unit != "":
                    latex_str += rf"$[\unit{{{column.unit}}}]$"
        latex_str += "\\\\ \\hline \n"

        # Value rows:
        for i, _ in enumerate(table.columns[0].cells):
            is_first_column = True
            for column in table.columns:
                if not is_first_column:
                    latex_str += "&"
                is_first_column = False

                cell = column.cells[i]

                if isinstance(cell, _Result):
                    value_str = _LaTeXer.create_latex_str(
                        cell.value, cell.uncertainties, cell.unit if column.unit == "" else ""
                    )
                    latex_str += f"${value_str}$"
                else:
                    latex_str += str(cell)

            latex_str += "\\\\\n"

        latex_str += "\\hline\n"
        latex_str += "\\end{tabular}\n"

        return latex_str

    @classmethod
    def _table_to_latex_tabular_horizontal(cls, table: _Table) -> str:
        latex_str = r"\begin{tabular}{|l"
        if cls._exist_units(table):
            latex_str += r"c||"
        else:
            latex_str += r"||"
        for _ in range(len(table.columns[0].cells)):
            latex_str += r"c|"
        latex_str += "}\n"
        latex_str += r"\hline" + "\n"

        # Iterate through columns (that are rows now):
        for row in table.columns:
            latex_str += rf"\textbf{{{row.title}}}"
            if row.unit != "":
                latex_str += rf" & $[\unit{{{row.unit}}}]$"
            else:
                latex_str += " & "
            for cell in row.cells:
                if isinstance(cell, _Result):
                    value_str = _LaTeXer.create_latex_str(
                        cell.value, cell.uncertainties, cell.unit if row.unit == "" else ""
                    )
                    latex_str += f" & ${value_str}$"
                else:
                    latex_str += f" & {cell}"
            latex_str += "\\\\ \\hline \n"

        latex_str += "\\end{tabular}\n"

        return latex_str

    @classmethod
    def _exist_units(cls, table: _Table) -> bool:
        for column in table.columns:
            if column.unit != "":
                return True
        return False
