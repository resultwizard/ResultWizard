from application.stringifier import Stringifier
from application.helpers import Helpers
from domain.result import Result
from domain.tables.table import Table


class TableLatexCommandifier:
    """Makes use of a LaTeX stringifier to embed a table into a LaTeX command."""

    def __init__(self, stringifier: Stringifier):
        self.s = stringifier

    def table_to_latex_cmd(self, table: Table) -> str:
        """
        Returns the table as LaTeX command to be used in a .tex file.
        """

        cmd_name = f"{self.s.config.table_identifier}{Helpers.capitalize(table.name)}"

        # New command:
        latex_str = rf"\newcommand*{{\{cmd_name}}}[1][]{{" + "\n"

        # Table header:
        latex_str += r"\begin{table}[#1]" + "\n"
        latex_str += r"\begin{center}" + "\n"
        if table.resize_to_fit_page:
            latex_str += r"\resizebox{\textwidth}{!}{"

        if table.horizontal:
            latex_str += self._table_to_latex_tabular_horizontal(table)
        else:
            latex_str += self._table_to_latex_tabular_vertical(table)

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

    def _table_to_latex_tabular_vertical(self, table: Table) -> str:
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
        if self._exist_units(table):
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

                if isinstance(cell, Result):
                    value_str = self.s.create_str(
                        cell.value, cell.uncertainties, cell.unit if column.unit == "" else ""
                    )
                    latex_str += f"${value_str}$"
                else:
                    latex_str += str(cell)

            latex_str += "\\\\\n"

        latex_str += "\\hline\n"
        latex_str += "\\end{tabular}\n"

        return latex_str

    def _table_to_latex_tabular_horizontal(self, table: Table) -> str:
        latex_str = r"\begin{tabular}{|l"
        if self._exist_units(table):
            latex_str += r"c||"
        else:
            latex_str += r"||"
        for _ in range(len(table.columns[0].cells)):
            latex_str += r"c|"
        latex_str += "}\n"
        latex_str += r"\hline" + "\n"

        # Iterate through columns (that are rows now):
        for row in table.columns:
            # Header column:
            latex_str += rf"\textbf{{{row.title}}}"

            # Unit column:
            if self._exist_units(table):
                if row.unit != "":
                    latex_str += rf" & $[\unit{{{row.unit}}}]$"
                else:
                    latex_str += " & "

            # Value columns:
            for cell in row.cells:
                if isinstance(cell, Result):
                    value_str = self.s.create_str(
                        cell.value, cell.uncertainties, cell.unit if row.unit == "" else ""
                    )
                    latex_str += f" & ${value_str}$"
                else:
                    latex_str += f" & {cell}"
            latex_str += "\\\\ \\hline \n"

        latex_str += "\\end{tabular}\n"

        return latex_str

    def _exist_units(self, table: Table) -> bool:
        for column in table.columns:
            if column.unit != "":
                return True
        return False
