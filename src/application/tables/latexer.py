import textwrap
from domain.tables.table import _Table


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

        latex_str = rf"""
        \newcommand*{{\{cmd_name}}}[1][]{{
        """
        latex_str = textwrap.dedent(latex_str).strip()

        raise NotImplementedError
