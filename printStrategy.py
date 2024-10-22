from MathTypes import Value, VoidValue, BaseOperation, NodeState
from abc import ABC, abstractmethod
from MathNode import Node


class PrintStrategy(ABC):

    @abstractmethod
    def do(self, node: Node or Value):
        pass


class ValuePrintStrategy(PrintStrategy):
    def do(self, node: Value):
        if node.value:
            print(node.value, end="")


class SinglePrintStrategy(PrintStrategy):
    def do(self, node: Node):
        print(node.value.symbl, end="(")
        centreStrategy = PrintContext.getStrategy(node.childes[0])
        centreStrategy.do(node.childes[0])
        print(")", end="")


class BasePrintStrategy(PrintStrategy):
    def do(self, node: Node):
        print("(", end="")
        leftStrategy = PrintContext.getStrategy(node.childes[0])
        leftStrategy.do(node.childes[0])

        print(node.value.symbl, end='')

        rightStrategy = PrintContext.getStrategy(node.childes[1])
        if rightStrategy:
            rightStrategy.do(node.childes[1])
        print(")", end="")


class PriorityPrintStrategy(PrintStrategy):
    def do(self, node: Node):
        BasePrintStrategy().do(node)


class PrintContext:
    def __init__(self, strategy: PrintStrategy):
        self._strategy = strategy

    @staticmethod
    def getStrategy(node) -> PrintStrategy:
        if type(node) is Value:
            return ValuePrintStrategy()
        if node.value.state == NodeState.SINGLE:
            return SinglePrintStrategy()
        if node.value.state == NodeState.PRIORITY:
            return PriorityPrintStrategy()
        if node.value.state == NodeState.BASE:
            return BasePrintStrategy()

    def do_strategy(self, node: Node):
        return self._strategy.do(node)
