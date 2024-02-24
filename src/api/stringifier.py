from domain.result import _Result


class Stringifier:
    @classmethod
    def result_to_str(cls, result: _Result):
        # TODO
        return result.__str__()
        # return "This is the result (TODO)"
