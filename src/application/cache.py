from domain.result import Result


class ResultsCache:
    """
    A cache for all user-defined results. Results are hashed by their name.
    If the user tries to add a result with a name that already exists in the cache,
    the new result will replace the old one ("shadowing").
    """

    def __init__(self):
        self.cache: dict[str, Result] = {}

    def add(self, name, result: Result):
        if name in self.cache:
            print(
                f"Warning: A result with the name '{name}' already exists and will be overwritten."
            )

        self.cache[name] = result

    def get_all_results(self) -> list[Result]:
        return list(self.cache.values())
