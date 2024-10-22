from MathTypes import VoidValue, OperationsList, NodeState, Value
from addStrategy import AddContext, SingleStrategy, PriorityStrategy, BaseStrategy
from printStrategy import PrintContext, SinglePrintStrategy, PriorityPrintStrategy, BasePrintStrategy


class MathCompound:

    def __init__(self):
        self.root = VoidValue

    def add(self, operator_symbl: str, *args):

        operator = OperationsList.get(operator_symbl)
        if operator is None:
            return

        context = None
        if operator.state == NodeState.SINGLE:
            context = AddContext(SingleStrategy())
        elif operator.state == NodeState.PRIORITY:
            context = AddContext(PriorityStrategy())
        elif operator.state == NodeState.BASE:
            context = AddContext(BaseStrategy())

        self.root = context.do_strategy(self.root, operator, *args)

    def get_node(self):
        return self.root.clone()

    def print(self):

        if self.root is Value:
            print(self.root)

        strategy = PrintContext.getStrategy(self.root)
        strategy.do(self.root)
