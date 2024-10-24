from MathCompound import MathCompound, Value
from MathTypes import OperationsList, NodeType


class MathEval:

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
    def __getNumber(line: str) -> str:
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

    @staticmethod
    def __get_single_operator(line: str):
        i: int = 0
        operation_name: str
        while i < len(line):
            if line[i] == '(' or \
                    line[i] == '.' or \
                    line[i] == '[' or \
                    ('0' <= line[i] <= '9'):
                break
            i += 1
        if i == len(line):
            operation_name = line
        else:
            operation_name = line[:i]
        if operation_name == "":
            return None
        operation = OperationsList.get(operation_name)
        if not operation or operation.state != NodeType.SINGLE:
            return None
        return operation_name

    @staticmethod
    def __get_base_operator(line: str) -> str | None:
        i: int = 0
        operation_name: str
        while i < len(line):
            if line[i] == '(' or \
                    line[i] == '.' or \
                    line[i] == '[' or \
                    ('0' <= line[i] <= '9'):
                break
            i += 1
        if i == len(line):
            operation_name = line
        else:
            operation_name = line[:i]
        if operation_name == "":
            return None
        operation = OperationsList.get(operation_name)
        if not operation or operation.state == NodeType.SINGLE:
            return None
        return operation_name

    @staticmethod
    def __eval_part(line: str) -> float:
        compound = MathCompound()
        i: int = 0
        while i < len(line):
            operation = MathEval.__get_base_operator(line[i:])
            if operation:
                i += len(operation)
            else:
                operation = '+'
            number = MathEval.__getNumber(line[i:])
            if line[i] == '[':
                i += 2
            i += len(number)
            compound.add(operation, Value(float(number)))
        return compound.calculations()

    @staticmethod
    def __eval_single_operator(operator: str, line: str) -> str:
        j = len(operator)
        number = MathEval.__getNumber(line[j:])
        tmp = MathCompound()
        tmp.add('+', Value(float(number)))
        tmp.add(operator)
        return '[' + str(tmp.calculations()) + line[j + len(number) + 1:]

    @staticmethod
    def __eval_brackets(line: str) -> (float, int):
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
        return MathEval.__equation(line[1:i]), i

    @staticmethod
    def __equation(line: str) -> float:
        i = 0
        while i < len(line):
            if line[i] == '(':
                number, j = MathEval.__eval_brackets(line[i:])
                line = line[:i] + "[" + str(number) + ']' + line[i + j + 1:]
            i += 1

        i = 0
        while i < len(line):
            operator_name = MathEval.__get_single_operator(line[i:])
            if not operator_name:
                i += 1
                continue
            line = line[:i] + MathEval.__eval_single_operator(operator_name, line[i:])
            i += 1
        return MathEval.__eval_part(line)

    @staticmethod
    def eval(line: str) -> float:
        if len(line) == 0:
            return 0.
        line = MathEval.__delete_spaces(line)
        return MathEval.__equation(line)
