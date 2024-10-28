from MathTypes import Value, NodeType, OperationsList
from abc import ABC, abstractmethod
from MathNode import Node


class CalculationsStrategy(ABC):

    @abstractmethod
    def do(self, node: Node | Value) -> float:
        pass


class ValueCalculationsStrategy(CalculationsStrategy):
    def do(self, node: Value) -> float:
        return node.value


class SingleCalculationsStrategy(CalculationsStrategy):
    def do(self, node: Node) -> float:
        operation = OperationsList.get(node.value.symbl)
        child_rep = CalculationsContext.do_auto_strategy(node.childes[0])
        return operation.func(child_rep)


class BaseCalculationsStrategy(CalculationsStrategy):
    def do(self, node: Node) -> float:
        operation = OperationsList.get(node.value.symbl)
        left_rep = CalculationsContext.do_auto_strategy(node.childes[0])
        right_rep = CalculationsContext.do_auto_strategy(node.childes[1])
        return operation.func(left_rep, right_rep)


class CalculationsContext:
    def __init__(self, strategy: CalculationsStrategy = None):
        self._strategy: CalculationsStrategy = strategy

    @staticmethod
    def getStrategy(node) -> CalculationsStrategy:
        if type(node) is Value:
            return ValueCalculationsStrategy()
        if node.value.state == NodeType.SINGLE_FUNCTION:
            return SingleCalculationsStrategy()
        if node.value.state == NodeType.PRIORITY:
            return BaseCalculationsStrategy()
        if node.value.state == NodeType.BASE:
            return BaseCalculationsStrategy()
        if node.value.state == NodeType.BASE_FUNCTION:
            return BaseCalculationsStrategy()

    def setStrategy(self, strategy: CalculationsStrategy):
        self._strategy = strategy

    @staticmethod
    def do_auto_strategy(node: Node) -> float:
        context = CalculationsContext()
        strategy = CalculationsContext.getStrategy(node)
        context.setStrategy(strategy)
        return context.do_strategy(node)

    def do_strategy(self, node: Node) -> float:
        return self._strategy.do(node)
