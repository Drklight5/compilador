import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from intermediate.quadruple import Quadruple
from intermediate.operand_stack import OperandStack
from intermediate.operator_stack import OperatorStack
from intermediate.type_stack import TypeStack
from semantic.semantic_cube import get_result_type, TYPES


class QuadrupleManager:
    def __init__(self):
        self._quadruples = []
        self._temp_count = 0

        self.operand_stack  = OperandStack()
        self.operator_stack = OperatorStack()
        self.type_stack     = TypeStack()

    # ── Temporales ────────────────────────────────────────────────────

    def new_temp(self):
        self._temp_count += 1
        return f't{self._temp_count}'

    # ── Emisión de cuádruplos ─────────────────────────────────────────

    def emit(self, op, left, right, result):
        self._quadruples.append(Quadruple(op, left, right, result))

    # ── Operaciones con pilas ─────────────────────────────────────────

    def push_operand(self, operand, operand_type):
        self.operand_stack.push(operand)
        self.type_stack.push(operand_type)

    def pop_operand(self):
        """Saca y regresa (operand, type)."""
        return self.operand_stack.pop(), self.type_stack.pop()

    def peek_type(self):
        return self.type_stack.top()

    # ── Generación de operación binaria ──────────────────────────────

    def generate_operation(self, op):
        """
        Saca dos operandos de las pilas, valida tipos con el cubo
        semántico, emite el cuádruplo y empuja el temporal resultado.
        Regresa el nombre del temporal.
        """
        right, right_type = self.pop_operand()
        left,  left_type  = self.pop_operand()

        result_type = get_result_type(left_type, op, right_type)
        if result_type == TYPES.ERROR:
            raise Exception(
                f'Type mismatch: {left_type} {op} {right_type}'
            )

        temp = self.new_temp()
        self.emit(op, left, right, temp)
        self.push_operand(temp, result_type)
        return temp

    # ── Asignación ────────────────────────────────────────────────────

    def emit_assignment(self, var_name):
        """Saca el tope de la pila y emite  (=, operand, _, var_name)."""
        operand, _ = self.pop_operand()
        self.emit('=', operand, None, var_name)

    # ── Acceso a la cola ──────────────────────────────────────────────

    def get_quadruples(self):
        return list(self._quadruples)

    def count(self):
        return len(self._quadruples)

    def print_quadruples(self):
        if not self._quadruples:
            print('  (sin cuadruplos generados)')
            return
        print(f"\n  {'#':<5} {'OP':<10} {'IZQ':<15} {'DER':<15} {'RES'}")
        print('  ' + '-' * 52)
        for i, q in enumerate(self._quadruples):
            left   = str(q.left)   if q.left   is not None else '_'
            right  = str(q.right)  if q.right  is not None else '_'
            result = str(q.result) if q.result is not None else '_'
            print(f'  {i:<5} {str(q.op):<10} {left:<15} {right:<15} {result}')
