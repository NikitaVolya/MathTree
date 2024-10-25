from MathEval import MathText
from MathTypes import OperationsList


def main():

    OperationsList.add_function("int", lambda x: int(x))
    print(MathText.eval("fib(58)"))


if __name__ == '__main__':
    main()
