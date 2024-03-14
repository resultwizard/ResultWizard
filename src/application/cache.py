from domain.result import _Result
from domain.tables.table import _Table


class _ResultsCache:
    """
    A cache for all user-defined results. Results are hashed by their name.
    If the user tries to add a result with a name that already exists in the cache,
    the new result will replace the old one ("shadowing").
    # TODO: is this the wanted behavior? Maybe print a warning in this case.
    """

    def __init__(self):
        self.res_cache: dict[str, _Result] = {}
        self.table_cache: dict[str, _Table] = {}

    def add_res(self, name: str, result: _Result):
        self.res_cache[name] = result

    def add_table(self, name: str, table: _Table):
        self.table_cache[name] = table

    def get_all_results(self) -> list[_Result]:
        return list(self.res_cache.values())
    
    def get_all_tables(self) -> list[_Table]:
        return list(self.table_cache.values())


_res_cache = _ResultsCache()
