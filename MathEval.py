from MathCompound import MathCompound, Value
from MathTypes import OperationsList, NodeType, OPERATOR_NAME_FILTER
from abc import ABC, abstractmethod


def parceNumber(line: str) -> str:
    rep = ""
    i = 0
    if line[0] == '[':
        j = i + 1
        while line[j] != ']':
            j += 1
        return line[1:j]
    while i < len(line):
        if line[i] == "." or ('0' <= line[i] <= '9'):
            rep += line[i]
        else:
            break
        i += 1
    return rep


def parceOperator(line: str, *filters) -> str:
    i = 0
    while i < len(line):
        if OPERATOR_NAME_FILTER(line[i]):
            break
        i += 1

    if i == len(line):
        raise "Error: text syntax"

    operation_name = line[:i]
    operation = OperationsList.get(operation_name)

    if not operation:
        return None

    for operation_filter in filters:
        if not operation_filter(operation):
            return None
    return operation_name


class EvalStrategyInterface(ABC):

    @staticmethod
    @abstractmethod
    def eval_text(line) -> float:
        pass


class EvalStrategyBrackets(EvalStrategyInterface):

    def __init__(self):
        pass

    @staticmethod
    def __eval_block(line) -> str:
        i = 1
        brackets_count = 1
        while brackets_count != 0 and i < len(line):
            if line[i] == '(':
                brackets_count += 1
            elif line[i] == ')':
                brackets_count -= 1
            i += 1

        if brackets_count != 0:
            raise "Error: __eval_brackets: brackets error"
        i -= 1
        return '[' + str(EvalStrategy.eval_text(line[1:i])) + ']' + line[i + 1:]

    @staticmethod
    def eval_text(line) -> float:
        i = 0
        while i < len(line):
            if line[i] == '(':
                line = line[:i] + EvalStrategyBrackets.__eval_block(line[i:])
            i += 1
        return line


class EvalStrategySingleOperation(EvalStrategyInterface):

    @staticmethod
    def __get_single_operator(line: str):
        operator_filter = lambda opr: opr.state == NodeType.SINGLE
        operation_name = parceOperator(line, operator_filter)
        return operation_name

    @staticmethod
    def __eval_single_operator(operator: str, line: str) -> str:
        j = len(operator)
        number = parceNumber(line[j:])
        tmp = MathCompound()
        tmp.add('+', Value(float(number)))
        tmp.add(operator)
        return '[' + str(tmp.calculations()) + line[j + len(number) + 1:]

    @staticmethod
    def eval_text(line) -> float:
        i = 0
        while i < len(line):
            operator_name = EvalStrategySingleOperation.__get_single_operator(line[i:])
            if operator_name:
                line = line[:i] + EvalStrategySingleOperation.__eval_single_operator(operator_name, line[i:])
            i += 1
        return line


class EvalStrategyBaseOperator(EvalStrategyInterface):

    def __init__(self):
        pass

    @staticmethod
    def __get_base_operator(line: str) -> str | None:
        operator_filter = lambda opr: opr.state == NodeType.BASE or opr.state == NodeType.PRIORITY
        operation_name = parceOperator(line, operator_filter)
        return operation_name

    @staticmethod
    def eval_text(line) -> float:
        compound = MathCompound()
        i: int = 0
        while i < len(line):
            operation = EvalStrategyBaseOperator.__get_base_operator(line[i:])

            if operation:
                i += len(operation)
            else:
                operation = '+'

            number = parceNumber(line[i:])

            if line[i] == '[':
                i += 2
            i += len(number)

            compound.add(operation, Value(float(number)))

        return compound.calculations()


class EvalStrategy(EvalStrategyInterface):

    @staticmethod
    def eval_text(line) -> float:
        line = EvalStrategyBrackets.eval_text(line)
        line = EvalStrategySingleOperation.eval_text(line)
        rep = EvalStrategyBaseOperator.eval_text(line)
        return rep


class MathText:

    def __init__(self):
        pass

    @staticmethod
    def __delete_spaces(line: str):
        rep = ""
        for ch in line:
            if ch != ' ':
                rep += ch
        return rep

    @staticmethod
    def eval(line: str) -> float:
        if len(line) == 0:
            return 0.
        line = MathText.__delete_spaces(line)
        rep = EvalStrategy.eval_text(line)
        return rep
