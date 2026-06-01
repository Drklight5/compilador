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

## 3.2 Directorio de Funciones

El Directorio de Funciones almacena información semántica de las funciones declaradas.

Cada función contiene:
- Tipo de retorno.
- Lista de parámetros.
- Tabla de variables local.

### Estructura utilizada

```python
function_directory = {
    'global': {
        'return_type': None,
        'params': [],
        'variables': {}
    },
    'function name': {
        'return_type': TYPES,
        'params': [...],
        'variables': {...}
    }
}
```

Operaciones principales:

**Crear función**
```python
create_function(name, return_type)
```

**Obtener función**
```python
get_function(name)
```

**Validar existencia**
```python
function_exists(name)
```

---

## 3.3 Tabla de Variables

Cada función contiene su propia tabla de variables.

La tabla almacena:
- nombre
- tipo
- valor
- scope

Ejemplo:

```python
'variables': {
    'a': {
        'type': TYPES.INT,
        'value': None,
        'scope': 'global'
    },
    'b': {
        'type': TYPES.FLOAT,
        'value': None,
        'scope': 'suma'
    }
}
```

Operaciones principales:

**Agregar variable**
```python
add_variable(name, var_type)
```

**Obtener variable**
```python
get_variable(name)
```

**Asignar valor**
```python
set_variable_value(name, value, var_type)
```

---

## 3.4 Manejo de Scopes

Se distinguen:
- Variables globales.
- Variables locales.

Se utiliza `self.current_scope` como scope actual.

**Resolución de variables**:
1. Scope local.
2. Scope global.

**Cambio de scope**:
- Entrar a una función: `change_scope(scope_name)`
- Regresar al scope global: `reset_scope()`

---

## 3.5 Puntos Neurálgicos

Acciones semánticas dentro del parser para:

- **Creación de funciones**: insertar en el directorio + cambiar scope.
- **Declaración de variables**: insertar en tabla + validar duplicados.
- **Declaración de parámetros**: agregar a params + insertar como variables locales.
- **Validación de expresiones**: consultar cubo semántico.
- **Validación de asignaciones**: validar tipo variable vs tipo expresión.

---

## 3.6 Validaciones Semánticas Implementadas

**Variables duplicadas**
```text
Variable "x" already declared
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

**Incompatibilidad de tipos**
```text
Type mismatch: entero + string
```

**Asignaciones inválidas**
```text
Cannot assign string to entero
```

---

## 3.7 Complejidad (promedio)

| Operación                | Complejidad   |
|-------------------------|---------------|
| Buscar variable          | O(1) promedio |
| Insertar variable        | O(1) promedio |
| Buscar función           | O(1) promedio |
| Insertar función         | O(1) promedio |
| Consultar cubo semántico | O(1) promedio |

---

## Navegación

- Anterior: [← Análisis Sintáctico](02_sintaxis.md)
- Siguiente: [Código Intermedio →](04_codigo_intermedio.md)
