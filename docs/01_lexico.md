# 1. Análisis Léxico

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

## 1.1 Expresiones Regulares

A continuación se definen las expresiones regulares correspondientes a los elementos léxicos del lenguaje.

### Identificadores

Los identificadores permiten letras mayúsculas, minúsculas y el carácter guion bajo (`_`), tanto al inicio como en posiciones subsecuentes.

```regex
id -> [a-zA-Z_][a-zA-Z0-9_]*
```

### Constantes numéricas

```regex
cte_ent  -> [0-9]+
cte_flot -> [0-9]+\.[0-9]+
```

### Cadenas de caracteres (letreros)

```regex
letrero -> "([^"\\]|\\.)*"
```

### Operadores

Los operadores se reconocen como tokens individuales:

```text
=   +   -   *   /   >   <   !=   ==
```

### Símbolos especiales

```text
;   ,   :   (   )   {   }   [   ]
```

### Palabras reservadas

Las siguientes palabras están reservadas y no pueden ser utilizadas como identificadores:

```text
programa
vars
inicio
fin
entero
flotante
escribe
mientras
haz
si
sino
nula
regresa
```

---

## 1.2 Tokens

Lista de tokens reconocidos por el lenguaje:

| Token      | Descripción                            |
| ---------- | -------------------------------------- |
| ID         | Identificadores                        |
| CTE_ENT    | Constantes enteras                     |
| CTE_FLOT   | Constantes de punto flotante           |
| LETRERO    | Cadenas de caracteres                  |
| OP_ASIG    | Operador de asignación (=)             |
| OP_ADD     | Operadores aditivos (+, -)             |
| OP_MUL     | Operadores multiplicativos (*, /)      |
| OP_REL     | Operadores relacionales (>, <, !=, ==) |
| PUNTO_COMA | Símbolo `;`                            |
| COMA       | Símbolo `,`                            |
| DOS_PUNTOS | Símbolo `:`                            |
| PAR_IZQ    | Símbolo `(`                            |
| PAR_DER    | Símbolo `)`                            |
| LLAVE_IZQ  | Símbolo `{`                            |
| LLAVE_DER  | Símbolo `}`                            |
| CORCH_IZQ  | Símbolo `[`                            |
| CORCH_DER  | Símbolo `]`                            |
| PROGRAMA   | Palabra reservada `programa`           |
| VARS       | Palabra reservada `vars`               |
| INICIO     | Palabra reservada `inicio`             |
| FIN        | Palabra reservada `fin`                |
| ENTERO     | Palabra reservada `entero`             |
| FLOTANTE   | Palabra reservada `flotante`           |
| ESCRIBE    | Palabra reservada `escribe`            |
| MIENTRAS   | Palabra reservada `mientras`           |
| HAZ        | Palabra reservada `haz`                |
| SI         | Palabra reservada `si`                 |
| SINO       | Palabra reservada `sino`               |
| NULA       | Palabra reservada `nula`               |
| REGRESA    | Palabra reservada `regresa`               |

---

## 1.3 Implementación del Analizador Léxico en SLY (referencia)

Esta sección documenta cómo se implementó el lexer en Python usando SLY.

### Clase base

```python
from sly import Lexer

class PatitoLexer(Lexer):
    pass
```

### Definición de tokens (ejemplo)

```python
tokens = {
    ID, CTE_ENT, CTE_FLOT, LETRERO,
    OP_ASIG, OP_ADD, OP_MUL, OP_REL,
    PUNTO_COMA, COMA, DOS_PUNTOS,
    PAR_IZQ, PAR_DER,
    LLAVE_IZQ, LLAVE_DER,
    CORCH_IZQ, CORCH_DER,
    PROGRAMA, VARS, INICIO, FIN,
    ENTERO, FLOTANTE, ESCRIBE,
    MIENTRAS, HAZ, SI, SINO, NULA, REGRESA
}
```

### Reglas principales

**ID**
```python
ID = r'[a-zA-Z_][a-zA-Z0-9_]*'
```

**Enteros**
```python
@_(r'\d+')
def CTE_ENT(self, t):
    t.value = int(t.value)
    return t
```

**Flotantes**
```python
@_(r'\d+\.\d+')
def CTE_FLOT(self, t):
    t.value = float(t.value)
    return t
```

**Letreros**
```python
@_(r'"([^"\\\\]|\\\\.)*"')
def LETRERO(self, t):
    return t
```

**Operadores**
```python
OP_ASIG = r'='
OP_ADD = r'\+|-'
OP_MUL = r'\*|/'
OP_REL = r'==|!=|>|<'
```

**Símbolos**
```python
PUNTO_COMA = r';'
COMA = r','
DOS_PUNTOS = r':'

PAR_IZQ = r'\('
PAR_DER = r'\)'

LLAVE_IZQ = r'\{'
LLAVE_DER = r'\}'

CORCH_IZQ = r'\['
CORCH_DER = r'\]'
```

### Palabras reservadas

```python
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
ID['regresa'] = REGRESA
```

### Ignorados y errores

**Espacios / tabs**
```python
ignore = ' \t'
```

**Comentarios**
```python
ignore_comment = r'//.*'
```

**Saltos de línea**
```python
@_(r'\n+')
def ignore_newline(self, t):
    self.lineno += len(t.value)
```

**Error léxico**
```python
def error(self, t):
    print(f'Caracter ilegal: {t.value}')
    self.index += 1
```

---

## Navegación

- Anterior: [← Overview](00_overview.md)
- Siguiente: [Análisis Sintáctico →](02_sintaxis.md)

