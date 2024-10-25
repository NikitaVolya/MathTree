import math
from typing import Callable
from dataclasses import dataclass
from enum import Enum
from MathFunctions import *


class NodeType(Enum):
    SINGLE = 'single'
    PRIORITY = 'priority'
    BASE = 'base'


@dataclass
class Value:
    value: int or float

    def clone(self):
        return Value(self.value)


VoidValue = Value(None)


@dataclass
class BaseOperation:
    symbl: str = None
    func: Callable = None
    state: str = NodeType.BASE

    def clone(self):
        return BaseOperation(self.symbl, self.func, self.state)


def OPERATOR_NAME_FILTER(name: str) -> bool:
    if '(' in name or ')' in name or '[' in name or ']' in name or \
            '.' in name:
        return True
    for i in range(0, 10):
        if str(i) in name:
            return True
    return False


DATA = {
    "+": BaseOperation("+", lambda a, b: a + b),
    "-": BaseOperation("-", lambda a, b: a - b),
    "*": BaseOperation("*", lambda a, b: a * b, NodeType.PRIORITY),
    "/": BaseOperation("/", lambda a, b: a / b, NodeType.PRIORITY),
    "//": BaseOperation("//", lambda a, b: a // b, NodeType.PRIORITY),
    "%": BaseOperation("%", lambda a, b: a % b, NodeType.PRIORITY),
    "**": BaseOperation("**", lambda a, b: a ** b, NodeType.PRIORITY),
    "^": BaseOperation("^", lambda a, b: a ** b, NodeType.PRIORITY),
    "abs": BaseOperation("abs", lambda a: abs(a), NodeType.SINGLE),
    "sqrt": BaseOperation("sqrt", lambda a: math.sqrt(a), NodeType.SINGLE),
    "sin": BaseOperation("sin", lambda a: math.sin(a), NodeType.SINGLE),
    "cos": BaseOperation("cos", lambda a: math.cos(a), NodeType.SINGLE),
    "fib": BaseOperation("fib", lambda a: fib(a), NodeType.SINGLE)
}


class OperationsList(Enum):

    @staticmethod
    def operators():
        return DATA.keys()

    @staticmethod
    def get(key: str) -> BaseOperation | None:
        return DATA.get(key)

    @staticmethod
    def add_function(name: str, func):
        if name in DATA:
            raise "Error: add_function: Function exist"
        if OPERATOR_NAME_FILTER(name):
            raise "Error: add_function"
        DATA[name] = BaseOperation(name, func, NodeType.SINGLE)

    @staticmethod
    def add_operator(name: str, func):
        if name in DATA:
            raise "Error: add_function: Function exist"
        if OPERATOR_NAME_FILTER(name):
            raise "Error: add_function"
        DATA[name] = BaseOperation(name, func, NodeType.BASE)
