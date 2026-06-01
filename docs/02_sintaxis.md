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

<EXPRESION> -> <EXP_REL>

<EXP_REL> -> <EXP_ADITIVA> <EXP_REL_PRIMA>

<EXP_REL_PRIMA> -> OP_REL <EXP_ADITIVA>
                 | ε

/* Gramática izquierda-recursiva para asociatividad izquierda    */
/* Garantiza que  a - b - c  genere  (a-b) - c  y no  a - (b-c) */
<EXP_ADITIVA> -> <EXP_ADITIVA> OP_ADD <TERMINO>
               | <TERMINO>

<TERMINO> -> <TERMINO> OP_MUL <FACTOR>
           | <FACTOR>

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

## 2.2 Nonterminals marcadores (para generación de código)

A partir de Fase 3/4, se añaden nonterminals auxiliares que permiten
ejecutar acciones semánticas **en el momento correcto** dentro de la
reducción bottom-up del parser LR(1).

| Marcador | Dónde se reduce | Acción |
|---|---|---|
| `prog_inicio` | Antes del `cuerpo` principal | Backpatch del `Goto` inicial; reset de temporales |
| `funcion_cabecera` | Antes de parámetros y cuerpo | `enter_function()`, registra `start_address` |
| `si_cond` | Después de evaluar condición de `si` | Emite `GotoF` pendiente, push a `JumpStack` |
| `sino_inicio` | Entre bloque verdadero y `sino` | Emite `Goto` pendiente, backpatch `GotoF` |
| `mientras_inicio` | Antes de evaluar condición del ciclo | Push índice de inicio a `JumpStack` |
| `mientras_cond` | Después de evaluar condición del ciclo | Emite `GotoF` pendiente, push a `JumpStack` |

### Ejemplo de producción con marcador

```python
# prog_inicio se reduce cuando el parser ve INICIO,
# antes de parsear el cuerpo del programa.
@_('PROGRAMA ID PUNTO_COMA declaraciones INICIO')
def prog_inicio(self, p):
    self.qm.fill(0, self.qm.count())   # backpatch Goto inicial
    self.vm.reset_temps()
    return p.ID

@_('prog_inicio cuerpo FIN')
def programa(self, p):
    self.qm.emit('HALT', None, None, None)
    return ('programa', p.prog_inicio)
```

> **Nota:** `programa` debe ser la **primera** producción definida en la
> clase para que SLY la tome como símbolo de inicio de la gramática.

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
