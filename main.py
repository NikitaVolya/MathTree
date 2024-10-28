from MathText import MathText
from MathTypes import OperationsList


def main():
    mathText = MathText()
    mathText.add_value("a", 10)
    mathText.add_value('b', 15)
    print(mathText.eval("fib({b} - {a})"))
    print(mathText.eval("ppcm({a}, {b}) * 2"))
    print(mathText.eval("fib({b} - {a}) + ppcm({a}, {b}) * 2"))
    print(mathText.eval("(fib({b} - {a}) + ppcm({a}, {b}) * 2) / 2"))


if __name__ == '__main__':
    main()
