# Cubo Semántico de Patito

## Introducción

El Cubo Semántico es la estructura encargada de determinar la validez de una operación entre dos operandos y definir el tipo resultante.

---

# Tipos Soportados

| Tipo  |
| ----- |
| int   |
| float |
| char  |
| bool  |

---

# Operadores Soportados

## Aritméticos

```text
+
-
*
/
```

## Relacionales

```text
<
>
<=
>=
==
!=
```

## Asignación

```text
=
```

---

# Reglas Generales

## Promoción Numérica

```text
int + int     -> int
int + float   -> float
float + int   -> float
float + float -> float
```

La misma regla aplica para:

```text
-
*
/
```

---

# Operaciones Aritméticas

| Izq   | Der   | Operador | Resultado |
| ----- | ----- | -------- | --------- |
| int   | int   | + - *    | int       |
| int   | int   | /        | float     |
| int   | float | + - * /  | float     |
| float | int   | + - * /  | float     |
| float | float | + - * /  | float     |

---

# Operaciones Relacionales

| Izq   | Der   | Operador  | Resultado |
| ----- | ----- | --------- | --------- |
| int   | int   | < > <= >= | bool      |
| int   | float | < > <= >= | bool      |
| float | int   | < > <= >= | bool      |
| float | float | < > <= >= | bool      |

---

# Igualdad

| Izq   | Der   | Operador | Resultado |
| ----- | ----- | -------- | --------- |
| int   | int   | == !=    | bool      |
| int   | float | == !=    | bool      |
| float | int   | == !=    | bool      |
| float | float | == !=    | bool      |
| char  | char  | == !=    | bool      |

---

# Asignaciones Permitidas

| Variable | Valor |
| -------- | ----- |
| int      | int   |
| float    | int   |
| float    | float |
| char     | char  |
| bool     | bool  |

---

# Asignaciones Inválidas

| Variable | Valor |
| -------- | ----- |
| int      | float |
| int      | char  |
| float    | char  |
| char     | int   |
| char     | float |
| bool     | int   |
| bool     | float |
| bool     | char  |

---

# Operaciones Inválidas

Todas las operaciones no definidas explícitamente en este documento generan error semántico.

Ejemplos:

```text
char + char
char * int
char / float
bool + int
bool * bool
```

---

# Representación Implementada

La implementación utiliza un diccionario tridimensional indexado por:

```python
(left_type, operator, right_type)
```

Ejemplo:

```python
semantic_cube[("int", "+", "float")] = "float"
semantic_cube[("float", ">", "int")] = "bool"
semantic_cube[("char", "+", "char")] = "error"
```

---

# Uso Durante la Compilación

Durante la generación de expresiones:

1. Se obtiene el tipo del operando izquierdo.
2. Se obtiene el tipo del operando derecho.
3. Se consulta el cubo semántico.
4. Si existe resultado válido:

   * Se genera un temporal.
   * Se genera el cuádruplo correspondiente.
5. Si no existe:

   * Se genera error semántico.
