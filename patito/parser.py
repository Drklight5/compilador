from sly import Parser
from lexer import PatitoLexer


class PatitoParser(Parser):

    tokens = PatitoLexer.tokens

    # ------------------------------------------------------------------ #
    #  <PROGRAMA>                                                         #
    # ------------------------------------------------------------------ #
    @_('PROGRAMA ID PUNTO_COMA declaraciones INICIO cuerpo FIN')
    def programa(self, p):
        return ('programa', p.ID, p.declaraciones, p.cuerpo)
 
    # ------------------------------------------------------------------ #
    #  <DECLARACIONES>                                                    #
    # ------------------------------------------------------------------ #
    @_('vars funcs')
    def declaraciones(self, p):
        return ('declaraciones', p.vars, p.funcs)
 
    # ------------------------------------------------------------------ #
    #  <VARS>                                                             #
    # ------------------------------------------------------------------ #
    @_('VARS lista_vars')
    def vars(self, p):
        return ('vars', p.lista_vars)
 
    @_('empty')
    def vars(self, p):
        return ('vars', [])
 
    # ------------------------------------------------------------------ #
    #  <LISTA_VARS>                                                       #
    # ------------------------------------------------------------------ #
    @_('ID lista_ids DOS_PUNTOS tipo PUNTO_COMA lista_vars')
    def lista_vars(self, p):
        ids = [p.ID] + p.lista_ids
        return [('decl', ids, p.tipo)] + p.lista_vars
 
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
        return 'entero'
 
    @_('FLOTANTE')
    def tipo(self, p):
        return 'flotante'
 
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
    @_('retorno ID PAR_IZQ params_opc PAR_DER LLAVE_IZQ vars cuerpo LLAVE_DER PUNTO_COMA')
    def funcion(self, p):
        return ('funcion', p.retorno, p.ID, p.params_opc, p.vars, p.cuerpo)
 
    # ------------------------------------------------------------------ #
    #  <RETORNO>                                                          #
    # ------------------------------------------------------------------ #
    @_('NULA')
    def retorno(self, p):
        return 'nula'
 
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
        return [('param', p.ID, p.tipo)] + p.mas_params
 
    # ------------------------------------------------------------------ #
    #  <MAS_PARAMS>                                                       #
    # ------------------------------------------------------------------ #
    @_('COMA ID DOS_PUNTOS tipo mas_params')
    def mas_params(self, p):
        return [('param', p.ID, p.tipo)] + p.mas_params
 
    @_('empty')
    def mas_params(self, p):
        return []
 
    # ------------------------------------------------------------------ #
    #  <CUERPO>                                                           #
    # ------------------------------------------------------------------ #
    @_('LLAVE_IZQ estatutos LLAVE_DER')
    def cuerpo(self, p):
        return ('cuerpo', p.estatutos)
 
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
 
    # ------------------------------------------------------------------ #
    #  <BLOQUE>                                                           #
    # ------------------------------------------------------------------ #
    @_('CORCH_IZQ estatutos CORCH_DER')
    def bloque(self, p):
        return ('bloque', p.estatutos)
 
    # ------------------------------------------------------------------ #
    #  <ESTATUTO_ID>  — distingue asignación de llamada a función         #
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
    #  <LLAMADA>  — se usa como expresión o como estatuto                 #
    # ------------------------------------------------------------------ #
    @_('PAR_IZQ args_opc PAR_DER')
    def llamada(self, p):
        return ('args', p.args_opc)
 
    # ------------------------------------------------------------------ #
    #  <CONDICION>                                                        #
    # ------------------------------------------------------------------ #
    @_('SI PAR_IZQ expresion PAR_DER cuerpo sino_opc PUNTO_COMA')
    def condicion(self, p):
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
        return ('mientras', p.expresion, p.cuerpo)
 
    # ------------------------------------------------------------------ #
    #  <IMPRIME>                                                          #
    # ------------------------------------------------------------------ #
    @_('ESCRIBE PAR_IZQ lista_imp PAR_DER PUNTO_COMA')
    def imprime(self, p):
        return ('escribe', p.lista_imp)
 
    # ------------------------------------------------------------------ #
    #  <LISTA_IMP>  — lista de argumentos para escribe                   #
    #  Cada elemento puede ser un LETRERO o una expresión                 #
    # ------------------------------------------------------------------ #
    @_('LETRERO mas_imp')
    def lista_imp(self, p):
        return [('letrero', p.LETRERO)] + p.mas_imp
 
    @_('expresion mas_imp')
    def lista_imp(self, p):
        return [p.expresion] + p.mas_imp
 
    # ------------------------------------------------------------------ #
    #  <MAS_IMP>  — elementos adicionales separados por coma             #
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
        return ('op_rel', op, p.exp_aditiva, derecha)
 
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
        return ('op_add', op, p.termino, derecha)
 
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
        return ('op_mul', op, p.factor, derecha)
 
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
        return ('grupo', p.expresion)
 
    @_('OP_ADD factor')
    def factor(self, p):
        return ('signo', p.OP_ADD, p.factor)
 
    @_('ID llamada_opc')
    def factor(self, p):
        if p.llamada_opc is None:
            return ('id', p.ID)
        return ('llamada_expr', p.ID, p.llamada_opc)
 
    @_('CTE_ENT')
    def factor(self, p):
        return ('cte_ent', int(p.CTE_ENT))
 
    @_('CTE_FLOT')
    def factor(self, p):
        return ('cte_flot', float(p.CTE_FLOT))
 
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
 

    # -------------------------
    # ERROR
    # -------------------------

    def error(self, token):
        if token:
            print(
                f"[PARSER ERROR] Token inesperado '{token.value}' "
                f"(tipo: {token.type}) en línea {token.lineno}"
            )
        else:
            print("[PARSER ERROR] Fin de archivo inesperado")
            
            
# Función de conveniencia para pruebas
def parse(source: str):
    lexer  = PatitoLexer()
    parser = PatitoParser()
    tokens = lexer.tokenize(source)
    return parser.parse(tokens)
 
 
if __name__ == '__main__':
    import pprint
 
    casos = {
        # ---- programa mínimo válido ----------------------------------- #
        "Programa mínimo": """
            programa minimo;
            inicio
            {
            }
            fin
        """,
 
        # ---- variables y asignación ----------------------------------- #
        "Variables y asignación": """
            programa test_vars;
            vars
                a, b : entero;
                c    : flotante;
            inicio
            {
                a = 5;
                b = 10;
                c = a + b * 2.0;
            }
            fin
        """,
 
        # ---- condicional con sino ------------------------------------- #
        "Condicional": """
            programa cond_test;
            inicio
            {
                si (x > 0) {
                    escribe("positivo");
                } sino {
                    escribe("no positivo");
                };
            }
            fin
        """,
 
        # ---- ciclo mientras ------------------------------------------ #
        "Ciclo mientras": """
            programa ciclo_test;
            vars i : entero;
            inicio
            {
                i = 0;
                mientras (i < 10) haz {
                    i = i + 1;
                };
            }
            fin
        """,
 
        # ---- función con parámetros y llamada ------------------------ #
        # La función tiene su propio cuerpo: { <vars_opt> <cuerpo> }
        # donde <cuerpo> es { estatutos }
        "Función y llamada": """
            programa func_test;
            nula saludar(nombre : entero)
            {
                {
                    escribe("hola", nombre);
                }
            };
            inicio
            {
                saludar(42);
            }
            fin
        """,
 
        # ---- programa completo con todo ----------------------------- #
        "Programa completo": """
            programa completo;
            vars
                x, y : entero;
                res  : flotante;
            entero suma(a : entero, b : entero)
            {
                vars r : entero;
                {
                    r = a + b;
                    escribe("suma =", r);
                }
            };
            inicio
            {
                x = 3;
                y = 7;
                res = suma(x, y);
                si (res > 5) {
                    escribe("grande");
                };
                mientras (x != 0) haz {
                    x = x - 1;
                };
            }
            fin
        """,
    }
 
    for nombre, codigo in casos.items():
        print(f"\n{'='*60}")
        print(f"  {nombre}")
        print('='*60)
        ast = parse(codigo)
        if ast:
            print("  ✅  Análisis sintáctico exitoso")
            pprint.pprint(ast, indent=4, width=80)
        else:
            print("  ❌  Error en el análisis sintáctico")