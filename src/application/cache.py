from application.error_messages import RESULT_SHADOWED
from domain.result import Result
from domain.tables.table import Table


class ResultsCache:
    """
    A cache for all user-defined results. Results are hashed by their name.
    If the user tries to add a result with a name that already exists in the cache,
    the new result will replace the old one ("shadowing").
    """

    def __init__(self):
        self.results: dict[str, Result] = {}
        self.tables: dict[str, Table] = {}
        self.issue_result_overwrite_warning = True

    def configure(self, issue_result_overwrite_warning: bool):
        self.issue_result_overwrite_warning = issue_result_overwrite_warning

    def add(self, name, result: Result):

        if self.issue_result_overwrite_warning and name in self.results:
            print(RESULT_SHADOWED.format(name=name))

        self.results[name] = result

    def add_table(self, name, table: Table):

        if self.issue_result_overwrite_warning and name in self.tables:
            print(RESULT_SHADOWED.format(name=name))

        self.tables[name] = table

    def get_all_results(self) -> list[Result]:
        return list(self.results.values())

    def get_all_tables(self) -> list[Table]:
        return list(self.tables.values())


_res_cache = ResultsCache()
