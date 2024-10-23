
class Stack:

    def __init__(self):
        self.__items = []

    def push(self, value):
        self.__items.insert(0, value)

    def pop(self):
        return self.__items.pop()

    def head(self):
        return self.__items[0]
