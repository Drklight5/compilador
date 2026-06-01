class TypeStack:
    def __init__(self):
        self._data = []

    def push(self, var_type):
        self._data.append(var_type)

    def pop(self):
        if self.is_empty():
            raise Exception('TypeStack: pop on empty stack')
        return self._data.pop()

    def top(self):
        if self.is_empty():
            raise Exception('TypeStack: top on empty stack')
        return self._data[-1]

    def is_empty(self):
        return len(self._data) == 0

    def __repr__(self):
        return f'TypeStack({self._data})'
