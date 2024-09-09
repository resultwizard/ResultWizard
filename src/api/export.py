from typing import Set
from api.latexer import get_latexer
from api.res import _res_cache
import api.config as c
from application.helpers import Helpers


def export(filepath: str):
    """
    Rounds all results according to the significant figures and writes them
    to a .tex file at the given filepath.
    """
    return _export(filepath, print_completed=True)


def _export(filepath: str, print_completed: bool):
    results = _res_cache.get_all_results()

    if print_completed:
        print(f"Processing {len(results)} result(s)")

    # Round and convert to LaTeX commands
    lines = [
        r"%",
        r"% In your `main.tex` file, put this line directly before `\begin{document}`:",
        r"%   \input{" + filepath.split("/")[-1].split(".")[0] + r"}",
        r"%",
        r"",
        r"% Import required package:",
        r"\usepackage{siunitx}",
        r"\usepackage{ifthen}",
        r"",
    ]

    latexer = get_latexer()

    uncertainty_names = set()
    result_lines = []
    for result in results:
        uncertainty_names.update(u.name for u in result.uncertainties if u.name != "")
        result_str = latexer.result_to_latex_cmd(result)
        result_lines.append(result_str)

    if not c.configuration.siunitx_fallback:
        siunitx_setup = _uncertainty_names_to_siunitx_setup(uncertainty_names)
        if siunitx_setup != "":
            lines.append("% Commands to correctly print the uncertainties in siunitx:")
            lines.append(siunitx_setup)
            lines.append("")

    lines.append("% Commands to print the results. Use them in your document.")
    lines.extend(result_lines)

    # Write to file
    with open(filepath, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    if print_completed:
        print(f'Exported to "{filepath}"')


def _uncertainty_names_to_siunitx_setup(uncert_names: Set[str]) -> str:
    """
    Returns the preamble for the LaTeX document to use the siunitx package.
    """
    if len(uncert_names) == 0:
        return ""

    cmd_names = []
    cmds = []
    for name in uncert_names:
        cmd_name = f"\\Uncert{Helpers.capitalize(name)}"
        cmd_names.append(cmd_name)
        cmds.append(rf"\NewDocumentCommand{{{cmd_name}}}{{}}{{_{{\text{{{name}}}}}}}")

    string = "\n".join(cmds)
    string += "\n"
    string += rf"\sisetup{{input-digits=0123456789{''.join(cmd_names)}}}"

    return string
