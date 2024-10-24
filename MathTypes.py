import math
from typing import Callable
from dataclasses import dataclass
from enum import Enum


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


DATA = {
        "+": BaseOperation("+", lambda a, b: a + b),
        "-": BaseOperation("-", lambda a, b: a - b),
        "*": BaseOperation("*", lambda a, b: a * b, NodeType.PRIORITY),
        "/": BaseOperation("/", lambda a, b: a / b, NodeType.PRIORITY),
        "^": BaseOperation("^", lambda a, b: a ** b, NodeType.PRIORITY),
        "abs": BaseOperation("abs", lambda a: abs(a), NodeType.SINGLE),
        "sqrt": BaseOperation("sqrt", lambda a: math.sqrt(a), NodeType.SINGLE),
        "sin": BaseOperation("sin", lambda a: math.sin(a), NodeType.SINGLE),
        "cos": BaseOperation("cos", lambda a: math.cos(a), NodeType.SINGLE)
}


class OperationsList(Enum):

    @staticmethod
    def operators():
        return DATA.keys()

    @staticmethod
    def get(key: str) -> BaseOperation | None:
        return DATA.get(key)

    @staticmethod
    def add_function(name: str, func, func_type: str = NodeType.BASE):
        if name in DATA:
            raise "Error: add_function: Function exist"
        DATA[name] = BaseOperation(name, func, func_type)
