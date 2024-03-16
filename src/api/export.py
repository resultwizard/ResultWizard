from api.res import _res_cache
import api.config as c
from application.latex_stringifier import LatexStringifier


def export(filepath: str):
    """
    Rounds all results according to the significant figures and writes them
    to a .tex file at the given filepath.
    """
    results = _res_cache.get_all_results()
    print(f"Processing {len(results)} result(s)")

    # Round and convert to LaTeX commands
    cmds = [
        r"%",
        r"% In your `main.tex` file, put this line directly before `\begin{document}`:",
        r"%   \input{" + filepath.split("/")[-1].split(".")[0] + r"}",
        r"%",
        r"",
        r"% Import required package:",
        r"\usepackage{siunitx}",
        r"\usepackage{ifthen}",
        r"",
        r"% Define commands to print the results:",
    ]

    latexer = LatexStringifier(c.configuration.to_stringifier_config())
    for result in results:
        result_str = latexer.result_to_latex_cmd(result)
        cmds.append(result_str)

    # Write to file
    with open(filepath, "w", encoding="utf-8") as f:
        f.write("\n".join(cmds))
    print(f'Exported to "{filepath}"')
