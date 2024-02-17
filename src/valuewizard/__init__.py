from result import _Result, PrintableResult
from cache import _ResultsCache

_cache = _ResultsCache()


def res(
    name: str, value: float | str, uncertainty: float | str, unit: str
) -> PrintableResult:
    if not isinstance(name, str):
        raise TypeError(f"`name` must be a string, not {type(name)}")

    result = _Result(name, value, uncertainty, unit)
    _cache.add(name, result)

    return result.to_printable()


def export(filepath):
    all_results = _cache.get_all_results()
    print(all_results)
    print(f"Write .tex file to {filepath}")
