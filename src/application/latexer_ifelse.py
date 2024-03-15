class LatexIfElseBuilder:
    def __init__(self):
        self.latex: str = ""
        self._num_parentheses_to_close: int = 0
        self.keywords: list[str] = []

    def add_branch(self, keyword: str, body: str):
        # Condition
        if self.latex == "":
            self.latex += rf"    \ifthenelse{{\equal{{#1}}{{{keyword}}}}}{{"
        else:
            self.latex += "\n"
            self.latex += rf"    }}{{\ifthenelse{{\equal{{#1}}{{{keyword}}}}}{{"
            self._num_parentheses_to_close += 1

        if keyword != "":
            self.keywords.append(keyword)

        # Body
        self.latex += "\n"
        self.latex += rf"        {body}"

    def build(self) -> str:
        for _ in range(self._num_parentheses_to_close):
            self.latex += "}"

        return self.latex
