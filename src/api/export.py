from application.cache import _res_cache
from application.latexer import _LaTeXer
from application.tables.latexer import _TableLaTeXer


def export(filepath: str):
    """
    Rounds all results according to the significant figures and writes them
    to a .tex file at the given filepath.
    """
    results = _res_cache.get_all_results()
    tables = _res_cache.get_all_tables()
    print(f"Processing {len(results)} result(s)")

    # Round and convert to LaTeX commands
    cmds = [
        r"%",
        r"% In your `main.tex` file, put this line directly before `\begin{document}`:",
        r"%   \input{" + filepath.split("/")[-1].split(".")[0] + r"}",
        r"%",
        r"",
        r"% Import required package:",
        r"\usepackage{ifthen}",
        r"",
        r"% Define commands to print the results:",
    ]
    for result in results:
        result_str = _LaTeXer.result_to_latex_cmd(result)
        cmds.append(result_str)
    for table in tables:
        table_str = _TableLaTeXer.table_to_latex_cmd(table)
        cmds.append(table_str)

    # Write to file
    with open(filepath, "w", encoding="utf-8") as f:
        f.write("\n".join(cmds))
    print(f'Exported to "{filepath}"')
