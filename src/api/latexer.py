import api.config as c
from application.latex_better_siunitx_stringifier import LatexBetterSiunitxStringifier
from application.latex_commandifier import LatexCommandifier
from application.latex_stringifier import LatexStringifier
from application.stringifier import Stringifier


def get_latexer() -> LatexCommandifier:
    return LatexCommandifier(_choose_latex_stringifier())


def _choose_latex_stringifier() -> Stringifier:
    use_fallback = c.configuration.siunitx_fallback
    stringifier_config = c.configuration.to_stringifier_config()

    if use_fallback:
        return LatexStringifier(stringifier_config)
    return LatexBetterSiunitxStringifier(stringifier_config)
