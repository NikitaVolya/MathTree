from Concstructions import Stack
from MathCompound import MathCompound, Value


class MathEval:

    def __init__(self):
        pass

    @staticmethod
    def __delete_spaces(line: str):
        rep = ""
        for ch in line:
            if ch != ' ':
                rep += ch
        return rep

    @staticmethod
    def getNumer(line: str) -> str:
        rep = ""
        i = 0
        if line[0] == '[':
            j = i + 1
            while line[j] != ']':
                j += 1
            return line[1:j]
        while i < len(line):
            if line[i] == "." or ('0' <= line[i] <= '9'):
                rep += line[i]
            else:
                break
            i += 1
        return rep

    @staticmethod
    def eval_part(line: str) -> float:
        print(line)
        compound = MathCompound()
        number = MathEval.getNumer(line)
        i = len(number)
        compound.add('+', Value(float(number)))
        while i < len(line):
            operation = line[i]
            i += 1
            number = MathEval.getNumer(line[i:])
            if line[i] == '[':
                i += 2
            i += len(number)
            compound.add(operation, Value(float(number)))
        return compound.calculations()

    @staticmethod
    def eval(line: str) -> float:
        line = MathEval.__delete_spaces(line)
        i = 0
        while i < len(line):
            if line[i] == '(':
                symbl_count = 1
                j = i + 1
                while symbl_count != 0:
                    if line[j] == '(':
                        symbl_count += 1
                    elif line[j] == ')':
                        symbl_count -= 1
                    j += 1
                tmp_line = line[i + 1:j - 1]
                line = line[:i] + '[' + str(MathEval.eval(tmp_line)) + ']' + line[j:]
            i += 1
        return MathEval.eval_part(line)
