from MathEval import EvalStrategy
from MathTypes import OPERATOR_NAME_FILTER


class MathText:

    def __init__(self):
        self.__values: [tuple[str, float | int]] = []

    @staticmethod
    def __delete_spaces(line: str):
        return line.replace(' ', '')

    def __replace_values(self, line: str):
        for key, value in self.__values:
            line = line.replace('{' + str(key) + '}', f"[{value}]")
        return line

    def add_value(self, key: str, value: float | int):
        assert not OPERATOR_NAME_FILTER(key), "Key value is nod valid"
        assert isinstance(value, float) or isinstance(value, int), "Value is not valid"

        self.__values.append([key, value])

    def eval(self, line: str) -> float:
        assert isinstance(line, str)

        if len(line) == 0:
            return 0.
        line = line.lower()
        line = self.__replace_values(line)
        line = MathText.__delete_spaces(line)
        rep = EvalStrategy().eval_text(line)
        return rep
