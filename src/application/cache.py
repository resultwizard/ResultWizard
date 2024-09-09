from application.error_messages import RESULT_SHADOWED
from domain.result import Result


class ResultsCache:
    """
    A cache for all user-defined results. Results are hashed by their name.
    If the user tries to add a result with a name that already exists in the cache,
    the new result will replace the old one ("shadowing").
    """

    def __init__(self):
        self.cache: dict[str, Result] = {}
        self.issue_result_overwrite_warning = True

    def configure(self, issue_result_overwrite_warning: bool):
        self.issue_result_overwrite_warning = issue_result_overwrite_warning

    def add(self, name, result: Result):

        if self.issue_result_overwrite_warning and name in self.cache:
            print(RESULT_SHADOWED.format(name=name))

        self.cache[name] = result

    def get_all_results(self) -> list[Result]:
        return list(self.cache.values())
