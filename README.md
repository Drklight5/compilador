<div align="center">

# Diseño del Lenguaje Patito

<br>

#### Valeria Pérez Alonso  
#### A00833973

<br><br>

##### TC3002B.503 Desarrollo de aplicaciones avanzadas de ciencias computacionales

**Titular:**  
Elda Guadalupe Quiroga González

<br><br>

 Instituto Tecnológico y de Estudios Superiores de Monterrey

</div>

## 1. Introducción
Se describe el diseño de un micro-lenguaje imperativo procedural clásico, hecho con fines educativos en la aplicación de análisis léxico y sintáctico en la construcción de compiladores. El paradigma utilizado para el lenguaje es el imperativo donde se ejecuta una secuencia ordenada de instrucciones que permiten la manipulación de variables, evaluación de expresiones aritméticas y el control del flujo mediante estructuras básicas.

Liga al repositorio: https://github.com/Drklight5/compilador
_____________
## 2. Análisis Léxico

### 2.1 Expresiones Regulares
A continuación se definen las expresiones regulares correspondientes a los elementos léxicos del lenguaje.

#### Identificadores
Los identificadores permiten letras mayúsculas, minúsculas y el carácter guion bajo (`_`), tanto al inicio como en posiciones subsecuentes.

```regex
id -> [a-zA-Z_][a-zA-Z0-9_]*
```

#### Constantes numéricas

```regex
cte_ent  -> [0-9]+
cte_flot -> [0-9]+\.[0-9]+
```

#### Cadenas de caracteres (letreros)

```regex
letrero -> "([^"\\]|\\.)*"
```

#### Operadores

Los operadores se reconocen como tokens individuales:

```text
=   +   -   *   /   >   <   !=   ==
```

#### Símbolos especiales

```text
;   ,   :   (   )   {   }   [   ]
```

#### Palabras reservadas

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
```

---

### 2.2 Tokens

A continuación se presenta la lista de tokens reconocidos por el lenguaje:

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

___________

## 3. Análisis Sintáctico

### 3.1 Gramática (CFG)

```bnf
         <PROGRAMA> -> PROGRAMA ID PUNTO_COMA <DECLARACIONES> INICIO <CUERPO> FIN

    <DECLARACIONES> -> <VARS> <FUNCS>

             <VARS> -> VARS <LISTA_VARS>
                     | ε

       <LISTA_VARS> -> ID <LISTA_IDS> DOS_PUNTOS <TIPO> PUNTO_COMA <LISTA_VARS>
                     | ε

        <LISTA_IDS> -> COMA ID <LISTA_IDS>
                     | ε

             <TIPO> -> ENTERO
                     | FLOTANTE

            <FUNCS> -> <FUNCION> <FUNCS>
                     | ε

          <FUNCION> -> <RETORNO> ID PAR_IZQ <PARAMS_OPC> PAR_DER LLAVE_IZQ <VARS> <CUERPO> LLAVE_DER PUNTO_COMA

          <RETORNO> -> NULA
                     | <TIPO>

       <PARAMS_OPC> -> <LISTA_PARAMS>
                     | ε

     <LISTA_PARAMS> -> ID DOS_PUNTOS <TIPO> <MAS_PARAMS>
                     | ε

       <MAS_PARAMS> -> COMA ID DOS_PUNTOS <TIPO> <MAS_PARAMS>
                     | ε

           <CUERPO> -> LLAVE_IZQ <ESTATUTOS> LLAVE_DER

        <ESTATUTOS> -> <ESTATUTO> <ESTATUTOS>
                     | ε

         <ESTATUTO> -> ID <ESTATUTO_ID>
                     | <CONDICION>
                     | <CICLO>
                     | <IMPRIME>
                     | <BLOQUE>

           <BLOQUE> -> CORCH_IZQ <ESTATUTOS> CORCH_DER

      <ESTATUTO_ID> -> <ASIGNA>
                     | <LLAMADA>

           <ASIGNA> -> OP_ASIG <EXPRESION> PUNTO_COMA
           <LLAMADA> -> PAR_IZQ <ARGS_OPC> PAR_DER

        <CONDICION> -> SI PAR_IZQ <EXPRESION> PAR_DER <CUERPO> <SINO_OPC>

         <SINO_OPC> -> SINO <CUERPO>
                     | ε

            <CICLO> -> MIENTRAS PAR_IZQ <EXPRESION> PAR_DER HAZ <CUERPO> PUNTO_COMA

          <IMPRIME> -> ESCRIBE PAR_IZQ <ARG_IMP> PAR_DER PUNTO_COMA

          <ARG_IMP> -> LETRERO
                     | <EXPRESION> <ARG_IMP_PRIMA>

    <ARG_IMP_PRIMA> -> COMA <EXPRESION>
                     | ε

         <ARGS_OPC> -> <LISTA_ARGS>
                     | ε

       <LISTA_ARGS> -> <EXPRESION> <MAS_ARGS>
                     | ε

         <MAS_ARGS> -> COMA <EXPRESION> <MAS_ARGS>
                     | ε

        <EXPRESION> -> <EXP_REL>

          <EXP_REL> -> <EXP_ADITIVA> <EXP_REL_PRIMA>
          
    <EXP_REL_PRIMA> -> OP_REL <EXP_ADITIVA>
                     | ε

      <EXP_ADITIVA> -> <TERMINO> <EXP_ADITIVA_PRIMA>

<EXP_ADITIVA_PRIMA> -> OP_ADD <TERMINO> <EXP_ADITIVA_PRIMA>
                     | ε

          <TERMINO> -> <FACTOR> <TERMINO_PRIMA>

    <TERMINO_PRIMA> -> OP_MUL <FACTOR> <TERMINO_PRIMA>
                     | ε

           <FACTOR> -> PAR_IZQ <EXPRESION> PAR_DER
                     | OP_ADD <FACTOR>
                     | ID <LLAMADA_OPC>
                     | CTE_ENT
                     | CTE_FLOT

      <LLAMADA_OPC> -> PAR_IZQ <ARGS_OPC> PAR_DER
                     | ε
```


## Herramientas de Generación de Compiladores

### Herramientas Analizadas

Con el propósito de seleccionar una herramienta adecuada para el desarrollo del compilador, se analizaron diferentes alternativas utilizadas en la construcción de analizadores léxicos y sintácticos.

Las herramientas evaluadas fueron:

- SLY (Sly Lex Yacc)
- Flex & GNU Bison
- Lark

Cada una de estas herramientas presenta características distintas en cuanto a implementación, paradigma de uso y nivel de complejidad.

#### SLY (Sly Lex Yacc)

SLY es una biblioteca desarrollada completamente en Python para la construcción de analizadores léxicos y sintácticos. Fue creada por David Beazley como una versión modernizada de PLY (Python Lex-Yacc).

La herramienta utiliza programación orientada a objetos y decoradores para definir tokens y reglas gramaticales directamente en código Python, permitiendo una integración sencilla entre el lexer, parser y futuras etapas del compilador.

Características principales
- Implementación completamente en Python.
- Uso de parsing LALR(1).
- Integración directa entre análisis léxico y sintáctico.
- No requiere generación externa de archivos.
- Facilita la incorporación de acciones semánticas.

#### Flex y GNU Bison

Flex y GNU Bison son herramientas clásicas utilizadas para la construcción de compiladores en lenguajes como C y C++.

Flex se encarga del análisis léxico mediante expresiones regulares, mientras que Bison implementa el análisis sintáctico utilizando gramáticas libres de contexto y parsing LALR.

Estas herramientas generan código en lenguaje C que posteriormente debe compilarse.

Características principales
- Herramientas estándar de la industria.
- Alta eficiencia y rendimiento.
- Generación de código en C/C++.
- Uso ampliamente extendido en compiladores tradicionales.
- Mayor complejidad de configuración e integración.

#### Lark

Lark es una biblioteca moderna de parsing para Python que permite definir gramáticas mediante sintaxis EBNF. La herramienta soporta múltiples algoritmos de parsing, incluyendo Earley y LALR.

Una de sus principales ventajas es la generación automática de árboles sintácticos (AST), facilitando el procesamiento posterior del lenguaje.

Características principales
- Implementación moderna y modular.
- Compatible con gramáticas EBNF.
- Generación automática de AST.
- Soporte para distintos algoritmos de parsing.

#### Comparación de Herramientas

| Criterio                     | SLY       | Flex & Bison | Lark          |
| ---------------------------- | --------- | ------------ | ------------- |
| Lenguaje base                | Python    | C/C++        | Python        |
| Tipo de parsing              | LALR(1)   | LALR(1)      | Earley / LALR |
| Facilidad de integración     | Alta      | Media        | Alta          |
| Curva de aprendizaje         | Media     | Alta         | Media-Baja    |
| Generación automática de AST | No        | No           | Sí            |


#### Herramienta Seleccionada

Para el desarrollo del compilador del lenguaje Patito se seleccionó la herramienta SLY (Sly Lex Yacc).

La decisión se tomó debido a que SLY ofrece una integración directa con Python, una sintaxis moderna y una implementación clara basada en clases y decoradores. Además, facilita la implementación progresiva de las siguientes etapas del compilador, incluyendo validaciones semánticas, generación de código intermedio y construcción de la máquina virtual.

Otra ventaja importante es que SLY permite mantener tanto el lexer como el parser dentro del mismo entorno de desarrollo, simplificando el proceso de pruebas y depuración.

## Documentación de Implementación del Lenguaje PATITO en SLY


Implementación del lenguaje PATITO utilizando la herramienta SLY (Sly Lex Yacc), una biblioteca desarrollada en Python para la construcción de analizadores léxicos y sintácticos.

SLY permite definir tokens y reglas gramaticales mediante programación orientada a objetos y decoradores, integrando el análisis léxico y sintáctico dentro de una misma aplicación.

La implementación desarrollada utiliza:

* Un analizador léxico (`Lexer`) para el reconocimiento de tokens.
* Un analizador sintáctico (`Parser`) basado en parsing LALR(1).
* Construcción de estructuras tipo AST (Abstract Syntax Tree) mediante tuplas de Python.

### 2. Implementación del Analizador Léxico

El analizador léxico fue implementado mediante una clase heredada de `Lexer`.

```python id="3g9u7v"
from sly import Lexer

class PatitoLexer(Lexer):
```

Dentro de esta clase se definieron:

* Tokens del lenguaje
* Expresiones regulares
* Palabras reservadas
* Reglas de ignorado
* Manejo de errores léxicos


### 3. Definición de Tokens

Los tokens fueron declarados utilizando un conjunto (`set`) dentro de la clase `PatitoLexer` en el archivo `lexer.py`.

```python
tokens = {
    ID,
    CTE_ENT,
    CTE_FLOT,
    LETRERO,

    OP_ASIG,
    OP_ADD,
    OP_MUL,
    OP_REL,
    ... el resto de tokens
}
```

### 4. Expresiones Regulares Utilizadas

Las expresiones regulares fueron registradas directamente como atributos de clase o mediante decoradores `@_()` proporcionados por SLY.

#### 4.1 Identificadores

```python 
ID = r'[a-zA-Z_][a-zA-Z0-9_]*'
```

Permite:

* letras mayúsculas
* letras minúsculas
* guion bajo (`_`)
* dígitos posteriores


#### 4.2 Constantes Enteras

```python 
@_(r'\d+')
def CTE_ENT(self, t):
    t.value = int(t.value)
    return t
```


#### 4.3 Constantes Flotantes

```python 
@_(r'\d+\.\d+')
def CTE_FLOT(self, t):
    t.value = float(t.value)
    return t
```

#### 4.4 Letreros

```python
@_(r'"([^"\\\\]|\\\\.)*"')
def LETRERO(self, t):
    return t
```

La expresión regular permite:

* cadenas delimitadas por comillas dobles
* caracteres escapados


#### 4.5 Operadores

```python
OP_ASIG = r'='
OP_ADD = r'\+|-'
OP_MUL = r'\*|/'
OP_REL = r'==|!=|>|<'
```

#### 4.6 Símbolos Especiales

```python id="o3lxqm"
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



### 5. Palabras Reservadas

Las palabras reservadas fueron implementadas reutilizando el token `ID`.

```python id="ynf57u"
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
```

Este mecanismo permite distinguir automáticamente entre:

* identificadores definidos por el usuario
* palabras reservadas del lenguaje


### 6. Ignorado de Caracteres y Comentarios

#### 6.1 Espacios y tabulaciones

```python id="rw9qzx"
ignore = ' \t'
```



#### 6.2 Comentarios

```python id="yzm2bh"
ignore_comment = r'//.*'
```

Se implementó soporte para comentarios de una sola línea.



#### 6.3 Saltos de línea

```python id="c4cfdo"
@_(r'\n+')
def ignore_newline(self, t):
    self.lineno += len(t.value)
```

El contador de líneas se utiliza para reportar errores léxicos y sintácticos.



### 7. Manejo de Errores Léxicos

```python
def error(self, t):
    print(f'Caracter ilegal: {t.value[0]}')
    self.index += 1
```

Cuando se detecta un carácter inválido:

* se reporta el error
* el analizador continúa procesando la entrada



### 8. Implementación del Analizador Sintáctico

El parser fue implementado mediante una clase heredada de `Parser`.

```python 
from sly import Parser

class PatitoParser(Parser):
```

La gramática fue registrada utilizando decoradores `@_()`.

Cada producción gramatical fue implementada como un método de Python.


### 9. Formato de Definición de Producciones

SLY utiliza decoradores para asociar reglas gramaticales a funciones.

Ejemplo:

```python 
@_('PROGRAMA ID PUNTO_COMA declaraciones INICIO cuerpo FIN')
def programa(self, p):
    return ('programa', p.ID, p.declaraciones, p.cuerpo)
```

La cadena dentro del decorador representa la producción gramatical.


### 10. Reglas Gramaticales Implementadas

#### 10.1 Programa Principal

```python id="wkhc6z"
@_('PROGRAMA ID PUNTO_COMA declaraciones INICIO cuerpo FIN')
def programa(self, p):
    return ('programa', p.ID, p.declaraciones, p.cuerpo)
```



#### 10.2 Declaraciones de Variables

```python id="1omzt5"
@_('VARS lista_vars')
def vars(self, p):
    return ('vars', p.lista_vars)
```



#### 10.3 Declaraciones de Funciones

```python id="4rkkfw"
@_('funcion funcs')
def funcs(self, p):
    return [p.funcion] + p.funcs
```



#### 10.4 Asignaciones

```python id="h01wqm"
@_('OP_ASIG expresion PUNTO_COMA')
def asigna(self, p):
    return ('asigna', p.expresion)
```



#### 10.5 Condicionales

```python id="tq1tbo"
@_('SI PAR_IZQ expresion PAR_DER cuerpo sino_opc PUNTO_COMA')
def condicion(self, p):
    return ('si', p.expresion, p.cuerpo, p.sino_opc)
```



#### 10.6 Ciclos

```python id="hbhcse"
@_('MIENTRAS PAR_IZQ expresion PAR_DER HAZ cuerpo PUNTO_COMA')
def ciclo(self, p):
    return ('mientras', p.expresion, p.cuerpo)
```



#### 10.7 Escritura en Pantalla

```python id="5mndwq"
@_('ESCRIBE PAR_IZQ lista_imp PAR_DER PUNTO_COMA')
def imprime(self, p):
    return ('escribe', p.lista_imp)
```



#### 10.8 Expresiones

Las expresiones fueron divididas por niveles de precedencia.

###### Expresiones relacionales

```python id="1avf76"
@_('exp_aditiva exp_rel_prima')
def exp_rel(self, p):
```

###### Expresiones aditivas

```python id="tqt01p"
@_('termino exp_aditiva_prima')
def exp_aditiva(self, p):
```

###### Términos multiplicativos

```python id="6k80gq"
@_('factor termino_prima')
def termino(self, p):
```

###### Factores

```python id="9z7m56"
@_('PAR_IZQ expresion PAR_DER')
@_('ID llamada_opc')
@_('CTE_ENT')
@_('CTE_FLOT')
```



### 11. Producciones Vacías

Las producciones ε fueron implementadas mediante una regla auxiliar.

```python id="1y0l5m"
@_('')
def empty(self, p):
    pass
```

Esta producción fue reutilizada en:

* listas opcionales
* parámetros opcionales
* declaraciones opcionales



### 12. Construcción del AST

El parser construye estructuras tipo AST utilizando tuplas de Python.

Ejemplo:

```python id="uyc0yz"
('op_add', '+', izquierda, derecha)
```

Estas estructuras permiten:

* análisis semántico posterior
* validación de tipos
* generación de código intermedio



### 13. Manejo de Errores Sintácticos

```python id="5oyc5u"
def error(self, token):
    if token:
        print(
            f\"[PARSER ERROR] Token inesperado '{token.value}' \"
            f\"(tipo: {token.type}) en línea {token.lineno}\"
        )
    else:
        print(\"[PARSER ERROR] Fin de archivo inesperado\")
```

El parser reporta:

* token inesperado
* tipo del token
* línea del error


---
## Plan de Pruebas (Test Plan)

###  Introducción

Se desarrolló un conjunto de pruebas funcionales enfocadas en verificar:

* Reconocimiento correcto de tokens.
* Validación sintáctica de estructuras válidas.
* Detección de errores léxicos.
* Detección de errores sintácticos.
* Manejo de expresiones aritméticas y relacionales.
* Manejo de estructuras de control.
* Validación de llamadas a funciones.
* Manejo de producciones vacías.
* Construcción adecuada del AST.



### Estrategia de Pruebas

Las pruebas fueron divididas en las siguientes categorías:

| Categoría             | Objetivo                                                            |
| --------------------- | ------------------------------------------------------------------- |
| Léxicas               | Validar reconocimiento de tokens y detección de caracteres ilegales |
| Sintácticas válidas   | Verificar que programas correctos sean aceptados                    |
| Sintácticas inválidas | Verificar detección de errores gramaticales                         |
| Expresiones           | Validar precedencia y agrupación                                    |
| Control de flujo      | Validar estructuras condicionales y ciclos                          |
| Funciones             | Validar definición y llamadas de funciones                          |
| Casos límite          | Validar estructuras opcionales y vacías                             |


### Estructura de Archivos de Prueba

Cada caso de prueba fue almacenado en archivos independientes con extensión `.pat` dentro de patito/test del repositorio.

```text
/tests
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

### Casos de Prueba

#### Test Case 01: Programa mínimo válido

Objetivo: Validar que el parser acepte el programa más pequeño posible.
Archivo: `test_01_minimo.pat`



```pat
programa minimo;

inicio
{
}
fin
```

*Resultado esperado:*

* El lexer debe reconocer correctamente todos los tokens.
* El parser debe aceptar el programa.
* No deben generarse errores.


#### Test Case 02: Declaración de variables

Objetivo: Validar declaraciones de variables múltiples.
Archivo: `test_02_variables.pat`

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

*Resultado esperado:*

* Reconocimiento correcto de tipos.
* Reconocimiento correcto de listas de identificadores.
* Construcción correcta del AST de variables.

#### Test Case 03: Expresiones aritméticas

Objetivo: Validar operaciones aritméticas y precedencia.
Archivo: `test_03_expresiones.pat`


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

*Resultado esperado:*

* Multiplicación con mayor precedencia que suma.
* AST correctamente jerarquizado.
* Sin conflictos sintácticos.


#### Test Case 04: Condicional

Objetivo: Validar estructura condicional con bloque `sino`.
Archivo: `test_04_condicional.pat`

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

*Resultado esperado:*

* Reconocimiento correcto de la condición.
* Reconocimiento correcto del bloque `sino`.
* Construcción adecuada del AST.



#### Test Case 05: Ciclo mientras

Objetivo: Validar estructuras iterativas.
Archivo: `test_05_ciclo.pat`

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

*Resultado esperado:*

* Reconocimiento correcto del ciclo.
* Reconocimiento correcto del cuerpo iterativo.
* AST correcto para expresiones relacionales.


#### Test Case 06: Definición de funciones

Objetivo: Validar declaración de funciones con parámetros.
Archivo: `test_06_funciones.pat`

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

*Resultado esperado:*

* Reconocimiento correcto de parámetros.
* Reconocimiento correcto de variables locales.
* Reconocimiento correcto de función nula.


#### Test Case 07: Llamadas a funciones

Objetivo: Validar llamadas a funciones con argumentos.
Archivo: `test_07_llamadas.pat`

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

*Resultado esperado:*

* Reconocimiento correcto de argumentos.
* Reconocimiento correcto de llamada.
* AST correcto para llamada a función.


#### Test Case 08: Error léxico

Objetivo: Validar detección de caracteres ilegales.
Archivo: `test_08_error_lexico.pat`

```pat
programa errorLexico;

inicio
{
    x = 10 @ 5;
}
fin
```

*Resultado esperado:*

El lexer debe reportar:

```text
Caracter ilegal: @
```


#### Test Case 09: Error sintáctico

Objetivo: Validar detección de errores de sintaxis.
Archivo: `test_09_error_sintactico.pat`

```pat
programa errorSintaxis;

inicio
{
    x = ;
}
fin
```

*Resultado esperado:*

* El parser debe reportar un error sintáctico asociado a una expresión faltante.



#### Test Case 10: Precedencia de operadores

Objetivo: Validar precedencia y agrupación mediante paréntesis.
Archivo: `test_10_precedencia.pat`

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

*Resultado esperado:*

* El parser debe respetar la agrupación por paréntesis.
* El AST debe representar correctamente la precedencia.



### Status de Pruebas

| Característica                | Pass |
| ----------------------------- | -------- |
| Declaración de variables      | Sí       |
| Declaración de funciones      | Sí       |
| Parámetros                    | Sí       |
| Asignaciones                  | Sí       |
| Expresiones aritméticas       | Sí       |
| Expresiones relacionales      | Sí       |
| Condicionales                 | Sí       |
| Ciclos                        | Sí       |
| Llamadas a funciones          | Sí       |
| Manejo de errores léxicos     | Sí       |
| Manejo de errores sintácticos | Sí       |
| Producciones vacías           | Sí       |
| Precedencia de operadores     | Sí       |


## Declaración de Uso de Inteligencia Artificial

Durante el desarrollo de esta entrega se utilizaron herramientas de Inteligencia Artificial como apoyo en tareas de documentación, validación y generación de casos de prueba. Su uso estuvo enfocado principalmente en la mejora del formato y redacción del documento en Markdown, la consulta de información técnica relacionada con la herramienta SLY (Sly Lex Yacc) y la generación de propuestas de casos de prueba orientados a cubrir distintos escenarios válidos y de error del lenguaje.

Adicionalmente, se utilizó asistencia de IA para verificar propiedades de la gramática diseñada, particularmente para la verficación de la recursividad izquierda, con el objetivo de asegurar compatibilidad con el parser implementado mediante SLY.

La definición del lenguaje, las expresiones regulares, los tokens, las reglas gramaticales y las decisiones de diseño fueron desarrolladas y validadas por el autor.