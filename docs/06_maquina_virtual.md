

# 6. Máquina Virtual

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


## 6.1 Objetivo

- Ejecutar la lista de cuádruplos generados.
- Mantener el estado de memoria (global y stack de activaciones).
- Implementar control de flujo, evaluación de expresiones y llamadas a función.

## 6.2 Componentes típicos

- **Instruction Pointer (IP)**: apunta al cuádruplo actual.
- **Memoria global**: valores persistentes del programa.
- **Stack de memorias locales**: activation records por función.
- **Memoria temporal**: temporales del contexto actual.
- **Tabla de constantes**: direcciones y valores constantes.
- **Call stack**: direcciones de retorno / contexto.

## 6.3 Ejecución de operadores (dispatch)

A nivel conceptual:

- Aritméticos: `+ - * /`
- Relacionales: `> < == !=`
- Asignación: `=`
- Saltos:
  - `GOTO`
  - `GOTOF`
- I/O:
  - `PRINT`

## 6.4 Funciones (si aplica)

Cuádruplos típicos (depende del diseño):

- `ERA` (reservar activation record)
- `PARAM` (paso de parámetros)
- `GOSUB` (salto a función)
- `RETURN`
- `ENDFUNC`

## 6.5 Errores en runtime

- División entre cero.
- Acceso inválido de dirección.
- Direcciones fuera de rango.
- Tipos incompatibles (si no quedó resuelto en semántica).

---

## Navegación

- Anterior: [← Memoria Virtual](05_memoria_virtual.md)
- Siguiente: [Testing →](07_testing.md)

