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

    @abstractmethod
    def eval_text(self, line) -> float:
        pass


class EvalStrategyBrackets(EvalStrategyInterface):

    def __init__(self):
        pass

    @staticmethod
    def __dynamic_split(line: str, symbl: str):
        assert len(symbl) == 1, "Error symbl"
        rep = []
        i = 0
        j = 0
        brackets_count = 0
        while j < len(line):
            if line[j] == '(':
                brackets_count += 1
            elif line[j] == ')':
                brackets_count -= 1

            if line[j] == symbl and brackets_count == 0:
                rep.append(line[i:j])
                i = j + 1
            j += 1
        rep.append(line[i:j])
        return rep

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

        assert brackets_count == 0, "Error: __eval_brackets: brackets error"
        rep = []
        for line_part in EvalStrategyBrackets.__dynamic_split(line[1: i - 1], ','):
            rep.append(str(EvalStrategy().eval_text(line_part)))

        return '[' + ",".join(rep) + ']' + line[i:]

    def eval_text(self, line) -> str:
        i = 0
        while i < len(line):
            if line[i] == '(':
                line = line[:i] + EvalStrategyBrackets.__eval_block(line[i:])
            i += 1
        return line


class EvalStrategySingleOperation(EvalStrategyInterface):

    @staticmethod
    def __get_single_operator(line: str):
        operator_filter = lambda opr: opr.state == NodeType.SINGLE_FUNCTION
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

    def eval_text(self, line) -> str:
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

    def eval_text(self, line) -> float:
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


class EvalBaseFunctionStrategy(EvalStrategyInterface):

    def eval_part(self):
        pass

    @staticmethod
    def __get__base_function(line: str) -> str:
        operator_filter = lambda opr: opr.state == NodeType.BASE_FUNCTION
        operation_name = parceOperator(line, operator_filter)
        return operation_name

    @staticmethod
    def __eval_base_function(operator_name: str, line: str) -> str:
        j = len(operator_name)
        arguments = parceNumber(line[j:])
        values = [Value(float(number)) for number in arguments.split(",")]
        tmp = MathCompound()
        tmp.add(operator_name, *values)
        return '[' + str(tmp.calculations()) + line[j + len(arguments) + 1:]

    def eval_text(self, line) -> float:
        i = 0
        while i < len(line):
            operator_name = EvalBaseFunctionStrategy.__get__base_function(line[i:])
            if operator_name:
                line = line[:i] + EvalBaseFunctionStrategy.__eval_base_function(operator_name, line[i:])
            i += 1
        return line


class EvalStrategy(EvalStrategyInterface):

    def __init__(self):
        pass

    def eval_text(self, line) -> float:
        line = EvalStrategyBrackets().eval_text(line)
        line = EvalStrategySingleOperation().eval_text(line)
        line = EvalBaseFunctionStrategy().eval_text(line)
        rep = EvalStrategyBaseOperator().eval_text(line)
        return rep
