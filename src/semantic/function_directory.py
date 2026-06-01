from .variable_table import VariableTable


class ParamEntry:
    def __init__(self, name, param_type):
        self.name = name
        self.type = param_type

    def __repr__(self):
        return f'Param({self.name!r}: {self.type!r})'


class FunctionEntry:
    def __init__(self, return_type, start_address=None):
        self.return_type = return_type
        self.params = []
        self.var_table = VariableTable()
        self.start_address = start_address   # índice del primer cuádruplo
        self.return_address = None           # dirección virtual del valor de retorno

    def __repr__(self):
        return (
            f'FunctionEntry(ret={self.return_type!r}, '
            f'params={self.params}, vars={self.var_table})'
        )


class FunctionDirectory:
    def __init__(self):
        self._dir = {'global': FunctionEntry(return_type=None)}

    def add_function(self, name, return_type):
        if name in self._dir:
            raise Exception(f'Function "{name}" already declared')
        self._dir[name] = FunctionEntry(return_type)

    def get_function(self, name):
        if name not in self._dir:
            raise Exception(f'Function "{name}" not declared')
        return self._dir[name]

    def exists(self, name):
        return name in self._dir

    def add_param(self, func_name, param_name, param_type, address=None):
        entry = self.get_function(func_name)
        entry.params.append(ParamEntry(param_name, param_type))
        entry.var_table.add(param_name, param_type, address=address)

    def add_variable(self, scope, name, var_type, address=None, value=None):
        self.get_function(scope).var_table.add(name, var_type, address, value)

    def get_variable(self, scope, name):
        var = self.get_function(scope).var_table.get(name)
        if var:
            return var
        if scope != 'global':
            var = self.get_function('global').var_table.get(name)
            if var:
                return var
        raise Exception(f'Variable "{name}" not declared')

    def all_functions(self):
        return dict(self._dir)

    def __repr__(self):
        return f'FunctionDirectory({list(self._dir.keys())})'
