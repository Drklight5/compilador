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
| `op` | Operador (ver tabla completa en §4.2) |
| `left` | Dirección virtual del operando izquierdo (`None` si no aplica) |
| `right` | Dirección virtual del operando derecho (`None` si no aplica) |
| `result` | Dirección virtual del resultado, variable destino, o índice de salto |

Los operandos son **direcciones virtuales enteras** (ver [Memoria Virtual](05_memoria_virtual.md)). Al mostrar cuádruplos, el compilador agrega el nombre simbólico entre paréntesis para facilitar la lectura: `1000(x)`.

---

## 4.2 Catálogo de operadores

| Operador | Significado | Formato |
|---|---|---|
| `+` `-` `*` `/` | Aritmética | `(op, izq, der, temp)` |
| `>` `<` `==` `!=` | Relacional → resultado bool | `(op, izq, der, temp_bool)` |
| `=` | Asignación | `(=, origen, _, destino)` |
| `UMINUS` | Negación unaria | `(UMINUS, operand, _, temp)` |
| `PRINT` | Imprimir valor | `(PRINT, operand, _, _)` |
| `GotoF` | Salto si falso | `(GotoF, cond_bool, _, índice)` |
| `Goto` | Salto incondicional | `(Goto, _, _, índice)` |
| `ERA` | Reservar activation record | `(ERA, nombre_func, _, _)` |
| `PARAM` | Pasar argumento | `(PARAM, addr_arg, _, num_param)` |
| `GOSUB` | Llamar función | `(GOSUB, nombre_func, _, start_addr)` |
| `RETURN` | Retornar valor | `(RETURN, val_addr, _, return_addr)` |
| `ENDFUNC` | Fin de función | `(ENDFUNC, _, _, _)` |
| `HALT` | Fin del programa | `(HALT, _, _, _)` |

---

## 4.3 Módulos (`src/intermediate/`)

| Módulo | Clase | Responsabilidad |
|---|---|---|
| `quadruple.py` | `Quadruple` | Estructura de un cuádruplo + `__repr__` |
| `operand_stack.py` | `OperandStack` | Pila de direcciones de operandos |
| `operator_stack.py` | `OperatorStack` | Pila de operadores (reservado) |
| `type_stack.py` | `TypeStack` | Pila de tipos, paralela a operandos |
| `jump_stack.py` | `JumpStack` | Índices de cuádruplos pendientes de backpatch |
| `quadruple_manager.py` | `QuadrupleManager` | Coordina todo: pilas, VM, emisión |
| `virtual_memory.py` | `VirtualMemory` | Asigna direcciones virtuales por segmento |

---

## 4.4 QuadrupleManager — interfaz

```python
qm.push_operand(addr, type)        # empuja dirección + tipo a las pilas
qm.pop_operand()                   # → (addr, type)
qm.peek_type()                     # tipo en tope sin sacar
qm.generate_operation(op)          # pop×2, valida, emite, push temp → temp_addr
qm.emit_assignment(var_addr)       # pop, emite (=, operand, _, var_addr)
qm.emit(op, left, right, result)   # emisión directa
qm.fill(index, value)              # backpatch: rellena result del cuádruplo [index]
qm.new_temp(type)                  # pide dirección temporal a VirtualMemory
qm.count()                         # número de cuádruplos emitidos (= índice del próximo)
qm.print_quadruples(vm=vm)         # tabla con dir(nombre)
```

---

## 4.5 Gramática con puntos neurálgicos

### Expresiones — izquierda-recursiva

```bnf
<EXP_ADITIVA> → <EXP_ADITIVA> OP_ADD <TERMINO>   ← asociatividad izquierda
              | <TERMINO>

<TERMINO>     → <TERMINO> OP_MUL <FACTOR>
              | <FACTOR>

<EXP_REL>     → <EXP_ADITIVA> <EXP_REL_PRIMA>
<EXP_REL_PRIMA> → OP_REL <EXP_ADITIVA> | ε
```

La recursión izquierda garantiza que `a - b - c` genere `(a-b)-c` y no `a-(b-c)`.

### Tabla completa de puntos neurálgicos

| Producción | Acción semántica | Cuádruplo |
|---|---|---|
| `factor → CTE_ENT` | `vm.get_constant(val, INT)` → `push_operand(addr, INT)` | — |
| `factor → CTE_FLOT` | `vm.get_constant(val, FLOAT)` → `push_operand(addr, FLOAT)` | — |
| `factor → ID` (var) | `lookup_variable(name).address` → `push_operand(addr, type)` | — |
| `factor → OP_ADD factor` (`-`) | `pop`, `new_temp`, `push` | `(UMINUS, addr, _, t)` |
| `termino → termino OP_MUL factor` | `generate_operation(op)` | `(*, a, b, t)` |
| `exp_aditiva → exp_aditiva OP_ADD termino` | `generate_operation(op)` | `(+, a, t1, t2)` |
| `exp_rel → exp_aditiva OP_REL exp_aditiva` | `generate_operation(op)` | `(<, a, b, t_bool)` |
| `estatuto → ID asigna` | `peek_type`, `validate_assignment`, `emit_assignment` | `(=, t, _, var)` |
| `lista_imp → expresion` | `pop_operand` → lista | — |
| `imprime` | `emit PRINT` por cada item | `(PRINT, addr, _, _)` |
| `si_cond` (marcador) | `pop_operand`, `validate_condition`, `emit GotoF`, `push_jump` | `(GotoF, bool, _, ?)` |
| `sino_inicio` (marcador vacío) | `emit Goto`, backpatch GotoF, `push_jump` | `(Goto, _, _, ?)` |
| `sino_opc → empty` | backpatch GotoF | — |
| `sino_opc → SINO ...` | backpatch Goto | — |
| `mientras_inicio` (marcador) | `push_jump(count)` — marca inicio del ciclo | — |
| `mientras_cond` (marcador) | `pop_operand`, `validate_condition`, `emit GotoF`, `push_jump` | `(GotoF, bool, _, ?)` |
| `ciclo` | `emit Goto(inicio)`, backpatch GotoF | `(Goto, _, _, inicio)` |
| `prog_inicio` (marcador) | backpatch Goto inicial (quad 0), `reset_temps` | — |
| `funcion_cabecera` | `enter_function`, registrar `start_address = count()` | — |
| `funcion` | `emit ENDFUNC`, `exit_function` | `(ENDFUNC, _, _, _)` |
| `retorna` (con valor) | `pop_operand`, `validate_return`, `emit RETURN` | `(RETURN, val, _, ret_addr)` |
| `retorna` (sin valor) | `validate_return`, `emit RETURN` | `(RETURN, _, _, _)` |
| `factor → ID llamada_opc` (llamada como expr) | `ERA`, `PARAM`×n, `GOSUB`, `=` ret | `(ERA,…) (PARAM,…) (GOSUB,…) (=, ret_addr, _, t)` |
| `estatuto → ID llamada_estat` | `ERA`, `PARAM`×n, `GOSUB` | `(ERA,…) (PARAM,…) (GOSUB,…)` |
| `programa` | `emit HALT` | `(HALT, _, _, _)` |

---

## 4.6 Ejemplos con direcciones virtuales

### Expresión aritmética con precedencia (`x = (2 + 3) * 4`)
```
#  OP    IZQ        DER        RES
0  Goto  _          _          1       ← salta sobre funciones (programa vacío → apunta a 1)
1  +     8000(2)    8001(3)    5000    ← t1
2  *     5000       8002(4)    5001    ← t2
3  =     5001       _          1000(x)
4  HALT  _          _          _
```

### Condicional con `sino`
```
si (x < y) { escribe("menor"); } sino { escribe("mayor"); };
```
```
#  OP     IZQ        DER        RES
…  <      1000(x)    1001(y)    7000
N  GotoF  7000       _          N+3    ← si falso, salta a sino
N+1 PRINT 10000("menor") _      _
N+2 Goto  _          _          N+4    ← salta sobre sino
N+3 PRINT 10001("mayor") _      _
N+4 ...
```

### Ciclo `mientras`
```
mientras (x < 5) haz { x = x + 1; };
```
```
#  OP     IZQ        DER        RES
1  <      1000(x)    8001(5)    7000
2  GotoF  7000       _          6      ← salir del ciclo
3  +      1000(x)    8002(1)    5000
4  =      5000       _          1000(x)
5  Goto   _          _          1      ← volver al inicio
6  HALT   _          _          _
```

### Función con retorno
```
entero doble(x : entero) { vars r : entero; { r = x + x; regresa r; } };
resultado = doble(5);
```
```
#  OP       IZQ           DER  RES
0  Goto     _             _    5         ← saltar definición de doble
1  +        3000(x)       3000(x)  5000  ← r = x + x
2  =        5000          _    3001(r)
3  RETURN   3001(r)       _    11000     ← almacenar retorno en 11000
4  ENDFUNC  _             _    _
5  ERA      doble         _    _
6  PARAM    8000(5)       _    1
7  GOSUB    doble         _    1         ← start_address de doble
8  =        11000         _    5000      ← recoger retorno
9  =        5000          _    1000(resultado)
10 HALT     _             _    _
```

---

## Navegación

- Anterior: [← Análisis Semántico](03_semantica.md)
- Siguiente: [Memoria Virtual →](05_memoria_virtual.md)
