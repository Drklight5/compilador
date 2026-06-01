import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'src'))

from lexico.lexer import PatitoLexer
from parser.parser import PatitoParser

import glob

BASE_DIR  = os.path.dirname(os.path.abspath(__file__))
TESTS_DIR = os.path.join(BASE_DIR, 'examples')


def ejecutar_prueba(archivo):
    print("\n==================================================")
    print(f" Ejecutando: {os.path.basename(archivo)}")
    print("==================================================")

    try:
        with open(archivo, 'r', encoding='utf-8') as f:
            data = f.read()
    except FileNotFoundError:
        print(f"[ERROR] No se encontro el archivo: {archivo}")
        return

    lexer  = PatitoLexer()
    parser = PatitoParser()

    try:
        tokens    = list(lexer.tokenize(data))
        resultado = parser.parse(iter(tokens))

        if resultado is None:
            print("[PARSER ERROR] No se pudo compilar")
            return

        print("[OK] Compilacion exitosa")

        # ── Tabla de constantes ──────────────────────────────────────
        consts = parser.vm.get_constants_table()
        if consts:
            print("\n--- CONSTANTES ---")
            print(f"  {'DIR':<8} {'TIPO':<12} {'VALOR'}")
            print("  " + "-" * 35)
            for addr, tipo, val in consts:
                print(f"  {addr:<8} {tipo:<12} {val}")

        # ── Cuádruplos ───────────────────────────────────────────────
        if parser.qm.count() > 0:
            print("\n--- CUADRUPLOS ---")
            parser.qm.print_quadruples(vm=parser.vm)

    except Exception as e:
        print(f"[PARSER ERROR] {e}")


def main():
    if not os.path.exists(TESTS_DIR):
        print(f"[ERROR] No existe la carpeta '{TESTS_DIR}'")
        return

    archivos = sorted(glob.glob(os.path.join(TESTS_DIR, "*.pat")))

    if not archivos:
        print("[ERROR] No se encontraron archivos .pat")
        return

    print("========================================")
    print("      EJECUCION DE TESTS PATITO")
    print("========================================")

    for archivo in archivos:
        ejecutar_prueba(archivo)

    print("\n========================================")
    print("      FIN DE EJECUCION DE TESTS")
    print("========================================")


if __name__ == "__main__":
    main()
