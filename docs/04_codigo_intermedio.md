# 4. Código Intermedio

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

## 4.1 Representación: Cuádruplos

Cada cuádruplo tiene cuatro campos:

| Campo | Descripción |
|---|---|
| `op` | Operador (`+`, `-`, `*`, `/`, `>`, `<`, `==`, `!=`, `=`, `PRINT`, `UMINUS`) |
| `left` | Operando izquierdo (nombre de variable, constante o temporal) |
| `right` | Operando derecho (`None` para operaciones unarias y asignación) |
| `result` | Resultado: temporal generado o variable destino |

**Representación actual (Fase 3):** nombres simbólicos (`x`, `t1`, `3.14`).  
**Fase 4** traducirá a direcciones virtuales enteras.

---

## 4.2 Módulos implementados (`src/intermediate/`)

| Módulo | Clase | Responsabilidad |
|---|---|---|
| `quadruple.py` | `Quadruple` | Estructura de un cuádruplo + `__repr__` |
| `operand_stack.py` | `OperandStack` | Pila de nombres de operandos |
| `operator_stack.py` | `OperatorStack` | Pila de operadores pendientes |
| `type_stack.py` | `TypeStack` | Pila de tipos (paralela a operandos) |
| `jump_stack.py` | `JumpStack` | Pila de índices para backpatching — Fase 4 |
| `quadruple_manager.py` | `QuadrupleManager` | Coordina pilas, genera temporales, emite cuádruplos |

---

## 4.3 QuadrupleManager

Interfaz principal usada por el parser:

```python
qm.push_operand(name, type)      # empuja a PilaOperandos + PilaTipos
qm.pop_operand()                 # saca y regresa (operand, type)
qm.peek_type()                   # consulta tipo en tope sin sacar
qm.generate_operation(op)        # saca dos operandos, valida, emite, empuja t_n
qm.emit_assignment(var_name)     # saca tope, emite (=, operand, _, var)
qm.emit(op, left, right, result) # emite cuádruplo directo
qm.new_temp()                    # genera nombre de temporal: t1, t2, ...
qm.print_quadruples()            # imprime tabla formateada
```

### Generación de temporales

Contador interno `_temp_count`. Cada operación binaria genera un nuevo temporal:

```
x + y * 2  →  (*, y, 2, t1)  →  (+, x, t1, t2)
```

---

## 4.4 Gramática y puntos neurálgicos

La gramática de expresiones usa **recursión izquierda** para obtener
asociatividad izquierda correcta (`a - b - c` = `(a-b) - c`):

```bnf
<EXP_ADITIVA> → <EXP_ADITIVA> OP_ADD <TERMINO>   ← izquierda-recursiva
              | <TERMINO>

<TERMINO>     → <TERMINO> OP_MUL <FACTOR>         ← izquierda-recursiva
              | <FACTOR>

<EXP_REL>     → <EXP_ADITIVA> <EXP_REL_PRIMA>
<EXP_REL_PRIMA> → OP_REL <EXP_ADITIVA> | ε
```

### Tabla de puntos neurálgicos

| Producción | Acción | Cuádruplo generado |
|---|---|---|
| `factor → CTE_ENT` | `push_operand(val, INT)` | — |
| `factor → CTE_FLOT` | `push_operand(val, FLOAT)` | — |
| `factor → ID` (var) | `push_operand(name, type)` | — |
| `factor → OP_ADD factor` (unario -) | `pop`, `new_temp`, `push` | `(UMINUS, x, _, t1)` |
| `termino → termino OP_MUL factor` | `generate_operation(op)` | `(*, a, b, t1)` |
| `exp_aditiva → exp_aditiva OP_ADD termino` | `generate_operation(op)` | `(+, a, t1, t2)` |
| `exp_rel → exp_aditiva OP_REL exp_aditiva` | `generate_operation(op)` | `(<, a, b, t3)` |
| `estatuto → ID asigna` | `peek_type`, validar, `emit_assignment` | `(=, t2, _, x)` |
| `lista_imp → expresion ...` | `pop_operand`, diferir a `imprime` | — |
| `imprime → ESCRIBE ...` | `emit` por cada item | `(PRINT, x, _, _)` |
| `condicion → SI (expr)` | `pop_operand`, validar tipo bool | — *(GotoF en Fase 4)* |
| `ciclo → MIENTRAS (expr)` | `pop_operand`, validar tipo bool | — *(GotoF/Goto en Fase 4)* |

---

## 4.5 Ejemplos de cuádruplos generados

### Expresión con precedencia
```
x = (2 + 3) * 4;
```
```
#  OP    IZQ  DER  RES
0  +     2    3    t1
1  *     t1   4    t2
2  =     t2   _    x
```

### Expresión aritmética encadenada
```
z = x + y * 2;
```
```
#  OP    IZQ  DER  RES
0  *     y    2    t1
1  +     x    t1   t2
2  =     t2   _    z
```

### Condicional (Fase 3 — sin saltos)
```
si (x < y) { escribe("menor"); } sino { escribe("mayor"); };
```
```
#  OP     IZQ      DER  RES
0  <      x        y    t1
1  PRINT  "menor"  _    _
2  PRINT  "mayor"  _    _
```
> En Fase 4 se insertarán `GotoF` y `Goto` con los índices correctos.

### Ciclo (Fase 3 — sin saltos)
```
mientras (x < 5) haz { escribe(x); x = x + 1; };
```
```
#  OP     IZQ  DER  RES
0  <      x    5    t1
1  PRINT  x    _    _
2  +      x    1    t2
3  =      t2   _    x
```

---

## 4.6 Pendiente en Fase 4

- Traducción de operandos a **direcciones virtuales** (enteros)
- Cuádruplos de salto: `GotoF`, `Goto` con backpatching via `JumpStack`
- Cuádruplos de función: `ERA`, `PARAM`, `GOSUB`, `RETURN`, `ENDFUNC`

---

## Navegación

- Anterior: [← Análisis Semántico](03_semantica.md)
- Siguiente: [Memoria Virtual →](05_memoria_virtual.md)
