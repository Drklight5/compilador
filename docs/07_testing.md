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

## 7.5 Status de Pruebas

| Característica                | Pass |
|-----------------------------|------|
| Declaración de variables      | Sí   |
| Declaración de funciones      | Sí   |
| Parámetros                    | Sí   |
| Asignaciones                  | Sí   |
| Expresiones aritméticas       | Sí   |
| Expresiones relacionales      | Sí   |
| Condicionales                 | Sí   |
| Ciclos                        | Sí   |
| Llamadas a funciones          | Sí   |
| Manejo de errores léxicos     | Sí   |
| Manejo de errores sintácticos | Sí   |
| Producciones vacías           | Sí   |
| Precedencia de operadores     | Sí   |

---

## Navegación

- Anterior: [← Máquina Virtual](06_maquina_virtual.md)
- Siguiente: [Herramientas de IA →](08_herramientas_ia.md)
