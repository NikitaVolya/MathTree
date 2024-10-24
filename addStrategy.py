from MathTypes import Value, VoidValue, BaseOperation
from abc import ABC, abstractmethod
from MathNode import Node


class AddStrategy(ABC):

    @abstractmethod
    def do(self, node: Node, operator: BaseOperation or Value, values: []):
        pass


class PriorityStrategy(AddStrategy):
    def do(self, node: Node, operator: BaseOperation or Value, values: []):
        if type(node) is Value:
            raise "Error"
        newNode = Node(operator, node.childes[1], values[0])
        node.childes[1] = newNode
        return node


class SingleStrategy(AddStrategy):
    def do(self, node: Node, operator: BaseOperation or Value, values: []):
        if type(node) is VoidValue:
            raise "Error"
        newNode = Node(operator, node)
        node = newNode
        return node


class BaseStrategy(AddStrategy):
    def do(self, node: Node, operator: BaseOperation or Value, values):
        newNode = Node(operator, node, values[0])
        node = newNode
        return node


class AddContext:
    def __init__(self, strategy: AddStrategy):
        self._strategy = strategy

    def do_strategy(self, node: Node, operator: BaseOperation or Value, *args):
        return self._strategy.do(node, operator, [*args])
