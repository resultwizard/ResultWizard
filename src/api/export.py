from application.cache import _res_cache
from application.rounder import _Rounder
from application.latexer import _LaTeXer


def export(filepath):
    """
    Rounds all results according to the significant figures and writes them
    to a .tex file at the given filepath.
    """
    results = _res_cache.get_all_results()
    print(f"Processing {len(results)} result(s)")

    # Round and convert to LaTeX commands
    cmds = []
    for result in results:
        _Rounder.round_result(result)
        print(result)
        result_str = _LaTeXer.result_to_latex_cmd(result)
        cmds.append(result_str)

    # Write to file
    with open(filepath, "w") as f:
        f.write("\n".join(cmds))
    print(f'Exported to "{filepath}"')
