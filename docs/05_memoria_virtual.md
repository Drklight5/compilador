# 5. Memoria Virtual

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

## 5.1 Objetivo

Asignar una **dirección virtual entera única** a cada variable, parámetro, temporal y constante del programa. Los cuádruplos usan estas direcciones en lugar de nombres simbólicos, lo que permite a la Máquina Virtual acceder a la memoria por índice numérico.

---

## 5.2 Distribución de segmentos

| Segmento | Tipo | Rango | Notas |
|---|---|---|---|
| Global | `entero` | 1000 – 1999 | Variables declaradas en el cuerpo principal |
| Global | `flotante` | 2000 – 2999 | |
| Local | `entero` | 3000 – 3999 | Variables locales y parámetros de función |
| Local | `flotante` | 4000 – 4999 | Se **reinician** al entrar a cada función |
| Temporal | `entero` | 5000 – 5999 | Resultados intermedios de expresiones |
| Temporal | `flotante` | 6000 – 6999 | Se **reinician** por scope |
| Temporal | `bool` | 7000 – 7999 | Resultados de operaciones relacionales |
| Constante | `entero` | 8000 – 8999 | Literales enteros (deduplicados) |
| Constante | `flotante` | 9000 – 9999 | Literales flotantes (deduplicados) |
| Constante | `string` | 10000 – 10999 | Letreros `"..."` (deduplicados) |
| Retorno func. | `entero` | 11000 – 11499 | Valor de retorno de funciones `entero` |
| Retorno func. | `flotante` | 11500 – 11999 | Valor de retorno de funciones `flotante` |

Capacidad máxima por segmento: **1000 símbolos** (suficiente para Patito).

---

## 5.3 Módulo `VirtualMemory` (`src/intermediate/virtual_memory.py`)

### Responsabilidades

- Mantener un **contador por segmento** que avanza con cada asignación.
- Mantener una **tabla de constantes** (valor → dirección) para reutilizar la misma dirección si la misma constante aparece varias veces.
- **Reiniciar** los contadores local y temporal al compilar cada función.
- Proveer un mapa inverso (dirección → nombre simbólico) para depuración.

### Interfaz principal

```python
vm.next_address('global', TYPES.INT)       # → 1000, 1001, ...
vm.next_address('local',  TYPES.FLOAT)     # → 4000, 4001, ...
vm.next_address('temp',   TYPES.BOOL)      # → 7000, 7001, ...
vm.next_address('return', TYPES.INT)       # → 11000, 11001, ...

vm.get_constant(42,    TYPES.INT)          # → 8000 (crea si no existe)
vm.get_constant(3.14,  TYPES.FLOAT)        # → 9000
vm.get_constant('"hi"', TYPES.STRING)      # → 10000

vm.reset_local()    # reinicia contadores local int/float a 3000/4000
vm.reset_temps()    # reinicia contadores temp int/float/bool a 5000/6000/7000

vm.get_name(1000)   # → 'x'  (mapa inverso para display)
vm.get_constants_table()  # lista de (dir, tipo, valor)
```

---

## 5.4 Ciclo de vida por scope

### Compilación del programa principal

```
__init__: reset no necesario (contadores ya en sus bases)
vars globales → 1000, 1001, ... (global int/float)
funciones  → (ver abajo)
prog_inicio (INICIO encontrado) → reset_temps() para el main
cuerpo main → temps 5000, 5001, ...
```

### Compilación de cada función

```
enter_function() → reset_local(), reset_temps()
parámetros    → 3000, 3001, ... (local)
vars locales  → siguiente libre en local
cuerpo        → temps 5000, 5001, ... (independiente del main)
return_address → 11000, 11001, ... (retorno, no se reinicia)
```

El segmento de **retorno** (`11000+`) no se reinicia, ya que cada función no-nula necesita una dirección permanente donde almacenar su valor de retorno.

---

## 5.5 Tabla de constantes

Las constantes se almacenan en un dict `valor → dirección`. Si la misma constante aparece varias veces, se reutiliza la misma dirección:

```python
# Ejemplo: x = 2 + 3; y = 2 * 5;
# La constante 2 aparece dos veces → misma dirección 8000
(+, 8000, 8001, 5000)   # 2 + 3 → t1 en 5000
(*  8000, 8002, 5001)   # 2 * 5 → t2 en 5001
```

---

## 5.6 Uso en la VM (Fase 5)

La VM mantiene tres arreglos (o dicts) de memoria en tiempo de ejecución:

| Arreglo | Rango | Contenido |
|---|---|---|
| `mem_global` | 1000–2999 | Variables globales (viven todo el programa) |
| `mem_local` | 3000–4999 | Frame actual de función (se apila en cada llamada) |
| `mem_temp` | 5000–7999 | Temporales del frame actual |
| `mem_const` | 8000–10999 | Constantes (solo lectura, inicializadas al cargar) |
| `mem_return` | 11000–11999 | Valores de retorno de funciones |

Para leer/escribir: `memory[address]` donde `address` es cualquier entero dentro de los rangos.

---

## Navegación

- Anterior: [← Código Intermedio](04_codigo_intermedio.md)
- Siguiente: [Máquina Virtual →](06_maquina_virtual.md)
