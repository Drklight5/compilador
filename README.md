<div align="center">

# 🦆 Compilador Patito

**Compilador completo para Patito — micro-lenguaje imperativo procedural**

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=white)
![SLY](https://img.shields.io/badge/Parser-SLY%20LALR(1)-orange)
![Fases](https://img.shields.io/badge/Fases%20completadas-0%20→%204-brightgreen)
![Tests](https://img.shields.io/badge/Tests-22%20passing-success)

<br>

**Valeria Pérez Alonso · A00833973**  
TC3002B.503 — Desarrollo de aplicaciones avanzadas de ciencias computacionales  
Tecnológico de Monterrey

</div>

---

## ¿Qué es Patito?

Patito es un micro-lenguaje imperativo procedural diseñado con fines educativos. Soporta variables enteras y flotantes, funciones con parámetros y retorno, condicionales, ciclos y salida por pantalla.

```patito
programa ejemplo;

vars resultado : entero;

entero factorial(n : entero)
{
    vars r : entero;
    {
        r = n * n;
        regresa r;
    }
};

inicio
{
    resultado = factorial(5);
    escribe("resultado =", resultado);
}
fin
```

---

## Estado del proyecto

| Fase | Descripción | Estado |
|------|-------------|--------|
| **0** | Gramática formal (CFG) y expresiones regulares | ✅ Completa |
| **1** | Análisis léxico y sintáctico (SLY) | ✅ Completa |
| **2** | Análisis semántico — cubo, directorio de funciones, tabla de variables | ✅ Completa |
| **3** | Generación de cuádruplos — expresiones y estatutos lineales | ✅ Completa |
| **4** | Direcciones virtuales, saltos (GotoF/Goto), cuádruplos de funciones | ✅ Completa |
| **5** | Máquina Virtual | 🔜 Próxima |

---

## Inicio rápido

```bash
# Clonar el repositorio
git clone https://github.com/Drklight5/compilador.git
cd compilador

# Instalar dependencia
pip install sly

# Correr todos los tests
python main.py
```

Para compilar un archivo `.pat` específico:

```bash
python -c "
import sys; sys.path.insert(0, 'src')
from lexico.lexer import PatitoLexer
from parser.parser import PatitoParser
code = open('mi_programa.pat').read()
parser = PatitoParser()
parser.parse(PatitoLexer().tokenize(code))
parser.qm.print_quadruples(vm=parser.vm)
"
```

---

## Ejemplo de salida

```
[OK] Compilacion exitosa

--- CONSTANTES ---
  DIR      TIPO         VALOR
  -----------------------------------
  8000     entero       5
  10000    string       "resultado ="

--- CUADRUPLOS ---
  #     OP         IZQ                  DER                  RES
  -----------------------------------------------------------------
  0     Goto       _                    _                    5
  1     *          3000(n)              3000(n)              5000
  2     =          5000                 _                    3001(r)
  3     RETURN     3001(r)              _                    11000
  4     ENDFUNC    _                    _                    _
  5     ERA        factorial            _                    _
  6     PARAM      8000(5)              _                    1
  7     GOSUB      factorial            _                    1
  8     =          11000                _                    5000
  9     =          5000                 _                    1000(resultado)
  10    PRINT      10000("resultado =") _                    _
  11    PRINT      1000(resultado)      _                    _
  12    HALT       _                    _                    _
```

---

## Estructura del proyecto

```
compilador/
├── main.py                     ← punto de entrada, corre todos los tests
├── src/
│   ├── lexico/
│   │   └── lexer.py            ← PatitoLexer (SLY)
│   ├── parser/
│   │   └── parser.py           ← PatitoParser (SLY LALR-1) + puntos neurálgicos
│   ├── semantic/
│   │   ├── semantic_cube.py    ← cubo semántico
│   │   ├── variable_table.py   ← VarEntry, VariableTable
│   │   ├── function_directory.py ← FunctionEntry, FunctionDirectory
│   │   └── semantic_actions.py ← validaciones: tipos, args, regresa...
│   └── intermediate/
│       ├── virtual_memory.py   ← mapa de direcciones 1000–11999
│       ├── quadruple.py        ← estructura Quadruple
│       ├── quadruple_manager.py ← pilas + cola + generación
│       ├── operand_stack.py
│       ├── operator_stack.py
│       ├── type_stack.py
│       └── jump_stack.py       ← backpatch de saltos
├── examples/                   ← 22 archivos .pat de prueba
└── docs/                       ← documentación completa por fase
```

---

## Mapa de memoria virtual

| Segmento | Tipo | Rango |
|----------|------|-------|
| Global | `entero` | 1000 – 1999 |
| Global | `flotante` | 2000 – 2999 |
| Local | `entero` | 3000 – 3999 |
| Local | `flotante` | 4000 – 4999 |
| Temporal | `entero` | 5000 – 5999 |
| Temporal | `flotante` | 6000 – 6999 |
| Temporal | `bool` | 7000 – 7999 |
| Constante | `entero` | 8000 – 8999 |
| Constante | `flotante` | 9000 – 9999 |
| Constante | `string` | 10000 – 10999 |
| Retorno de función | `entero/flotante` | 11000 – 11999 |

---

## Tests

22 casos de prueba en `examples/`:

| Rango | Categoría |
|-------|-----------|
| 01 – 07, 10 | Programas válidos (léxico + sintáctico) |
| 08 – 09 | Errores léxicos y sintácticos esperados |
| 11 – 13 | Semántica válida (retorno, scope local, flotantes) |
| 14 – 22 | Errores semánticos (variable duplicada, tipo incorrecto, regresa inválido...) |

---

## Documentación

La documentación técnica completa está en [`docs/`](docs/):

- [`00_overview.md`](docs/00_overview.md) — Introducción
- [`01_lexico.md`](docs/01_lexico.md) — Tokens y expresiones regulares
- [`02_sintaxis.md`](docs/02_sintaxis.md) — Gramática CFG
- [`03_semantica.md`](docs/03_semantica.md) — Cubo semántico y validaciones
- [`04_codigo_intermedio.md`](docs/04_codigo_intermedio.md) — Cuádruplos y puntos neurálgicos
- [`05_memoria_virtual.md`](docs/05_memoria_virtual.md) — Distribución de direcciones
- [`07_testing.md`](docs/07_testing.md) — Plan de pruebas
- [`08_herramientas_ia.md`](docs/08_herramientas_ia.md) — Uso de IA
