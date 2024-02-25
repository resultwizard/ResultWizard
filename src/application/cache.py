from domain.result import _Result


class _ResultsCache:
    """
    A cache for all user-defined results. Results are hashed by their name.
    If the user tries to add a result with a name that already exists in the cache,
    the new result will replace the old one ("shadowing").
    # TODO: is this the wanted behavior? Maybe print a warning in this case.
    """

    def __init__(self):
        self.cache: dict[str, _Result] = {}

    def add(self, name, result: _Result):
        self.cache[name] = result

    def get_all_results(self) -> list[_Result]:
        return list(self.cache.values())


_res_cache = _ResultsCache()
