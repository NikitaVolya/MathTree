import math
from typing import Callable
from dataclasses import dataclass
from enum import Enum


class NodeState(Enum):
    SINGLE = 'single'
    PRIORITY = 'priority'
    BASE = 'base'


@dataclass
class Value:
    value: int or float


VoidValue = Value(None)


@dataclass
class BaseOperation:
    symbl: str = None
    func: Callable = None
    state: str = NodeState.BASE

    def clone(self):
        return BaseOperation(self.symbl, self.func, self.state)


class OperationsList(Enum):

    @staticmethod
    def get(key: str) -> BaseOperation:
        data = {
            "+": BaseOperation("+", lambda a, b: a + b),
            "-": BaseOperation("-", lambda a, b: a - b),
            "*": BaseOperation("*", lambda a, b: a * b, NodeState.PRIORITY),
            "/": BaseOperation("-", lambda a, b: a / b, NodeState.PRIORITY),
            "abs": BaseOperation("abs", lambda a: abs(a), NodeState.SINGLE),
            "sqrt": BaseOperation("sqrt", lambda a: math.sqrt(a), NodeState.SINGLE),
        }
        return data.get(key)
