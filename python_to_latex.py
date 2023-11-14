import os
from src.config import ExportConfig
from src.globals_to_latex import globals_to_latex
from src.var_to_latex import var_to_latex
from src.helpers import snake_case_to_camel_case


class PythonToLatex:
    def __init__(self, config: ExportConfig = ExportConfig()) -> None:
        self._config = config
        self._export_str = ""

    def var(
        self,
        name: str,
        value: float,
        error: float = 0,
        unit: str = "",
        sig_figs: int = -1,
    ):
        self._export_str += var_to_latex(
            snake_case_to_camel_case(self._config.complete_identifier() + name),
            value,
            error,
            unit,
            sig_figs,
            self._config,
        )

    def export(self, path: str, globals: dict[str, any] = {}):
        abs_path = os.path.realpath(os.path.join(os.getcwd(), path))

        # Globals to latex:
        self._export_str += globals_to_latex(globals, self._config)

        # Delete current file:
        try:
            os.remove(abs_path)
        except:
            pass

        # Write file:
        with open(abs_path, "w") as f:
            f.write(self._export_str)
