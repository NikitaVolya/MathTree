from MathTypes import BaseOperation, Value


class Node:

    def __init__(self, value: Value or BaseOperation, *args):
        self.value = value
        self.childes = [*args]

    def clone(self) -> 'Node':
        tmp = Node(self.value.clone())
        for el in self.childes:
            if type(el) is Node:
                tmp.childes.append(el.clone())
            else:
                tmp.childes.append(el)
        return tmp

    def __str__(self) -> str:
        return self.__repr__()

    def __repr__(self) -> str:
        return '[' + str(self.value) + ' -> x' + str(len(self.childes)) + ']'
