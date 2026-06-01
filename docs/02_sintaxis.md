# 2. Análisis Sintáctico

## Índice

1. [Overview](00_overview.md)
2. [Análisis Léxico](01_lexico.md)
3. [Análisis Sintáctico](02_sintaxis.md)
4. [Análisis Semántico](03_semantica.md)
5. [Código Intermedio](04_codigo_intermedio.md)
6. [Memoria Virtual](05_memoria_virtual.md)
7. [Máquina Virtual](06_maquina_virtual.md)
8. [Testing](07_testing.md)
9. [Herramientas de IA](08_herramientas_ia.md)

---

## 2.1 Gramática (CFG)

```bnf
/* ─── PROGRAMA ─────────────────────────────────────────────── */

<PROGRAMA> -> PROGRAMA ID PUNTO_COMA <DECLARACIONES> INICIO <CUERPO> FIN

/* ─── DECLARACIONES ─────────────────────────────────────────── */

<DECLARACIONES> -> <VARS> <FUNCS>

<VARS> -> VARS <LISTA_VARS>
        | ε

<LISTA_VARS> -> ID <LISTA_IDS> DOS_PUNTOS <TIPO> PUNTO_COMA <LISTA_VARS>
              | ε

<LISTA_IDS> -> COMA ID <LISTA_IDS>
             | ε

<TIPO> -> ENTERO
        | FLOTANTE

/* ─── FUNCIONES ──────────────────────────────────────────────── */

<FUNCS> -> <FUNCION> <FUNCS>
         | ε

<FUNCION> -> <TIPO_RETORNO> ID PAR_IZQ <PARAMS_OPC> PAR_DER
             LLAVE_IZQ <VARS> <CUERPO> LLAVE_DER PUNTO_COMA

/* Nota: el cuerpo de la función usa doble llave: { <VARS> { <ESTATUTOS> } }
   Esto es necesario para que el parser LR(1) pueda distinguir sin ambigüedad
   entre una declaración de variable (ID : tipo ;) y un estatuto (ID = expr ;),
   ya que ambos inician con ID y un lookahead de un token no es suficiente. */

/* Renombrado de <RETORNO> a <TIPO_RETORNO> para mayor claridad */
<TIPO_RETORNO> -> NULA
               | ENTERO
               | FLOTANTE

<PARAMS_OPC> -> <LISTA_PARAMS>
              | ε

<LISTA_PARAMS> -> ID DOS_PUNTOS <TIPO> <MAS_PARAMS>

<MAS_PARAMS> -> COMA ID DOS_PUNTOS <TIPO> <MAS_PARAMS>
              | ε

/* ─── ESTATUTOS ──────────────────────────────────────────────── */

<ESTATUTOS> -> <ESTATUTO> <ESTATUTOS>
             | ε

<ESTATUTO> -> <ASIGNACION>
            | <LLAMADA_STMT>
            | <CONDICION>
            | <CICLO>
            | <IMPRIME>
            | <RETORNA>           


<ASIGNACION> -> ID OP_ASIG <EXPRESION> PUNTO_COMA

<LLAMADA_STMT> -> ID PAR_IZQ <ARGS_OPC> PAR_DER PUNTO_COMA

/* ─── RETORNO ────────────────────────────────────────────────── */

/* Permite tanto  regresa <exp>;  como  regresa;  (para NULA)    */
<RETORNA> -> REGRESA <RETORNA_VALOR> PUNTO_COMA

<RETORNA_VALOR> -> <EXPRESION>
                 | ε

/* ─── CONDICIONAL ────────────────────────────────────────────── */

<CONDICION> -> SI PAR_IZQ <EXPRESION> PAR_DER
               LLAVE_IZQ <ESTATUTOS> LLAVE_DER
               <SINO_OPC>

<SINO_OPC> -> SINO LLAVE_IZQ <ESTATUTOS> LLAVE_DER
            | ε

/* ─── CICLO ──────────────────────────────────────────────────── */

<CICLO> -> MIENTRAS PAR_IZQ <EXPRESION> PAR_DER
           HAZ LLAVE_IZQ <ESTATUTOS> LLAVE_DER

/* ─── IMPRIME ────────────────────────────────────────────────── */

<IMPRIME> -> ESCRIBE PAR_IZQ <LISTA_IMP> PAR_DER PUNTO_COMA

/* Lista que acepta  ESCRIBE(a, b, c)  y  ESCRIBE("hola")        */
<LISTA_IMP> -> <ITEM_IMP> <MAS_IMP>

<ITEM_IMP> -> LETRERO
            | <EXPRESION>

<MAS_IMP> -> COMA <ITEM_IMP> <MAS_IMP>
           | ε

/* ─── ARGUMENTOS ─────────────────────────────────────────────── */

<ARGS_OPC> -> <EXPRESION> <MAS_ARGS>
            | ε

<MAS_ARGS> -> COMA <EXPRESION> <MAS_ARGS>
            | ε

/* ─── EXPRESIONES ────────────────────────────────────────────── */

<EXPRESION> -> <EXP_ADITIVA> <EXP_REL_PRIMA>

<EXP_REL_PRIMA> -> OP_REL <EXP_ADITIVA>
                 | ε

<EXP_ADITIVA> -> <TERMINO> <EXP_ADITIVA_PRIMA>

<EXP_ADITIVA_PRIMA> -> OP_ADD <TERMINO> <EXP_ADITIVA_PRIMA>
                     | ε

<TERMINO> -> <FACTOR> <TERMINO_PRIMA>

<TERMINO_PRIMA> -> OP_MUL <FACTOR> <TERMINO_PRIMA>
                 | ε

/* OP_ADD como prefijo unario (signo negativo / positivo)        */
<FACTOR> -> PAR_IZQ <EXPRESION> PAR_DER
          | OP_ADD <FACTOR>
          | ID <LLAMADA_OPC>
          | CTE_ENT
          | CTE_FLOT

<LLAMADA_OPC> -> PAR_IZQ <ARGS_OPC> PAR_DER
               | ε
```

---

## 2.2 Implementación del Parser en SLY (referencia)

### Clase base

```python
from sly import Parser

class PatitoParser(Parser):
    pass
```

### Ejemplo de producción

```python
@_('PROGRAMA ID PUNTO_COMA declaraciones INICIO cuerpo FIN')
def programa(self, p):
    return ('programa', p.ID, p.declaraciones, p.cuerpo)
```

### Producciones vacías

```python
@_('')
def empty(self, p):
    pass
```

### Manejo de errores sintácticos

```python
def error(self, token):
    if token:
        print(
            f"[PARSER ERROR] Token inesperado '{token.value}' "
            f"(tipo: {token.type}) en línea {token.lineno}"
        )
    else:
        print("[PARSER ERROR] Fin de archivo inesperado")
```

---

## Navegación

- Anterior: [← Análisis Léxico](01_lexico.md)
- Siguiente: [Análisis Semántico →](03_semantica.md)
