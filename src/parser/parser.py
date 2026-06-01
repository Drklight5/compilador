import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from sly import Parser
from lexico.lexer import PatitoLexer
from semantic.semantic_cube import TYPES
from semantic.function_directory import FunctionDirectory
from semantic.semantic_actions import SemanticActions
from intermediate.virtual_memory import VirtualMemory
from intermediate.quadruple_manager import QuadrupleManager


class PatitoParser(Parser):

    tokens = PatitoLexer.tokens

    def __init__(self):
        self.vm       = VirtualMemory()
        self.func_dir = FunctionDirectory()
        self.actions  = SemanticActions(self.func_dir, self.vm)
        self.qm       = QuadrupleManager(self.vm)
        # Cuádruplo 0: Goto al inicio del programa principal
        # (saltará sobre las definiciones de funciones)
        self.qm.emit('Goto', None, None, None)

    # ------------------------------------------------------------------ #
    #  <PROGRAMA>  — dividido en dos producciones para el backpatch       #
    # ------------------------------------------------------------------ #

    # IMPORTANTE: esta producción debe ir PRIMERO para que SLY la tome
    # como símbolo de inicio de la gramática.
    @_('prog_inicio cuerpo FIN')
    def programa(self, p):
        self.qm.emit('HALT', None, None, None)
        return ('programa', p.prog_inicio)

    # Marcador: consume hasta INICIO y hace el backpatch del Goto inicial
    @_('PROGRAMA ID PUNTO_COMA declaraciones INICIO')
    def prog_inicio(self, p):
        self.qm.fill(0, self.qm.count())   # backpatch cuádruplo 0
        self.vm.reset_temps()               # reiniciar temps para el main
        return p.ID

    # ------------------------------------------------------------------ #
    #  <DECLARACIONES>                                                    #
    # ------------------------------------------------------------------ #
    @_('vars funcs')
    def declaraciones(self, p):
        pass

    # ------------------------------------------------------------------ #
    #  <VARS>                                                             #
    # ------------------------------------------------------------------ #
    @_('VARS lista_vars')
    def vars(self, p):
        pass

    @_('empty')
    def vars(self, p):
        pass

    # ------------------------------------------------------------------ #
    #  <LISTA_VARS>                                                       #
    # ------------------------------------------------------------------ #
    @_('ID lista_ids DOS_PUNTOS tipo PUNTO_COMA lista_vars')
    def lista_vars(self, p):
        for var_name in [p.ID] + p.lista_ids:
            self.actions.declare_variable(var_name, p.tipo)

    @_('empty')
    def lista_vars(self, p):
        pass

    # ------------------------------------------------------------------ #
    #  <LISTA_IDS>                                                        #
    # ------------------------------------------------------------------ #
    @_('COMA ID lista_ids')
    def lista_ids(self, p):
        return [p.ID] + p.lista_ids

    @_('empty')
    def lista_ids(self, p):
        return []

    # ------------------------------------------------------------------ #
    #  <TIPO>                                                             #
    # ------------------------------------------------------------------ #
    @_('ENTERO')
    def tipo(self, p):
        return TYPES.INT

    @_('FLOTANTE')
    def tipo(self, p):
        return TYPES.FLOAT

    # ------------------------------------------------------------------ #
    #  <FUNCS>                                                            #
    # ------------------------------------------------------------------ #
    @_('funcion funcs')
    def funcs(self, p):
        pass

    @_('empty')
    def funcs(self, p):
        pass

    # ------------------------------------------------------------------ #
    #  <FUNCION>                                                          #
    # ------------------------------------------------------------------ #
    @_('retorno ID')
    def funcion_cabecera(self, p):
        self.actions.enter_function(p.ID, p.retorno)
        # Registrar start_address antes de compilar el cuerpo
        self.func_dir.get_function(p.ID).start_address = self.qm.count()
        return (p.retorno, p.ID)

    @_('funcion_cabecera PAR_IZQ params_opc PAR_DER LLAVE_IZQ vars cuerpo LLAVE_DER PUNTO_COMA')
    def funcion(self, p):
        self.qm.emit('ENDFUNC', None, None, None)
        self.actions.exit_function()

    # ------------------------------------------------------------------ #
    #  <RETORNO>                                                          #
    # ------------------------------------------------------------------ #
    @_('NULA')
    def retorno(self, p):
        return TYPES.NULL

    @_('tipo')
    def retorno(self, p):
        return p.tipo

    # ------------------------------------------------------------------ #
    #  <PARAMS_OPC>                                                       #
    # ------------------------------------------------------------------ #
    @_('lista_params')
    def params_opc(self, p):
        return p.lista_params

    @_('empty')
    def params_opc(self, p):
        return []

    # ------------------------------------------------------------------ #
    #  <LISTA_PARAMS>                                                     #
    # ------------------------------------------------------------------ #
    @_('ID DOS_PUNTOS tipo mas_params')
    def lista_params(self, p):
        self.actions.declare_parameter(p.ID, p.tipo)
        return [('param', p.ID, p.tipo)] + p.mas_params

    # ------------------------------------------------------------------ #
    #  <MAS_PARAMS>                                                       #
    # ------------------------------------------------------------------ #
    @_('COMA ID DOS_PUNTOS tipo mas_params')
    def mas_params(self, p):
        self.actions.declare_parameter(p.ID, p.tipo)
        return [('param', p.ID, p.tipo)] + p.mas_params

    @_('empty')
    def mas_params(self, p):
        return []

    # ------------------------------------------------------------------ #
    #  <CUERPO>                                                           #
    # ------------------------------------------------------------------ #
    @_('LLAVE_IZQ estatutos LLAVE_DER')
    def cuerpo(self, p):
        pass

    # ------------------------------------------------------------------ #
    #  <ESTATUTOS>                                                        #
    # ------------------------------------------------------------------ #
    @_('estatuto estatutos')
    def estatutos(self, p):
        pass

    @_('empty')
    def estatutos(self, p):
        pass

    # ------------------------------------------------------------------ #
    #  <ESTATUTO>                                                         #
    # ------------------------------------------------------------------ #
    @_('ID estatuto_id')
    def estatuto(self, p):
        kind = p.estatuto_id[0] if isinstance(p.estatuto_id, tuple) else None

        if kind == 'asigna':
            expr_type = self.qm.peek_type()
            var = self.actions.lookup_variable(p.ID)
            self.actions.validate_assignment(var.type, expr_type)
            self.qm.emit_assignment(var.address)

        elif kind == 'llamada_estat':
            _, args_tuple = p.estatuto_id[1]    # ('args', [(addr,type),...])
            arg_types = [t for _, t in args_tuple]
            self.actions.validate_call(p.ID, arg_types)
            func = self.actions.lookup_function(p.ID)
            self.qm.emit('ERA', p.ID, None, None)
            for i, (arg_addr, _) in enumerate(args_tuple):
                self.qm.emit('PARAM', arg_addr, None, i + 1)
            self.qm.emit('GOSUB', p.ID, None, func.start_address)

    @_('condicion')
    def estatuto(self, p):
        pass

    @_('ciclo')
    def estatuto(self, p):
        pass

    @_('imprime')
    def estatuto(self, p):
        pass

    @_('bloque')
    def estatuto(self, p):
        pass

    @_('retorna')
    def estatuto(self, p):
        pass

    # ------------------------------------------------------------------ #
    #  <RETORNA>                                                          #
    # ------------------------------------------------------------------ #
    @_('REGRESA retorna_valor PUNTO_COMA')
    def retorna(self, p):
        if p.retorna_valor is not None:
            val_addr, expr_type = self.qm.pop_operand()
            self.actions.validate_return(expr_type)
            func = self.func_dir.get_function(self.actions.current_scope)
            self.qm.emit('RETURN', val_addr, None, func.return_address)
        else:
            self.actions.validate_return(None)
            self.qm.emit('RETURN', None, None, None)

    @_('expresion')
    def retorna_valor(self, p):
        return p.expresion

    @_('empty')
    def retorna_valor(self, p):
        return None

    # ------------------------------------------------------------------ #
    #  <BLOQUE>                                                           #
    # ------------------------------------------------------------------ #
    @_('CORCH_IZQ estatutos CORCH_DER')
    def bloque(self, p):
        pass

    # ------------------------------------------------------------------ #
    #  <ESTATUTO_ID>                                                      #
    # ------------------------------------------------------------------ #
    @_('asigna')
    def estatuto_id(self, p):
        return p.asigna

    @_('llamada PUNTO_COMA')
    def estatuto_id(self, p):
        return ('llamada_estat', p.llamada)

    # ------------------------------------------------------------------ #
    #  <ASIGNA>                                                           #
    # ------------------------------------------------------------------ #
    @_('OP_ASIG expresion PUNTO_COMA')
    def asigna(self, p):
        return ('asigna', p.expresion)

    # ------------------------------------------------------------------ #
    #  <LLAMADA>                                                          #
    # ------------------------------------------------------------------ #
    @_('PAR_IZQ args_opc PAR_DER')
    def llamada(self, p):
        return ('args', p.args_opc)

    # ------------------------------------------------------------------ #
    #  <CONDICION>  — marcadores para backpatch de saltos                 #
    # ------------------------------------------------------------------ #

    # Marcador: después de evaluar la condición, emite GotoF pendiente
    @_('SI PAR_IZQ expresion PAR_DER')
    def si_cond(self, p):
        cond_addr, cond_type = self.qm.pop_operand()
        self.actions.validate_condition(cond_type)
        idx = self.qm.count()
        self.qm.emit('GotoF', cond_addr, None, None)   # destino pendiente
        self.qm.jump_stack.push(idx)

    @_('si_cond cuerpo sino_opc PUNTO_COMA')
    def condicion(self, p):
        pass

    # ------------------------------------------------------------------ #
    #  <SINO_OPC>                                                         #
    # ------------------------------------------------------------------ #

    # Marcador vacío: entre el bloque verdadero y el bloque sino
    # Emite Goto (salto al final), hace backpatch del GotoF
    @_('')
    def sino_inicio(self, p):
        goto_idx = self.qm.count()
        self.qm.emit('Goto', None, None, None)          # saltar sobre sino
        gotof_idx = self.qm.jump_stack.pop()
        self.qm.fill(gotof_idx, self.qm.count())        # backpatch GotoF
        self.qm.jump_stack.push(goto_idx)

    @_('SINO sino_inicio cuerpo')
    def sino_opc(self, p):
        goto_idx = self.qm.jump_stack.pop()
        self.qm.fill(goto_idx, self.qm.count())         # backpatch Goto

    @_('empty')
    def sino_opc(self, p):
        gotof_idx = self.qm.jump_stack.pop()
        self.qm.fill(gotof_idx, self.qm.count())        # backpatch GotoF

    # ------------------------------------------------------------------ #
    #  <CICLO>  — marcadores para backpatch                               #
    # ------------------------------------------------------------------ #

    # Marcador: antes de la condición, guarda el índice de inicio
    @_('MIENTRAS')
    def mientras_inicio(self, p):
        self.qm.jump_stack.push(self.qm.count())        # índice de inicio

    # Marcador: después de la condición, emite GotoF
    @_('mientras_inicio PAR_IZQ expresion PAR_DER')
    def mientras_cond(self, p):
        cond_addr, cond_type = self.qm.pop_operand()
        self.actions.validate_condition(cond_type)
        idx = self.qm.count()
        self.qm.emit('GotoF', cond_addr, None, None)    # destino pendiente
        self.qm.jump_stack.push(idx)

    @_('mientras_cond HAZ cuerpo PUNTO_COMA')
    def ciclo(self, p):
        gotof_idx  = self.qm.jump_stack.pop()
        start_idx  = self.qm.jump_stack.pop()
        self.qm.emit('Goto', None, None, start_idx)     # regresar al inicio
        self.qm.fill(gotof_idx, self.qm.count())        # backpatch GotoF

    # ------------------------------------------------------------------ #
    #  <IMPRIME>                                                          #
    # ------------------------------------------------------------------ #
    @_('ESCRIBE PAR_IZQ lista_imp PAR_DER PUNTO_COMA')
    def imprime(self, p):
        for item in p.lista_imp:
            self.qm.emit('PRINT', item, None, None)

    # ------------------------------------------------------------------ #
    #  <LISTA_IMP>                                                        #
    # ------------------------------------------------------------------ #
    @_('LETRERO mas_imp')
    def lista_imp(self, p):
        addr = self.vm.get_constant(p.LETRERO, TYPES.STRING)
        return [addr] + p.mas_imp

    @_('expresion mas_imp')
    def lista_imp(self, p):
        operand, _ = self.qm.pop_operand()
        return [operand] + p.mas_imp

    # ------------------------------------------------------------------ #
    #  <MAS_IMP>                                                          #
    # ------------------------------------------------------------------ #
    @_('COMA lista_imp')
    def mas_imp(self, p):
        return p.lista_imp

    @_('empty')
    def mas_imp(self, p):
        return []

    # ------------------------------------------------------------------ #
    #  <ARGS_OPC>                                                         #
    # ------------------------------------------------------------------ #
    @_('lista_args')
    def args_opc(self, p):
        return p.lista_args

    @_('empty')
    def args_opc(self, p):
        return []

    # ------------------------------------------------------------------ #
    #  <LISTA_ARGS>                                                       #
    # ------------------------------------------------------------------ #
    @_('expresion mas_args')
    def lista_args(self, p):
        operand, op_type = self.qm.pop_operand()
        return [(operand, op_type)] + p.mas_args

    # ------------------------------------------------------------------ #
    #  <MAS_ARGS>                                                         #
    # ------------------------------------------------------------------ #
    @_('COMA expresion mas_args')
    def mas_args(self, p):
        operand, op_type = self.qm.pop_operand()
        return [(operand, op_type)] + p.mas_args

    @_('empty')
    def mas_args(self, p):
        return []

    # ------------------------------------------------------------------ #
    #  <EXPRESION>                                                        #
    # ------------------------------------------------------------------ #
    @_('exp_rel')
    def expresion(self, p):
        return p.exp_rel

    # ------------------------------------------------------------------ #
    #  <EXP_REL>                                                          #
    # ------------------------------------------------------------------ #
    @_('exp_aditiva exp_rel_prima')
    def exp_rel(self, p):
        if p.exp_rel_prima is None:
            return p.exp_aditiva
        return self.qm.generate_operation(p.exp_rel_prima)

    @_('OP_REL exp_aditiva')
    def exp_rel_prima(self, p):
        return p.OP_REL

    @_('empty')
    def exp_rel_prima(self, p):
        return None

    # ------------------------------------------------------------------ #
    #  <EXP_ADITIVA>  — izquierda-recursiva                              #
    # ------------------------------------------------------------------ #
    @_('exp_aditiva OP_ADD termino')
    def exp_aditiva(self, p):
        return self.qm.generate_operation(p.OP_ADD)

    @_('termino')
    def exp_aditiva(self, p):
        return p.termino

    # ------------------------------------------------------------------ #
    #  <TERMINO>  — izquierda-recursiva                                  #
    # ------------------------------------------------------------------ #
    @_('termino OP_MUL factor')
    def termino(self, p):
        return self.qm.generate_operation(p.OP_MUL)

    @_('factor')
    def termino(self, p):
        return p.factor

    # ------------------------------------------------------------------ #
    #  <FACTOR>                                                           #
    # ------------------------------------------------------------------ #
    @_('PAR_IZQ expresion PAR_DER')
    def factor(self, p):
        return p.expresion

    @_('OP_ADD factor')
    def factor(self, p):
        if p.OP_ADD == '-':
            operand, op_type = self.qm.pop_operand()
            temp = self.qm.new_temp(op_type)
            self.qm.emit('UMINUS', operand, None, temp)
            self.qm.push_operand(temp, op_type)
            return temp
        return p.factor

    @_('ID llamada_opc')
    def factor(self, p):
        if p.llamada_opc is None:
            var = self.actions.lookup_variable(p.ID)
            self.qm.push_operand(var.address, var.type)
            return var.address

        # Llamada a función como expresión
        func = self.actions.lookup_function(p.ID)
        arg_types = [t for _, t in p.llamada_opc]
        self.actions.validate_call(p.ID, arg_types)

        self.qm.emit('ERA', p.ID, None, None)
        for i, (arg_addr, _) in enumerate(p.llamada_opc):
            self.qm.emit('PARAM', arg_addr, None, i + 1)
        self.qm.emit('GOSUB', p.ID, None, func.start_address)

        # Temporal para recoger el valor de retorno
        temp = self.qm.new_temp(func.return_type)
        self.qm.emit('=', func.return_address, None, temp)
        self.qm.push_operand(temp, func.return_type)
        return temp

    @_('CTE_ENT')
    def factor(self, p):
        val  = int(p.CTE_ENT)
        addr = self.vm.get_constant(val, TYPES.INT)
        self.qm.push_operand(addr, TYPES.INT)
        return addr

    @_('CTE_FLOT')
    def factor(self, p):
        val  = float(p.CTE_FLOT)
        addr = self.vm.get_constant(val, TYPES.FLOAT)
        self.qm.push_operand(addr, TYPES.FLOAT)
        return addr

    # ------------------------------------------------------------------ #
    #  <LLAMADA_OPC>                                                      #
    # ------------------------------------------------------------------ #
    @_('PAR_IZQ args_opc PAR_DER')
    def llamada_opc(self, p):
        return p.args_opc

    @_('empty')
    def llamada_opc(self, p):
        return None

    # ------------------------------------------------------------------ #
    #  Producción vacía                                                   #
    # ------------------------------------------------------------------ #
    @_('')
    def empty(self, p):
        pass

    # ------------------------------------------------------------------ #
    #  ERROR                                                              #
    # ------------------------------------------------------------------ #
    def error(self, token):
        if token:
            print(
                f"[PARSER ERROR] Token inesperado '{token.value}' "
                f"(tipo: {token.type}) en linea {token.lineno}"
            )
        else:
            print("[PARSER ERROR] Fin de archivo inesperado")


def parse(source):
    lexer  = PatitoLexer()
    parser = PatitoParser()
    try:
        result = parser.parse(lexer.tokenize(source))
        return result, parser
    except Exception as e:
        print(f'[SEMANTIC ERROR] {e}')
        return None, None
