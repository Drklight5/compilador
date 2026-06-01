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

> Nota: Este capítulo se deja como plantilla/documentación base para completar conforme avances en la implementación.

## 5.1 Objetivo

- Asignar direcciones virtuales por **segmento** (global/local/temporal/constante) y por **tipo**.
- Permitir que la VM lea/escriba valores usando direcciones numéricas.
- Reiniciar correctamente memoria local/temporal por llamada de función.

## 5.2 Segmentación sugerida (ejemplo)

Ajusta rangos según tu implementación:

- **Global**
  - entero: 1000–1999
  - flotante: 2000–2999
  - bool: 3000–3999
  - string: 4000–4999

- **Local**
  - entero: 5000–5999
  - flotante: 6000–6999
  - bool: 7000–7999
  - string: 8000–8999

- **Temporales**
  - entero: 9000–9999
  - flotante: 10000–10999
  - bool: 11000–11999
  - string: 12000–12999

- **Constantes**
  - entero: 13000–13999
  - flotante: 14000–14999
  - string: 15000–15999

## 5.3 Asignación de direcciones (idea)

- Mantener contadores por (segmento, tipo).
- Funciones típicas:
  - `alloc_global(type)`
  - `alloc_local(type)`
  - `alloc_temp(type)`
  - `alloc_const(value, type)` (deduplicación en tabla de constantes)

## 5.4 Consideraciones

- Reinicio de locales/temporales al entrar/salir de funciones.
- Tabla de constantes para no duplicar direcciones.
- Validación de overflow de rangos.

---

## Navegación

- Anterior: [← Código Intermedio](04_codigo_intermedio.md)
- Siguiente: [Máquina Virtual →](06_maquina_virtual.md)
