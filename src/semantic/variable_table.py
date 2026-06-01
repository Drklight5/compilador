class VarEntry:
    def __init__(self, name, var_type, address=None, value=None):
        self.name = name
        self.type = var_type
        self.address = address  # reservado para Fase 4 (direcciones virtuales)
        self.value = value

    def __repr__(self):
        return f'VarEntry({self.name!r}: {self.type!r}, addr={self.address})'


class VariableTable:
    def __init__(self):
        self._table = {}

    def add(self, name, var_type, address=None, value=None):
        if name in self._table:
            raise Exception(f'Variable "{name}" already declared in this scope')
        self._table[name] = VarEntry(name, var_type, address, value)

    def get(self, name):
        return self._table.get(name)

    def exists(self, name):
        return name in self._table

    def all(self):
        return dict(self._table)

    def __repr__(self):
        return f'VariableTable({list(self._table.keys())})'
