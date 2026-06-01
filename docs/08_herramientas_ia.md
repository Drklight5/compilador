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

Durante el desarrollo de este proyecto se utilizó **Claude Sonnet 4.6** (Anthropic) como asistente principal mediante la interfaz **Claude Code CLI**. La IA funcionó como un colaborador técnico activo: no solo respondió preguntas sino que leyó el código existente, propuso cambios, los aplicó directamente sobre los archivos y explicó las decisiones tomadas.

---

## 8.2 Sesiones de trabajo

### Sesión 1 — Verificación de estructura y diagnóstico inicial

**Contexto:** Se presentó el proyecto completo al asistente y se solicitó un diagnóstico del estado de avance por fase.

**Prompts utilizados:**
- *"Ayúdame a hacer mi proyecto de compiladores [...] Lee el proyecto y dime qué tengo que hacer hoy"*
- *"Según lo que ves en mi código, en qué etapa se encuentra completamente cumplida"*

**Lo que hizo la IA:**
- Recorrió la estructura completa del repositorio (`src/`, `docs/`, `examples/`, `patito/`)
- Leyó `patito/lexer.py`, `patito/parser.py`, `src/parser/parser.py`, `src/lexico/lexer.py`, `src/semantic/semantic_cube.py` y todos los docs
- Identificó el estado real de cada fase:
  - Fase 0: completa
  - Fase 1: ~85% — bug de scope en funciones bloqueaba tests 06 y 07
  - Fase 2: ~55% — cubo semántico funcional pero scope roto y módulos `src/semantic/` vacíos
  - Fases 3–5: no iniciadas
- Detectó el bug crítico: `self.functions[p.ID]` en la producción `funcion` referenciaba una variable inexistente (debía ser `create_function()`)

**Decisiones tomadas por el autor:** El diagnóstico fue revisado y validado antes de proceder.

---

### Sesión 2 — Implementación del token y estatuto `regresa`

**Contexto:** Se había modificado `docs/02_sintaxis.md` para agregar la producción `<RETORNA>` a la gramática. Se solicitó aplicar ese cambio al código.

**Prompts utilizados:**
- *"Acabo de modificar el archivo docs/02_sintaxis.md para agregar un retorno a las expresiones [...] lo único que tendría que hacer es agregar esto a mi parser y otros documentos necesarios"*
- *"Si, haz los cambios"*

**Lo que hizo la IA:**

En `patito/lexer.py` y `src/lexico/lexer.py`:
- Agregó `REGRESA` al conjunto de tokens
- Mapeó la palabra reservada `'regresa'` → `REGRESA`

En `patito/parser.py` y `src/parser/parser.py`:
- Agregó el caso `retorna` en la regla `estatuto`
- Agregó producciones `retorna` y `retorna_valor`:
  ```python
  @_('REGRESA retorna_valor PUNTO_COMA')
  def retorna(self, p): ...

  @_('expresion')
  def retorna_valor(self, p): ...

  @_('empty')
  def retorna_valor(self, p): ...
  ```
- Corrigió el bug `self.functions[p.ID]` → `self.create_function(p.ID, p.retorno)`

**Decisiones tomadas por el autor:** Se aprobó explícitamente cada cambio antes de aplicarlo.

---

### Sesión 3 — Migración a `src/` y actualización de `main.py`

**Contexto:** Los cambios anteriores se habían aplicado a `patito/`. Se solicitó replicarlos en `src/` y hacer funcionar `main.py` desde la raíz.

**Prompts utilizados:**
- *"Vuelve a aplicar los cambios pero a los archivos dentro de src y actualiza el main.py en el root para que funciones"*

**Lo que hizo la IA:**
- Corrigió los imports de `src/parser/parser.py` (de `from lexer import` a `from lexico.lexer import` y `from semantic.semantic_cube import`) usando `sys.path`
- Reescribió `main.py` para importar desde `src/` y apuntar a `examples/` como directorio de tests
- Descubrió que los archivos `.pat` estaban en `examples/`, no en `patito/tests/`
- Verificó que 8/10 tests pasaran correctamente (06 y 07 fallaban por el bug de scope, que era preexistente)

---

### Sesión 4 — Completar Fase 1: fix de scope en funciones

**Contexto:** Se solicitó completar la Fase 1. La IA identificó que el único blocker era el bug de scope en la producción `funcion`.

**Prompts utilizados:**
- *"¿Qué información necesitas que te brinde para completar la fase 1?"*
- *"¿Cómo debe ser la estructura de una función en Patito?"* → El autor eligió **llaves simples**
- *"Si"* (confirmar los cambios)

**Lo que hizo la IA:**

Intentó implementar llaves simples (`LLAVE_IZQ vars estatutos LLAVE_DER`) usando un nonterminal marcador `funcion_cabecera`:

```python
@_('retorno ID')
def funcion_cabecera(self, p):
    self.create_function(p.ID, p.retorno)
    self.change_scope(p.ID)
    return (p.retorno, p.ID)
```

Y movió `add_parameter` a `lista_params` / `mas_params` para que los parámetros se registraran en el scope correcto.

Diagnosticó que las llaves simples generan un **conflicto LR(1) estructural**: `lista_vars` y `estatutos` ambos inician con `ID`, y con un solo token de lookahead el parser no puede distinguir `y : entero;` (declaración) de `y = x;` (estatuto). Por esta razón se mantuvo la **doble llave** para cuerpos de función.

**Resultado:** 10/10 tests con comportamiento correcto (8 válidos pasan, 2 inválidos reportan error esperado).

**Decisiones tomadas por el autor:** El autor eligió inicialmente llaves simples; al conocer la restricción LR(1), confirmó el uso de doble llave.

---

### Sesión 5 — Corrección de documentación

**Prompts utilizados:**
- *"Actualiza los archivos docs pertinentes"*
- *"Gracias, actualiza los docs 8 uso de IA, con lo que has hecho conmigo hasta ahorita"*

**Lo que hizo la IA:**
- `docs/01_lexico.md`: corrigió token `retorna`/`NULA`/`RETORNA` → `regresa`/`REGRESA` en 4 lugares
- `docs/02_sintaxis.md`: corrigió `DOS_PUNTOS` → `PUNTO_COMA` en la producción `PROGRAMA`; `<ESTATUTOS>` → `<CUERPO>`; agregó nota sobre la doble llave y el conflicto LR(1)
- `docs/07_testing.md`: corrigió ruta `patito/test` → `examples/`; agregó nota de implementación sobre doble llave en test 06
- `docs/08_herramientas_ia.md`: este documento (registro completo de sesiones)

---

## 8.3 Consideraciones generales

| Aspecto | Detalle |
|---|---|
| Herramienta | Claude Sonnet 4.6 (Anthropic) vía Claude Code CLI |
| Modalidad | Asistente activo — lee archivos, aplica cambios, explica decisiones |
| Código generado por IA | Revisado y aprobado por el autor en cada paso |
| Decisiones de diseño | Tomadas por el autor; la IA propuso alternativas con sus trade-offs |
| Prompts registrados | Sí — incluidos en cada sesión de esta sección |

La definición del lenguaje, la gramática, los tokens y la arquitectura general del compilador fueron diseñados por el autor. La IA se utilizó como herramienta de implementación, diagnóstico y documentación.

---

## Navegación

- Anterior: [← Testing](07_testing.md)
- Inicio: [↑ Overview](00_overview.md)
