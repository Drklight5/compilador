#Types
INT = 'entero'
FLOAT = 'flotante'
BOOL = 'bool'
STRING = 'string'
ERROR = 'error'
NULL = 'null'

class TYPES:
    INT = INT
    FLOAT = FLOAT
    BOOL = BOOL
    STRING = STRING
    ERROR = ERROR
    NULL = NULL

#OPERATORS
# suma/resta
# + -

# multiplicación/división
# * /

# relacionales
# > < == !=

# asignación
# =

semantic_cube = {


    # ENTERO
   INT: {

        # SUMA / RESTA

        '+': {
           INT:INT,
           FLOAT:FLOAT
        },

        '-': {
           INT:INT,
           FLOAT:FLOAT
        },

        # MULT / DIV

        '*': {
           INT:INT,
           FLOAT:FLOAT
        },

        '/': {
           INT:FLOAT,
           FLOAT:FLOAT
        },

        # RELACIONALES

        '>': {
           INT: BOOL,
           FLOAT: BOOL
        },

        '<': {
           INT: BOOL,
           FLOAT: BOOL
        },

        '==': {
           INT: BOOL,
           FLOAT: BOOL
        },

        '!=': {
           INT: BOOL,
           FLOAT: BOOL
        },

        # ASIGNACION
        # STRICT

        '=': {
           INT:INT
        }
    },


    # FLOTANTE


   FLOAT: {

        '+': {
           INT:FLOAT,
           FLOAT:FLOAT
        },

        '-': {
           INT:FLOAT,
           FLOAT:FLOAT
        },

        '*': {
           INT:FLOAT,
           FLOAT:FLOAT
        },

        '/': {
           INT:FLOAT,
           FLOAT:FLOAT
        },

        '>': {
           INT: BOOL,
           FLOAT: BOOL
        },

        '<': {
           INT: BOOL,
           FLOAT: BOOL
        },

        '==': {
           INT: BOOL,
           FLOAT: BOOL
        },

        '!=': {
           INT: BOOL,
           FLOAT: BOOL
        },

        '=': {
           FLOAT:FLOAT
        }
    },


    # STRING


    STRING: {
        # Sería el letrero, pero no hay operaciones, así que lo dejamos comentado por ahora
        # # concatenación
        # '+': {
        #     STRING: STRING
        # },

        # # comparaciones
        # '==': {
        #     STRING: BOOL
        # },

        # '!=': {
        #     STRING: BOOL
        # },

        # '=': {
        #     STRING: STRING
        # }
    },


    # BOOL


    BOOL: {

        # igualdad lógica
        '==': {
            BOOL: BOOL
        },

        '!=': {
            BOOL: BOOL
        },

        '=': {
            BOOL: BOOL
        }
    }
}

def get_result_type(left_type, operator, right_type):

    try:
        return semantic_cube[left_type][operator][right_type]

    except KeyError:
        return ERROR
    
