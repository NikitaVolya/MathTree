from MathCompound import MathCompound
from MathTypes import Value


def main():
    a = MathCompound()
    a.add('-', Value(10))
    a.add('+', Value(2))

    a.print()


if __name__ == '__main__':
    main()
