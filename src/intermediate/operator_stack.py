class OperatorStack:
    def __init__(self):
        self._data = []

    def push(self, operator):
        self._data.append(operator)

    def pop(self):
        if self.is_empty():
            raise Exception('OperatorStack: pop on empty stack')
        return self._data.pop()

    def top(self):
        if self.is_empty():
            raise Exception('OperatorStack: top on empty stack')
        return self._data[-1]

    def is_empty(self):
        return len(self._data) == 0

    def __repr__(self):
        return f'OperatorStack({self._data})'
