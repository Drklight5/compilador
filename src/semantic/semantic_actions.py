from .function_directory import FunctionDirectory
from .semantic_cube import get_result_type, TYPES


class SemanticActions:
    def __init__(self, func_dir):
        self.func_dir = func_dir
        self.current_scope = 'global'

    # ── Scope ─────────────────────────────────────────────────────────

    def enter_function(self, name, return_type):
        if self.func_dir.exists(name):
            raise Exception(f'Function "{name}" already declared')
        self.func_dir.add_function(name, return_type)
        self.current_scope = name

    def exit_function(self):
        self.current_scope = 'global'

    # ── Variables y parámetros ────────────────────────────────────────

    def declare_variable(self, name, var_type):
        self.func_dir.add_variable(self.current_scope, name, var_type)

    def declare_parameter(self, param_name, param_type):
        self.func_dir.add_param(self.current_scope, param_name, param_type)

    def lookup_variable(self, name):
        return self.func_dir.get_variable(self.current_scope, name)

    def lookup_function(self, name):
        return self.func_dir.get_function(name)

    def function_exists(self, name):
        return self.func_dir.exists(name)

    # ── Validaciones de tipo ──────────────────────────────────────────

    def validate_assignment(self, left_type, right_type):
        if get_result_type(left_type, '=', right_type) == TYPES.ERROR:
            raise Exception(f'Cannot assign {right_type} to {left_type}')

    def validate_operation(self, left_type, op, right_type):
        result = get_result_type(left_type, op, right_type)
        if result == TYPES.ERROR:
            raise Exception(f'Type mismatch: {left_type} {op} {right_type}')
        return result

    def validate_condition(self, expr_type):
        if expr_type != TYPES.BOOL:
            raise Exception(
                f'Condition must be boolean, got {expr_type}'
            )

    # ── Validación de llamadas ────────────────────────────────────────

    def validate_call(self, func_name, arg_types):
        func = self.func_dir.get_function(func_name)
        params = func.params
        if len(arg_types) != len(params):
            raise Exception(
                f'Function "{func_name}" expects {len(params)} '
                f'argument(s), got {len(arg_types)}'
            )
        for i, (arg_type, param) in enumerate(zip(arg_types, params)):
            if get_result_type(param.type, '=', arg_type) == TYPES.ERROR:
                raise Exception(
                    f'Argument {i + 1} in call to "{func_name}": '
                    f'cannot pass {arg_type} as {param.type}'
                )

    # ── Validación de regresa ─────────────────────────────────────────

    def validate_return(self, expr_type=None):
        if self.current_scope == 'global':
            raise Exception('regresa cannot be used outside a function')
        func = self.func_dir.get_function(self.current_scope)
        expected = func.return_type
        if expr_type is None:
            if expected != TYPES.NULL:
                raise Exception(
                    f'Function "{self.current_scope}" must return '
                    f'{expected}, cannot use regresa without a value'
                )
        else:
            if expected == TYPES.NULL:
                raise Exception(
                    f'Function "{self.current_scope}" is nula, '
                    f'cannot return a value'
                )
            if get_result_type(expected, '=', expr_type) == TYPES.ERROR:
                raise Exception(
                    f'Function "{self.current_scope}" must return '
                    f'{expected}, got {expr_type}'
                )
