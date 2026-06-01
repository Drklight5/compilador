import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from intermediate.quadruple import Quadruple
from intermediate.operand_stack import OperandStack
from intermediate.operator_stack import OperatorStack
from intermediate.type_stack import TypeStack
from intermediate.jump_stack import JumpStack
from semantic.semantic_cube import get_result_type, TYPES


class QuadrupleManager:
    def __init__(self, vm):
        self.vm = vm
        self._quadruples = []

        self.operand_stack  = OperandStack()
        self.operator_stack = OperatorStack()
        self.type_stack     = TypeStack()
        self.jump_stack     = JumpStack()

    # ── Temporales ────────────────────────────────────────────────────

    def new_temp(self, temp_type):
        """Asigna dirección virtual para un nuevo temporal."""
        return self.vm.next_address('temp', temp_type)

    # ── Emisión ───────────────────────────────────────────────────────

    def emit(self, op, left, right, result):
        self._quadruples.append(Quadruple(op, left, right, result))

    def fill(self, index, value):
        """Backpatch: rellena el campo result del cuádruplo en 'index'."""
        self._quadruples[index].result = value

    # ── Pilas ─────────────────────────────────────────────────────────

    def push_operand(self, operand, operand_type):
        self.operand_stack.push(operand)
        self.type_stack.push(operand_type)

    def pop_operand(self):
        return self.operand_stack.pop(), self.type_stack.pop()

    def peek_type(self):
        return self.type_stack.top()

    # ── Operación binaria ─────────────────────────────────────────────

    def generate_operation(self, op):
        right, right_type = self.pop_operand()
        left,  left_type  = self.pop_operand()

        result_type = get_result_type(left_type, op, right_type)
        if result_type == TYPES.ERROR:
            raise Exception(f'Type mismatch: {left_type} {op} {right_type}')

        temp = self.new_temp(result_type)
        self.emit(op, left, right, temp)
        self.push_operand(temp, result_type)
        return temp

    # ── Asignación ────────────────────────────────────────────────────

    def emit_assignment(self, var_addr):
        operand, _ = self.pop_operand()
        self.emit('=', operand, None, var_addr)

    # ── Acceso ────────────────────────────────────────────────────────

    def count(self):
        return len(self._quadruples)

    def get_quadruples(self):
        return list(self._quadruples)

    def print_quadruples(self, vm=None):
        if not self._quadruples:
            print('  (sin cuadruplos generados)')
            return

        def fmt(val):
            if val is None:
                return '_'
            if vm and isinstance(val, int):
                name = vm.get_name(val)
                return f'{val}({name})' if name != str(val) else str(val)
            return str(val)

        print(f"\n  {'#':<5} {'OP':<10} {'IZQ':<20} {'DER':<20} {'RES'}")
        print('  ' + '-' * 65)
        for i, q in enumerate(self._quadruples):
            print(
                f'  {i:<5} {str(q.op):<10} '
                f'{fmt(q.left):<20} {fmt(q.right):<20} {fmt(q.result)}'
            )
