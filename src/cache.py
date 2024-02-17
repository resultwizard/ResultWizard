from result import _Result


class _ResultsCache:
    def __init__(self):
        self.cache: dict[str, _Result] = {}

    def add(self, name, result: _Result):
        self.cache[name] = result

    def get_all_results(self):
        return self.cache.items()
