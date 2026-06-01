class OperandStack:
    def __init__(self):
        self._data = []

    def push(self, operand):
        self._data.append(operand)

    def pop(self):
        if self.is_empty():
            raise Exception('OperandStack: pop on empty stack')
        return self._data.pop()

    def top(self):
        if self.is_empty():
            raise Exception('OperandStack: top on empty stack')
        return self._data[-1]

    def is_empty(self):
        return len(self._data) == 0

    def __repr__(self):
        return f'OperandStack({self._data})'
