# 8. Herramientas de Inteligencia Artificial

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

## 8.1 Declaración de uso de IA

Durante el desarrollo de este proyecto se utilizó **Claude Sonnet 4.6** (Anthropic) como asistente principal mediante la interfaz **Claude Code CLI**. La IA funcionó como un colaborador técnico activo: leyó el código existente, propuso cambios, los aplicó directamente sobre los archivos, explicó las decisiones tomadas y diagnosticó errores.

---

## 8.2 Sesiones de trabajo

### Sesión 1 — Verificación de estructura y diagnóstico inicial

**Contexto:** Se presentó el proyecto completo al asistente y se solicitó un diagnóstico del estado de avance por fase.

**Prompts utilizados:**
- *"Ayúdame a hacer mi proyecto de compiladores [...] Lee el proyecto y dime qué tengo que hacer hoy"*
- *"Según lo que ves en mi código, en qué etapa se encuentra completamente cumplida"*

**Lo que hizo la IA:**
- Recorrió la estructura completa del repositorio (`src/`, `docs/`, `examples/`)
- Identificó el estado real de cada fase (0: completa, 1: ~85%, 2: ~55%, 3–5: no iniciadas)
- Detectó el bug crítico: `self.functions[p.ID]` en la producción `funcion` referenciaba una variable inexistente

**Decisiones tomadas por el autor:** El diagnóstico fue revisado y validado antes de proceder.

---

### Sesión 2 — Token y estatuto `regresa`

**Prompts utilizados:**
- *"Acabo de modificar docs/02_sintaxis.md para agregar un retorno [...] lo único que tendría que hacer es agregar esto a mi parser"*

**Lo que hizo la IA:**
- Agregó `REGRESA` al lexer (`src/lexico/lexer.py`)
- Agregó producciones `retorna` y `retorna_valor` al parser
- Corrigió el bug `self.functions[p.ID]` → `create_function()`

---

### Sesión 3 — Migración a `src/` y `main.py`

**Prompts utilizados:**
- *"Vuelve a aplicar los cambios pero a los archivos dentro de src y actualiza el main.py en el root"*

**Lo que hizo la IA:**
- Corrigió imports en `src/parser/parser.py` usando `sys.path`
- Reescribió `main.py` para importar desde `src/` y apuntar a `examples/`

---

### Sesión 4 — Fase 1 completa: fix de scope en funciones

**Prompts utilizados:**
- *"¿Qué información necesitas para completar la fase 1?"*
- *"¿Cómo debe ser la estructura de una función?"* → autor eligió llaves simples
- *"Si"*

**Lo que hizo la IA:**
- Introdujo el nonterminal marcador `funcion_cabecera` que dispara `enter_function` + cambio de scope antes de parsear parámetros y cuerpo
- Diagnosticó el conflicto LR(1) con llaves simples: `lista_vars` y `estatutos` ambos inician con `ID`, el parser no puede distinguirlos con un solo token de lookahead
- Mantuvo la doble llave para cuerpos de función como solución al conflicto

**Decisiones tomadas por el autor:** Confirmó el uso de doble llave al conocer la restricción técnica.

---

### Sesión 5 — Corrección de documentación (Fase 1)

**Prompts utilizados:**
- *"Actualiza los archivos docs pertinentes"*

**Lo que hizo la IA:**
- `docs/01_lexico.md`: corrigió `retorna`/`NULA`/`RETORNA` → `regresa`/`REGRESA`
- `docs/02_sintaxis.md`: corrigió `DOS_PUNTOS` → `PUNTO_COMA`; nota sobre la doble llave
- `docs/07_testing.md`: corrigió ruta de tests; tabla de status

---

### Sesión 6 — Fase 2: módulos semánticos separados

**Prompts utilizados:**
- *"Vamos con la Fase 2, dime qué tenemos que hacer"*
- *"¿Qué tipo de estructuras me recomiendas para variable table y function directory?"*
- *"Si"* (confirmar implementación)

**Lo que hizo la IA:**
- Propuso arquitectura: una `VariableTable` por scope, `FunctionDirectory` como dict, `SemanticActions` como fachada
- Creó `src/semantic/variable_table.py`, `function_directory.py`, `semantic_actions.py`
- Extrajo toda la lógica semántica del parser hacia los módulos separados
- Implementó 4 validaciones nuevas: conteo de argumentos, tipos de argumentos, tipo de `regresa`, `regresa` fuera de función
- Creó 12 tests semánticos (3 válidos + 9 de error, uno por validación)

**Decisiones tomadas por el autor:** Eligió la arquitectura de módulos separados; aprobó las validaciones a implementar.

---

### Sesión 7 — Fase 3: generación de cuádruplos con nombres simbólicos

**Prompts utilizados:**
- *"Vamos con la fase 3"*
- *"¿Qué es todo lo que vas a hacer?"*
- *"Si"*

**Lo que hizo la IA:**
- Diseñó y explicó el plan completo antes de implementar (pilas, cola, puntos neurálgicos)
- Creó `src/intermediate/`: `quadruple.py`, `operand_stack.py`, `operator_stack.py`, `type_stack.py`, `jump_stack.py`, `quadruple_manager.py`
- Cambió las gramáticas de `termino` y `exp_aditiva` a **izquierda-recursiva** para obtener asociatividad izquierda correcta (evita que `a - b - c` genere `a - (b - c)`)
- Generó cuádruplos para: operaciones aritméticas (`+`, `-`, `*`, `/`), relacionales (`>`, `<`, `==`, `!=`), asignaciones, `PRINT`, `UMINUS`
- Operandos representados como nombres simbólicos (`x`, `t1`, `"hola"`)

**Decisiones tomadas por el autor:** Eligió nombres simbólicos (Opción A) para Fase 3; eligió usar la Opción B (direcciones virtuales) en Fase 4.

---

### Sesión 8 — Fase 4: direcciones virtuales, saltos y funciones

**Prompts utilizados:**
- *"Ahora vamos con la fase 4 [...] Primero diseñemos"*
- *"Igual aplica la opción B — Direcciones virtuales [...] y si arranca"*

**Diseño aprobado por el autor antes de implementar:**
- Mapa de memoria con 11 segmentos (rangos 1000–11999)
- Traducción inline durante el parsing
- Protocolo ERA / PARAM / GOSUB / RETURN

**Lo que hizo la IA:**
- Creó `src/intermediate/virtual_memory.py` con 11 segmentos, tabla de constantes y reset por scope
- Integró `VirtualMemory` en `SemanticActions` para asignar direcciones al declarar variables y parámetros
- Implementó saltos condicionales con backpatching usando marcadores (`si_cond`, `sino_inicio`) y `JumpStack`
- Implementó saltos de ciclo (`mientras_inicio`, `mientras_cond`) con backpatch de `GotoF` + `Goto`
- Generó cuádruplos de función: `ERA`, `PARAM`, `GOSUB`, `RETURN` (con dirección de retorno), `ENDFUNC`
- Dividió `programa` en `prog_inicio` + `programa` para hacer backpatch del `Goto` inicial que salta definiciones de funciones
- Emite `HALT` al final del programa principal
- Diagnosticó y corrigió el bug donde SLY tomaba `prog_inicio` como símbolo de inicio en lugar de `programa`

**Decisiones tomadas por el autor:** Aprobó el mapa de memoria, el protocolo de llamada y el enfoque inline.

---

## 8.3 Consideraciones generales

| Aspecto | Detalle |
|---|---|
| Herramienta | Claude Sonnet 4.6 (Anthropic) vía Claude Code CLI |
| Modalidad | Asistente activo — lee archivos, aplica cambios, explica decisiones |
| Código generado por IA | Revisado y aprobado por el autor en cada paso |
| Decisiones de diseño | Tomadas por el autor; la IA propuso alternativas con trade-offs |
| Prompts registrados | Sí — incluidos en cada sesión |
| Commits | Realizados por el autor |

La definición del lenguaje, la gramática, los tokens, la arquitectura general y las decisiones de diseño fueron responsabilidad del autor. La IA se utilizó como herramienta de implementación, diagnóstico y documentación.

---

## Navegación

- Anterior: [← Testing](07_testing.md)
- Inicio: [↑ Overview](00_overview.md)
