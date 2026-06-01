import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from sly import Parser
from lexico.lexer import PatitoLexer
from semantic.semantic_cube import TYPES
from semantic.function_directory import FunctionDirectory
from semantic.semantic_actions import SemanticActions


class PatitoParser(Parser):

    tokens = PatitoLexer.tokens

    def __init__(self):
        self.func_dir = FunctionDirectory()
        self.actions = SemanticActions(self.func_dir)

    # ------------------------------------------------------------------ #
    #  <PROGRAMA>                                                         #
    # ------------------------------------------------------------------ #
    @_('PROGRAMA ID PUNTO_COMA declaraciones INICIO cuerpo FIN')
    def programa(self, p):
        return make_node(
            'programa',
            value=p.ID,
            children=[p.declaraciones, p.cuerpo]
        )

    # ------------------------------------------------------------------ #
    #  <DECLARACIONES>                                                    #
    # ------------------------------------------------------------------ #
    @_('vars funcs')
    def declaraciones(self, p):
        return make_node('declaraciones', children=[p.vars, p.funcs])

    # ------------------------------------------------------------------ #
    #  <VARS>                                                             #
    # ------------------------------------------------------------------ #
    @_('VARS lista_vars')
    def vars(self, p):
        return make_node('vars', children=p.lista_vars)

    @_('empty')
    def vars(self, p):
        return make_node('vars')

    # ------------------------------------------------------------------ #
    #  <LISTA_VARS>                                                       #
    # ------------------------------------------------------------------ #
    @_('ID lista_ids DOS_PUNTOS tipo PUNTO_COMA lista_vars')
    def lista_vars(self, p):
        ids = [p.ID] + p.lista_ids
        declarations = []
        for var_name in ids:
            self.actions.declare_variable(var_name, p.tipo)
            declarations.append(
                make_node('var_decl', node_type=p.tipo, value=var_name)
            )
        return declarations + p.lista_vars

    @_('empty')
    def lista_vars(self, p):
        return []

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
        return [p.funcion] + p.funcs

    @_('empty')
    def funcs(self, p):
        return []

    # ------------------------------------------------------------------ #
    #  <FUNCION>                                                          #
    # ------------------------------------------------------------------ #

    # Marcador: dispara enter_function + cambio de scope antes de parsear
    # parámetros y cuerpo, para que ambos vean el scope correcto.
    @_('retorno ID')
    def funcion_cabecera(self, p):
        self.actions.enter_function(p.ID, p.retorno)
        return (p.retorno, p.ID)

    @_('funcion_cabecera PAR_IZQ params_opc PAR_DER LLAVE_IZQ vars cuerpo LLAVE_DER PUNTO_COMA')
    def funcion(self, p):
        ret_type, name = p.funcion_cabecera
        self.actions.exit_function()
        return make_node(
            'function',
            node_type=ret_type,
            value=name,
            children=[p.params_opc, p.vars, p.cuerpo]
        )

    # ------------------------------------------------------------------ #
    #  <RETORNO>  (tipo de retorno de función)                           #
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
        return make_node('body', children=p.estatutos)

    # ------------------------------------------------------------------ #
    #  <ESTATUTOS>                                                        #
    # ------------------------------------------------------------------ #
    @_('estatuto estatutos')
    def estatutos(self, p):
        return [p.estatuto] + p.estatutos

    @_('empty')
    def estatutos(self, p):
        return []

    # ------------------------------------------------------------------ #
    #  <ESTATUTO>                                                         #
    # ------------------------------------------------------------------ #
    @_('ID estatuto_id')
    def estatuto(self, p):
        kind = p.estatuto_id[0] if isinstance(p.estatuto_id, tuple) else None
        if kind == 'asigna':
            expr = p.estatuto_id[1]
            var = self.actions.lookup_variable(p.ID)
            self.actions.validate_assignment(var.type, expr['type'])
        elif kind == 'llamada_estat':
            _, llamada = p.estatuto_id
            _, args = llamada
            arg_types = [a['type'] for a in args]
            self.actions.validate_call(p.ID, arg_types)
        return ('estatuto_id', p.ID, p.estatuto_id)

    @_('condicion')
    def estatuto(self, p):
        return p.condicion

    @_('ciclo')
    def estatuto(self, p):
        return p.ciclo

    @_('imprime')
    def estatuto(self, p):
        return p.imprime

    @_('bloque')
    def estatuto(self, p):
        return p.bloque

    @_('retorna')
    def estatuto(self, p):
        return p.retorna

    # ------------------------------------------------------------------ #
    #  <RETORNA>  (estatuto de retorno)                                  #
    # ------------------------------------------------------------------ #
    @_('REGRESA retorna_valor PUNTO_COMA')
    def retorna(self, p):
        expr_type = p.retorna_valor['type'] if p.retorna_valor else None
        self.actions.validate_return(expr_type)
        return make_node(
            'retorna',
            children=[p.retorna_valor] if p.retorna_valor else []
        )

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
        return ('bloque', p.estatutos)

    # ------------------------------------------------------------------ #
    #  <ESTATUTO_ID>  — distingue asignación de llamada a función        #
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
    #  <LLAMADA>  — se usa como expresión o como estatuto                #
    # ------------------------------------------------------------------ #
    @_('PAR_IZQ args_opc PAR_DER')
    def llamada(self, p):
        return ('args', p.args_opc)

    # ------------------------------------------------------------------ #
    #  <CONDICION>                                                        #
    # ------------------------------------------------------------------ #
    @_('SI PAR_IZQ expresion PAR_DER cuerpo sino_opc PUNTO_COMA')
    def condicion(self, p):
        self.actions.validate_condition(p.expresion['type'])
        return ('si', p.expresion, p.cuerpo, p.sino_opc)

    # ------------------------------------------------------------------ #
    #  <SINO_OPC>                                                         #
    # ------------------------------------------------------------------ #
    @_('SINO cuerpo')
    def sino_opc(self, p):
        return ('sino', p.cuerpo)

    @_('empty')
    def sino_opc(self, p):
        return None

    # ------------------------------------------------------------------ #
    #  <CICLO>                                                            #
    # ------------------------------------------------------------------ #
    @_('MIENTRAS PAR_IZQ expresion PAR_DER HAZ cuerpo PUNTO_COMA')
    def ciclo(self, p):
        self.actions.validate_condition(p.expresion['type'])
        return ('mientras', p.expresion, p.cuerpo)

    # ------------------------------------------------------------------ #
    #  <IMPRIME>                                                          #
    # ------------------------------------------------------------------ #
    @_('ESCRIBE PAR_IZQ lista_imp PAR_DER PUNTO_COMA')
    def imprime(self, p):
        return ('escribe', p.lista_imp)

    # ------------------------------------------------------------------ #
    #  <LISTA_IMP>                                                        #
    # ------------------------------------------------------------------ #
    @_('LETRERO mas_imp')
    def lista_imp(self, p):
        return [('letrero', p.LETRERO)] + p.mas_imp

    @_('expresion mas_imp')
    def lista_imp(self, p):
        return [p.expresion] + p.mas_imp

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
        return [p.expresion] + p.mas_args

    # ------------------------------------------------------------------ #
    #  <MAS_ARGS>                                                         #
    # ------------------------------------------------------------------ #
    @_('COMA expresion mas_args')
    def mas_args(self, p):
        return [p.expresion] + p.mas_args

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
        op, derecha = p.exp_rel_prima
        result_type = self.actions.validate_operation(
            p.exp_aditiva['type'], op, derecha['type']
        )
        return make_node('rel_op', node_type=result_type, value=op,
                         children=[p.exp_aditiva, derecha])

    # ------------------------------------------------------------------ #
    #  <EXP_REL_PRIMA>                                                    #
    # ------------------------------------------------------------------ #
    @_('OP_REL exp_aditiva')
    def exp_rel_prima(self, p):
        return (p.OP_REL, p.exp_aditiva)

    @_('empty')
    def exp_rel_prima(self, p):
        return None

    # ------------------------------------------------------------------ #
    #  <EXP_ADITIVA>                                                      #
    # ------------------------------------------------------------------ #
    @_('termino exp_aditiva_prima')
    def exp_aditiva(self, p):
        if p.exp_aditiva_prima is None:
            return p.termino
        op, derecha = p.exp_aditiva_prima
        result_type = self.actions.validate_operation(
            p.termino['type'], op, derecha['type']
        )
        return make_node('add_op', node_type=result_type, value=op,
                         children=[p.termino, derecha])

    # ------------------------------------------------------------------ #
    #  <EXP_ADITIVA_PRIMA>                                                #
    # ------------------------------------------------------------------ #
    @_('OP_ADD termino exp_aditiva_prima')
    def exp_aditiva_prima(self, p):
        if p.exp_aditiva_prima is None:
            return (p.OP_ADD, p.termino)
        op2, derecha2 = p.exp_aditiva_prima
        return (p.OP_ADD, ('op_add', op2, p.termino, derecha2))

    @_('empty')
    def exp_aditiva_prima(self, p):
        return None

    # ------------------------------------------------------------------ #
    #  <TERMINO>                                                          #
    # ------------------------------------------------------------------ #
    @_('factor termino_prima')
    def termino(self, p):
        if p.termino_prima is None:
            return p.factor
        op, derecha = p.termino_prima
        result_type = self.actions.validate_operation(
            p.factor['type'], op, derecha['type']
        )
        return make_node('mul_op', node_type=result_type, value=op,
                         children=[p.factor, derecha])

    # ------------------------------------------------------------------ #
    #  <TERMINO_PRIMA>                                                    #
    # ------------------------------------------------------------------ #
    @_('OP_MUL factor termino_prima')
    def termino_prima(self, p):
        if p.termino_prima is None:
            return (p.OP_MUL, p.factor)
        op2, derecha2 = p.termino_prima
        return (p.OP_MUL, ('op_mul', op2, p.factor, derecha2))

    @_('empty')
    def termino_prima(self, p):
        return None

    # ------------------------------------------------------------------ #
    #  <FACTOR>                                                           #
    # ------------------------------------------------------------------ #
    @_('PAR_IZQ expresion PAR_DER')
    def factor(self, p):
        return make_node('group', node_type=p.expresion['type'],
                         children=[p.expresion])

    @_('OP_ADD factor')
    def factor(self, p):
        return make_node('sign', node_type=p.factor['type'],
                         value=p.OP_ADD, children=[p.factor])

    @_('ID llamada_opc')
    def factor(self, p):
        if p.llamada_opc is None:
            var = self.actions.lookup_variable(p.ID)
            return make_node('id', node_type=var.type, value=p.ID)
        func = self.actions.lookup_function(p.ID)
        arg_types = [a['type'] for a in p.llamada_opc]
        self.actions.validate_call(p.ID, arg_types)
        return make_node('function_call', node_type=func.return_type,
                         value=p.ID, children=p.llamada_opc)

    @_('CTE_ENT')
    def factor(self, p):
        return make_node('cte_int', node_type=TYPES.INT, value=int(p.CTE_ENT))

    @_('CTE_FLOT')
    def factor(self, p):
        return make_node('cte_float', node_type=TYPES.FLOAT, value=float(p.CTE_FLOT))

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
    #  Producción vacía auxiliar                                          #
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
                f"(tipo: {token.type}) en línea {token.lineno}"
            )
        else:
            print("[PARSER ERROR] Fin de archivo inesperado")


def make_node(node, node_type=None, value=None, children=None):
    return {
        'node': node,
        'type': node_type,
        'value': value,
        'children': children or []
    }


def parse(source):
    lexer = PatitoLexer()
    parser = PatitoParser()
    try:
        tokens = lexer.tokenize(source)
        return parser.parse(tokens)
    except Exception as e:
        print(f'[SEMANTIC ERROR] {e}')
