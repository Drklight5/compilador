# 3. Análisis Semántico

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

El análisis semántico tiene como objetivo validar que las construcciones del programa tengan sentido lógico y respeten las reglas del lenguaje.

En esta etapa se verifica:

- Compatibilidad de tipos.
- Variables declaradas previamente.
- Variables duplicadas.
- Existencia de funciones.
- Compatibilidad de operaciones.
- Manejo correcto de scopes (global y local).

Para implementar esta etapa se diseñaron:

1. Un **Cubo Semántico**.
2. Un **Directorio de Funciones**.
3. Una **Tabla de Variables por scope**.
4. Validaciones semánticas integradas en el parser mediante puntos neurálgicos.

---

## 3.1 Cubo Semántico

El cubo semántico define qué operaciones son válidas entre tipos de datos y cuál es el tipo resultante. Si una operación no es válida, devuelve el tipo `ERROR`.

### Tipos soportados

| Tipo     |
|----------|
| entero   |
| flotante |
| bool     |
| string   |
| nula     |

### Estructura utilizada

Se implementó utilizando diccionarios hash (`dict`) anidados.

```python
semantic_cube = {
    INT: {
        '+': {
            INT: INT,
            FLOAT: FLOAT
        }
    }
}
```

Razones de diseño:

- Acceso rápido promedio O(1).
- Facilidad de lectura y mantenimiento.
- Representación directa de:
  - tipo izquierdo
  - operador
  - tipo derecho
- Escalabilidad para agregar nuevos operadores o tipos.

### Operaciones soportadas

**Operadores aritméticos:** `+ - * /`  
**Operadores relacionales:** `> < == !=`  
**Asignación:** `=`

Función principal:

```python
get_result_type(left_type, operator, right_type)
```

Devuelve:
- tipo resultante
- `TYPES.ERROR` si la operación es inválida

---

## 3.2 Arquitectura de módulos semánticos

La lógica semántica está separada del parser en tres módulos independientes dentro de `src/semantic/`:

| Módulo | Clase principal | Responsabilidad |
|---|---|---|
| `variable_table.py` | `VariableTable` | Tabla de variables de un scope |
| `function_directory.py` | `FunctionDirectory` | Directorio global de funciones |
| `semantic_actions.py` | `SemanticActions` | Validaciones de alto nivel usadas por el parser |

---

## 3.3 Tabla de Variables (`VariableTable`)

Una instancia por función (scope). Implementada como `dict` indexado por nombre.

Cada entrada es un `VarEntry` con:

| Campo | Tipo | Descripción |
|---|---|---|
| `name` | `str` | Nombre de la variable |
| `type` | `TYPES` | Tipo semántico |
| `address` | `int\|None` | Dirección virtual — reservado para Fase 4 |
| `value` | `any\|None` | Valor en tiempo de compilación (opcional) |

Operaciones principales:

```python
var_table.add(name, var_type)      # agrega, lanza si duplicada
var_table.get(name)                # retorna VarEntry o None
var_table.exists(name)             # bool
```

---

## 3.4 Directorio de Funciones (`FunctionDirectory`)

`dict` global indexado por nombre de función. El scope `'global'` es una entrada especial con `return_type=None` que contiene las variables globales del programa.

Cada entrada es un `FunctionEntry` con:

| Campo | Tipo | Descripción |
|---|---|---|
| `return_type` | `TYPES\|None` | Tipo de retorno |
| `params` | `list[ParamEntry]` | Lista ordenada de parámetros |
| `var_table` | `VariableTable` | Tabla de variables locales |
| `start_address` | `int\|None` | Dirección de inicio — reservado para Fase 4 |

```
FunctionDirectory
├── 'global'  →  FunctionEntry(ret=None,  params=[], vars={x, y})
├── 'suma'    →  FunctionEntry(ret=INT,   params=[a:INT, b:INT], vars={a, b, r})
└── 'foo'     →  FunctionEntry(ret=NULL,  params=[n:INT], vars={n})
```

Operaciones principales:

```python
func_dir.add_function(name, return_type)
func_dir.get_function(name)         # lanza si no existe
func_dir.exists(name)
func_dir.add_param(func, pname, ptype)   # agrega a params + var_table
func_dir.add_variable(scope, name, type)
func_dir.get_variable(scope, name)  # busca local → global
```

**Lookup de variables:** busca primero en el scope local; si no encuentra, busca en `global`. Esto implementa la regla de scoping de Patito.

---

## 3.5 Acciones Semánticas (`SemanticActions`)

Fachada que coordina `FunctionDirectory` y el cubo semántico. Es el único punto de entrada del parser para operaciones semánticas.

Mantiene `current_scope` para saber en qué función se está parseando.

| Método | Cuándo se llama |
|---|---|
| `enter_function(name, ret)` | Al reducir `funcion_cabecera` |
| `exit_function()` | Al terminar de reducir `funcion` |
| `declare_variable(name, type)` | Al reducir cada `var_decl` en `lista_vars` |
| `declare_parameter(name, type)` | Al reducir cada param en `lista_params` / `mas_params` |
| `lookup_variable(name)` | Al reducir `factor → ID` (variable) |
| `lookup_function(name)` | Al reducir `factor → ID llamada_opc` (llamada) |
| `validate_assignment(lt, rt)` | Al reducir `estatuto → ID asigna` |
| `validate_operation(lt, op, rt)` | Al reducir `exp_rel`, `exp_aditiva`, `termino` |
| `validate_condition(type)` | Al reducir `condicion` y `ciclo` |
| `validate_call(func, arg_types)` | Al reducir llamadas en `estatuto` y `factor` |
| `validate_return(expr_type)` | Al reducir `retorna` |

---

## 3.6 Puntos Neurálgicos

```
PROGRAMA id ;
    ↓
  declaraciones
    ├── VARS lista_vars          ← declare_variable() por cada ID
    └── funcs
         └── retorno ID          ← enter_function()  [funcion_cabecera]
              └── ( params )     ← declare_parameter() por cada param
                   └── { vars    ← declare_variable() por cada var local
                        { body } ← validaciones en asignaciones, llamadas, regresa
                   }             ← exit_function()
  INICIO
    └── { body }                 ← validaciones en expresiones, condiciones, ciclos
FIN
```

---

## 3.7 Validaciones Semánticas Implementadas

**Variables duplicadas**
```text
Variable "x" already declared in this scope
```

**Variables no declaradas**
```text
Variable "x" not declared
```

**Funciones duplicadas**
```text
Function "suma" already declared
```

**Funciones inexistentes**
```text
Function "suma" not declared
```

**Incompatibilidad de tipos en expresión**
```text
Type mismatch: entero + flotante  →  (válido, resultado flotante)
Type mismatch: entero + bool      →  ERROR
```

**Asignación inválida**
```text
Cannot assign flotante to entero
```

**Condición no booleana**
```text
Condition must be boolean, got entero
```

**Número de argumentos incorrecto**
```text
Function "foo" expects 1 argument(s), got 2
```

**Tipo de argumento incompatible**
```text
Argument 1 in call to "foo": cannot pass flotante as entero
```

**`regresa` con valor en función `nula`**
```text
Function "foo" is nula, cannot return a value
```

**`regresa` sin valor en función con tipo de retorno**
```text
Function "foo" must return entero, cannot use regresa without a value
```

**`regresa` fuera de función**
```text
regresa cannot be used outside a function
```

---

## 3.8 Complejidad (promedio)

| Operación                | Complejidad   |
|-------------------------|---------------|
| Buscar variable (local)  | O(1) promedio |
| Buscar variable (global) | O(1) promedio |
| Insertar variable        | O(1) promedio |
| Buscar función           | O(1) promedio |
| Insertar función         | O(1) promedio |
| Consultar cubo semántico | O(1) promedio |
| Validar argumentos       | O(n) — n = número de parámetros |

---

## Navegación

- Anterior: [← Análisis Sintáctico](02_sintaxis.md)
- Siguiente: [Código Intermedio →](04_codigo_intermedio.md)
