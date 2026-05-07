from lexer import PatitoLexer
from parser import PatitoParser

import os
import glob


# Direccion base y carpeta de tests
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TESTS_DIR = os.path.join(BASE_DIR, "tests")

def ejecutar_prueba(archivo):

    print("\n==================================================")
    print(f" Ejecutando: {archivo}")
    print("==================================================")

    try:
        with open(archivo, 'r', encoding='utf-8') as f:
            data = f.read()

    except FileNotFoundError:
        print(f"[ERROR] No se encontró el archivo: {archivo}")
        return

    lexer = PatitoLexer()
    parser = PatitoParser()

    # -------------------------------------------------
    # ANALISIS LEXICO
    # -------------------------------------------------

    print("\n--- TOKENS ---")

    try:
        tokens = list(lexer.tokenize(data))

        for token in tokens:
            print(token)

    except Exception as e:
        print(f"[LEXER ERROR] {e}")
        return

    # -------------------------------------------------
    # ANALISIS SINTACTICO
    # -------------------------------------------------

    print("\n--- PARSER ---")

    try:
        resultado = parser.parse(iter(tokens))

        if resultado is None:
            print("[PARSER ERROR] No se pudo generar el AST")
            return  
        else:
            print("[OK] Compilación exitosa")

        print("\nAST:")
        print(resultado)

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