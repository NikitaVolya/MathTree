from MathTypes import OperationsList, NodeType, Value
from addStrategy import AddContext, SingleStrategy, PriorityStrategy, BaseStrategy, BaseFunctionStrategy
from printStrategy import PrintContext
from CalculationsStrategy import CalculationsContext


class MathCompound:

    def __init__(self):
        self.root = Value(0)

    def add(self, operator_symbl: str, *args):
        operator = OperationsList.get(operator_symbl)
        if operator is None:
            return

        context = None
        if operator.state == NodeType.SINGLE_FUNCTION:
            context = AddContext(SingleStrategy())
        elif operator.state == NodeType.PRIORITY:
            context = AddContext(PriorityStrategy())
        elif operator.state == NodeType.BASE:
            context = AddContext(BaseStrategy())
        elif operator.state == NodeType.BASE_FUNCTION:
            context = AddContext(BaseFunctionStrategy())

        self.root = context.do_strategy(self.root, operator, *args)
        return self

    def calculations(self):
        if type(self.root) is Value:
            return self.root.value
        return CalculationsContext.do_auto_strategy(self.root)

    def get_node(self):
        return self.root.clone()

    def print(self):

        if self.root is Value:
            print(self.root)

        strategy = PrintContext.getStrategy(self.root)
        strategy.do(self.root)
        print()
