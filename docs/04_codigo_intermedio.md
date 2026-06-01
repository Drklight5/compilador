
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

> Nota: Este capítulo queda como plantilla/documentación base para completar conforme avances en la implementación.

## 4.1 Objetivo

- Traducir el resultado del parseo (AST/producciones) a una forma ejecutable por la máquina virtual.
- Representar operaciones, control de flujo y llamadas a funciones de manera uniforme.
- Facilitar depuración y pruebas.

## 4.2 Representación propuesta: Cuádruplos

Un cuádruplo suele tener forma:

| # | Operador | Operando Izq | Operando Der | Resultado |
|---|----------|--------------|--------------|-----------|

Ejemplos típicos:

- `(+ , a , b , t1)`
- `(= , t1, _ , x)`
- `(> , x , 5 , t2)`
- `(GOTOF, t2, _ , 18)`
- `(GOTO, _ , _ , 7)`
- `(PRINT, _ , _ , x)`

## 4.3 Estructuras comunes para generación

- **Pila de operandos**: guarda direcciones/IDs/temporales.
- **Pila de operadores**: guarda `+ - * / > < == != =`.
- **Pila de tipos**: se alinea con operandos para validación con el cubo semántico.
- **Pila de saltos**: guarda posiciones de cuádruplos para backpatching.
- **Generador de temporales**: produce `t1, t2, ...` o direcciones temporales.

## 4.4 Puntos neurálgicos sugeridos

- **Asignación**: al cerrar `ID = EXP;` generar `=`.
- **Expresiones**: al detectar precedencia, generar `+ - * /`.
- **Relacionales**: generar `> < == !=` y producir temporal booleano.
- **Condición `si/sino`**:
  - `GOTOF cond -> salto_falso`
  - `GOTO -> salto_fin` (si hay `sino`)
  - backpatch de saltos.
- **Ciclo `mientras`**:
  - marca inicio
  - `GOTOF cond -> salida`
  - `GOTO -> inicio`
- **Escritura**: `PRINT` por cada argumento.

## 4.5 Pendientes

- Definir set final de operadores y convenciones.
- Definir formato final de operandos (IDs vs direcciones virtuales).
- Integrar con memoria virtual y tabla de constantes.

---

## Navegación

- Anterior: [← Análisis Semántico](03_semantica.md)
- Siguiente: [Memoria Virtual →](05_memoria_virtual.md)

