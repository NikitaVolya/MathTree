from MathEval import MathEval
from MathTypes import OperationsList, NodeType


def main():
    OperationsList.add_function("test", lambda x: x + 10, NodeType.SINGLE)
    print(MathEval.eval("3.0 * 2 + test(2)"))


if __name__ == '__main__':
    main()
