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
        "/": BaseOperation("-", lambda a, b: a / b, NodeType.PRIORITY),
        "m": BaseOperation("m", lambda a: abs(a), NodeType.SINGLE),
        "√": BaseOperation("√", lambda a: math.sqrt(a), NodeType.SINGLE),
        "s": BaseOperation("s", lambda a: math.sin(a), NodeType.SINGLE),
        "c": BaseOperation("c", lambda a: math.cos(a), NodeType.SINGLE)
}


class OperationsList(Enum):

    @staticmethod
    def operators():
        return DATA.keys()

    @staticmethod
    def get(key: str) -> BaseOperation:
        return DATA.get(key)
