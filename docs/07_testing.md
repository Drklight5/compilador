# 7. Plan de Pruebas (Test Plan)

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

## 7.1 Introducción

Se desarrolló un conjunto de pruebas funcionales enfocadas en verificar:

- Reconocimiento correcto de tokens.
- Validación sintáctica de estructuras válidas.
- Detección de errores léxicos.
- Detección de errores sintácticos.
- Manejo de expresiones aritméticas y relacionales.
- Manejo de estructuras de control.
- Validación de llamadas a funciones.
- Manejo de producciones vacías.
- Construcción adecuada del AST.

## 7.2 Estrategia de Pruebas

| Categoría             | Objetivo                                                            |
|----------------------|---------------------------------------------------------------------|
| Léxicas               | Validar reconocimiento de tokens y detección de caracteres ilegales |
| Sintácticas válidas   | Verificar que programas correctos sean aceptados                    |
| Sintácticas inválidas | Verificar detección de errores gramaticales                         |
| Expresiones           | Validar precedencia y agrupación                                    |
| Control de flujo      | Validar estructuras condicionales y ciclos                          |
| Funciones             | Validar definición y llamadas de funciones                          |
| Casos límite          | Validar estructuras opcionales y vacías                             |

## 7.3 Estructura de Archivos de Prueba

Cada caso de prueba fue almacenado en archivos independientes con extensión `.pat` dentro de `examples/` del repositorio.

```text
/examples
│
├── test_01_minimo.pat
├── test_02_variables.pat
├── test_03_expresiones.pat
├── test_04_condicional.pat
├── test_05_ciclo.pat
├── test_06_funciones.pat
├── test_07_llamadas.pat
├── test_08_error_lexico.pat
├── test_09_error_sintactico.pat
└── test_10_precedencia.pat
```

## 7.4 Casos de Prueba

### Test Case 01: Programa mínimo válido

**Objetivo:** Validar que el parser acepte el programa más pequeño posible.  
**Archivo:** `test_01_minimo.pat`

```pat
programa minimo;

inicio
{
}
fin
```

**Resultado esperado:**
- El lexer reconoce correctamente tokens.
- El parser acepta el programa.
- No hay errores.

---

### Test Case 02: Declaración de variables

**Objetivo:** Validar declaraciones de variables múltiples.  
**Archivo:** `test_02_variables.pat`

```pat
programa variables;

vars
x, y : entero;
z : flotante;

inicio
{
}
fin
```

**Resultado esperado:**
- Reconocimiento correcto de tipos.
- Reconocimiento correcto de listas de identificadores.
- Construcción correcta del AST de variables.

---

### Test Case 03: Expresiones aritméticas

**Objetivo:** Validar operaciones aritméticas y precedencia.  
**Archivo:** `test_03_expresiones.pat`

```pat
programa expresiones;

vars
x, y, z : entero;

inicio
{
    x = 10;
    y = 20;
    z = x + y * 2;
}
fin
```

**Resultado esperado:**
- Multiplicación con mayor precedencia que suma.
- AST correctamente jerarquizado.
- Sin conflictos sintácticos.

---

### Test Case 04: Condicional

**Objetivo:** Validar estructura condicional con bloque `sino`.  
**Archivo:** `test_04_condicional.pat`

```pat
programa condicion;

vars
x, y : entero;

inicio
{
    x = 5;
    y = 10;

    si (x < y)
    {
        escribe("x es menor");
    }
    sino
    {
        escribe("x no es menor");
    };
}
fin
```

**Resultado esperado:**
- Reconocimiento correcto de la condición.
- Reconocimiento correcto del bloque `sino`.
- Construcción adecuada del AST.

---

### Test Case 05: Ciclo mientras

**Objetivo:** Validar estructuras iterativas.  
**Archivo:** `test_05_ciclo.pat`

```pat
programa ciclo;

vars
x : entero;

inicio
{
    x = 0;

    mientras (x < 5) haz
    {
        escribe(x);
        x = x + 1;
    };
}
fin
```

**Resultado esperado:**
- Reconocimiento correcto del ciclo.
- Reconocimiento correcto del cuerpo iterativo.
- AST correcto para expresiones relacionales.

---

### Test Case 06: Definición de funciones

**Objetivo:** Validar declaración de funciones con parámetros.  
**Archivo:** `test_06_funciones.pat`

```pat
programa funciones;

nula imprimirNumero(x : entero)
{
    vars
    y : entero;

    {
        y = x;
        escribe(y);
    }
};

inicio
{
}
fin
```

**Resultado esperado:**
- Reconocimiento correcto de parámetros.
- Reconocimiento correcto de variables locales.
- Reconocimiento correcto de función nula.

> **Nota de implementación:** Las funciones usan doble llave `{ vars ... { estatutos } }`. Las llaves externas delimitan el cuerpo completo de la función (vars + cuerpo); las internas delimitan los estatutos. Esto es necesario para evitar un conflicto LR(1) entre declaraciones de variables e instrucciones, que ambas inician con `ID`.

---

### Test Case 07: Llamadas a funciones

**Objetivo:** Validar llamadas a funciones con argumentos.  
**Archivo:** `test_07_llamadas.pat`

```pat
programa llamadas;

nula suma(x : entero, y : entero)
{
    {
        escribe(x + y);
    }
};

inicio
{
    suma(10, 20);
}
fin
```

**Resultado esperado:**
- Reconocimiento correcto de argumentos.
- Reconocimiento correcto de llamada.
- AST correcto para llamada a función.

---

### Test Case 08: Error léxico

**Objetivo:** Validar detección de caracteres ilegales.  
**Archivo:** `test_08_error_lexico.pat`

```pat
programa errorLexico;

inicio
{
    x = 10 @ 5;
}
fin
```

**Resultado esperado:**
```text
Caracter ilegal: @
```

---

### Test Case 09: Error sintáctico

**Objetivo:** Validar detección de errores de sintaxis.  
**Archivo:** `test_09_error_sintactico.pat`

```pat
programa errorSintaxis;

inicio
{
    x = ;
}
fin
```

**Resultado esperado:**
- El parser reporta un error sintáctico asociado a una expresión faltante.

---

### Test Case 10: Precedencia de operadores

**Objetivo:** Validar precedencia y agrupación mediante paréntesis.  
**Archivo:** `test_10_precedencia.pat`

```pat
programa precedencia;

vars
x : entero;

inicio
{
    x = (2 + 3) * 4;
}
fin
```

**Resultado esperado:**
- El parser respeta la agrupación por paréntesis.
- El AST representa correctamente la precedencia.

---

---

## 7.4.2 Tests de Fase 2 — Análisis Semántico

### Test Case 11: Función con valor de retorno

**Objetivo:** Validar `regresa` con tipo compatible con el tipo de retorno declarado.  
**Archivo:** `test_11_sem_retorno_valido.pat`  
**Resultado esperado:** Compilación exitosa.

---

### Test Case 12: Scope local en función

**Objetivo:** Validar que un parámetro con el mismo nombre que una variable global no genera conflicto, y que dentro de la función el parámetro tiene precedencia.  
**Archivo:** `test_12_sem_scope_local.pat`  
**Resultado esperado:** Compilación exitosa.

---

### Test Case 13: Operaciones con flotantes

**Objetivo:** Validar función con parámetros y retorno de tipo `flotante`.  
**Archivo:** `test_13_sem_flotante_valido.pat`  
**Resultado esperado:** Compilación exitosa.

---

### Test Case 14: Error — Variable duplicada

**Objetivo:** Detectar variable declarada dos veces en el mismo scope.  
**Archivo:** `test_14_err_variable_duplicada.pat`  
**Resultado esperado:**
```text
[PARSER ERROR] Variable "x" already declared in this scope
```

---

### Test Case 15: Error — Variable no declarada

**Objetivo:** Detectar uso de variable que no fue declarada.  
**Archivo:** `test_15_err_variable_no_declarada.pat`  
**Resultado esperado:**
```text
[PARSER ERROR] Variable "z" not declared
```

---

### Test Case 16: Error — Función duplicada

**Objetivo:** Detectar función declarada dos veces.  
**Archivo:** `test_16_err_funcion_duplicada.pat`  
**Resultado esperado:**
```text
[PARSER ERROR] Function "foo" already declared
```

---

### Test Case 17: Error — Conteo de argumentos incorrecto

**Objetivo:** Detectar llamada con número incorrecto de argumentos.  
**Archivo:** `test_17_err_args_conteo.pat`  
**Resultado esperado:**
```text
[PARSER ERROR] Function "foo" expects 1 argument(s), got 2
```

---

### Test Case 18: Error — Tipo de argumento incompatible

**Objetivo:** Detectar argumento de tipo incompatible con el parámetro declarado.  
**Archivo:** `test_18_err_args_tipo.pat`  
**Resultado esperado:**
```text
[PARSER ERROR] Argument 1 in call to "foo": cannot pass flotante as entero
```

---

### Test Case 19: Error — Tipo de asignación inválido

**Objetivo:** Detectar asignación de `flotante` a variable `entero`.  
**Archivo:** `test_19_err_tipo_asignacion.pat`  
**Resultado esperado:**
```text
[PARSER ERROR] Cannot assign flotante to entero
```

---

### Test Case 20: Error — `regresa` con valor en función `nula`

**Objetivo:** Detectar retorno de valor en función de tipo `nula`.  
**Archivo:** `test_20_err_regresa_en_nula.pat`  
**Resultado esperado:**
```text
[PARSER ERROR] Function "foo" is nula, cannot return a value
```

---

### Test Case 21: Error — `regresa` fuera de función

**Objetivo:** Detectar uso de `regresa` en el cuerpo principal del programa.  
**Archivo:** `test_21_err_regresa_global.pat`  
**Resultado esperado:**
```text
[PARSER ERROR] regresa cannot be used outside a function
```

---

### Test Case 22: Error — Condición no booleana

**Objetivo:** Detectar uso de expresión no booleana en condición de `si`.  
**Archivo:** `test_22_err_condicion_tipo.pat`  
**Resultado esperado:**
```text
[PARSER ERROR] Condition must be boolean, got entero
```

---

## 7.5 Status de Pruebas

| # | Archivo | Tipo | Resultado esperado | Estado |
|---|---------|------|--------------------|--------|
| 01 | test_01_minimo.pat | Válido | OK | ✓ |
| 02 | test_02_variables.pat | Válido | OK | ✓ |
| 03 | test_03_expresiones.pat | Válido | OK | ✓ |
| 04 | test_04_condicional.pat | Válido | OK | ✓ |
| 05 | test_05_ciclo.pat | Válido | OK | ✓ |
| 06 | test_06_funciones.pat | Válido | OK | ✓ |
| 07 | test_07_llamadas.pat | Válido | OK | ✓ |
| 08 | test_08_error_lexico.pat | Error léxico | ERROR | ✓ |
| 09 | test_09_error_sintactico.pat | Error sintáctico | ERROR | ✓ |
| 10 | test_10_precedencia.pat | Válido | OK | ✓ |
| 11 | test_11_sem_retorno_valido.pat | Válido semántico | OK | ✓ |
| 12 | test_12_sem_scope_local.pat | Válido semántico | OK | ✓ |
| 13 | test_13_sem_flotante_valido.pat | Válido semántico | OK | ✓ |
| 14 | test_14_err_variable_duplicada.pat | Error semántico | ERROR | ✓ |
| 15 | test_15_err_variable_no_declarada.pat | Error semántico | ERROR | ✓ |
| 16 | test_16_err_funcion_duplicada.pat | Error semántico | ERROR | ✓ |
| 17 | test_17_err_args_conteo.pat | Error semántico | ERROR | ✓ |
| 18 | test_18_err_args_tipo.pat | Error semántico | ERROR | ✓ |
| 19 | test_19_err_tipo_asignacion.pat | Error semántico | ERROR | ✓ |
| 20 | test_20_err_regresa_en_nula.pat | Error semántico | ERROR | ✓ |
| 21 | test_21_err_regresa_global.pat | Error semántico | ERROR | ✓ |
| 22 | test_22_err_condicion_tipo.pat | Error semántico | ERROR | ✓ |

---

## Navegación

- Anterior: [← Máquina Virtual](06_maquina_virtual.md)
- Siguiente: [Herramientas de IA →](08_herramientas_ia.md)
