from api.latexer import get_latexer
from api.res import _res_cache


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

    lines.append("% Commands to print the results. Use them in your document.")
    lines.extend(result_lines)

    # Write to file
    with open(filepath, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    if print_completed:
        print(f'Exported to "{filepath}"')
