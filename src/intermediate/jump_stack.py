# Reservado para Fase 4 — saltos condicionales y cíclicos

class JumpStack:
    def __init__(self):
        self._data = []

    def push(self, index):
        self._data.append(index)

    def pop(self):
        if self.is_empty():
            raise Exception('JumpStack: pop on empty stack')
        return self._data.pop()

    def top(self):
        if self.is_empty():
            raise Exception('JumpStack: top on empty stack')
        return self._data[-1]

    def is_empty(self):
        return len(self._data) == 0

    def __repr__(self):
        return f'JumpStack({self._data})'
