from sly import Lexer


class PatitoLexer(Lexer):

    # -------------------------
    # TOKENS
    # -------------------------
 
    tokens = {
        # Identificadores y literales
        ID,
        CTE_ENT,
        CTE_FLOT,
        LETRERO,

        # Operadores
        OP_ASIG,
        OP_ADD,
        OP_MUL,
        OP_REL,

        # Delimitadores
        PUNTO_COMA,
        COMA,
        DOS_PUNTOS,

        PAR_IZQ,
        PAR_DER,

        LLAVE_IZQ,
        LLAVE_DER,

        CORCH_IZQ,
        CORCH_DER,

        # Palabras reservadas
        PROGRAMA,
        VARS,
        INICIO,
        FIN,

        ENTERO,
        FLOTANTE,

        ESCRIBE,

        MIENTRAS,
        HAZ,

        SI,
        SINO,

        NULA
    }

    # -------------------------
    # IGNORAR
    # -------------------------

    ignore = ' \t'

    ignore_comment = r'//.*'

    # -------------------------
    # TOKENS SIMPLES
    # -------------------------

    OP_ASIG = r'='
    OP_ADD = r'\+|-'
    OP_MUL = r'\*|/'
    OP_REL = r'==|!=|>|<'

    PUNTO_COMA = r';'
    COMA = r','
    DOS_PUNTOS = r':'

    PAR_IZQ = r'\('
    PAR_DER = r'\)'

    LLAVE_IZQ = r'\{'
    LLAVE_DER = r'\}'

    CORCH_IZQ = r'\['
    CORCH_DER = r'\]'

    # -------------------------
    # PALABRAS RESERVADAS
    # -------------------------

    ID = r'[a-zA-Z_][a-zA-Z0-9_]*'

    ID['programa'] = PROGRAMA
    ID['vars'] = VARS
    ID['inicio'] = INICIO
    ID['fin'] = FIN

    ID['entero'] = ENTERO
    ID['flotante'] = FLOTANTE

    ID['escribe'] = ESCRIBE

    ID['mientras'] = MIENTRAS
    ID['haz'] = HAZ

    ID['si'] = SI
    ID['sino'] = SINO

    ID['nula'] = NULA

    # -------------------------
    # CONSTANTES
    # -------------------------

    @_(r'\d+\.\d+')
    def CTE_FLOT(self, t):
        t.value = float(t.value)
        return t

    @_(r'\d+')
    def CTE_ENT(self, t):
        t.value = int(t.value)
        return t

    @_(r'"([^"\\\\]|\\\\.)*"')
    def LETRERO(self, t):
        return t

    # -------------------------
    # SALTOS DE LINEA
    # -------------------------

    @_(r'\n+')
    def ignore_newline(self, t):
        self.lineno += len(t.value)

    # -------------------------
    # ERRORES
    # -------------------------

    def error(self, t):
        print(f'Caracter ilegal: {t.value[0]}')
        self.index += 1
        
def tokenize(source: str) -> list:
    lexer = PatitoLexer()
    return list(lexer.tokenize(source))


# Código de prueba para el lexer
if __name__ == '__main__':
    codigo = """
    programa miProg;
    vars
        x, y : entero;
        resultado : flotante;
    inicio
    {
        x = 10;
        y = 20;
        resultado = x + y * 2.5;
 
        si (x > y) {
            escribe("x es mayor", x);
        } sino {
            escribe("y es mayor o igual");
        };
 
        mientras (x != 0) haz {
            x = x - 1;
        };
    }
    fin
    """
 
    lexer = PatitoLexer()
    print(f"{'TOKEN':<15} {'VALOR':<20} {'LÍNEA'}")
    print("-" * 45)
    for tok in lexer.tokenize(codigo):
        print(f"{tok.type:<15} {str(tok.value):<20} {tok.lineno}")