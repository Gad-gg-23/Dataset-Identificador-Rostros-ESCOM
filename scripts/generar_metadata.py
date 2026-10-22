"""
Genera las filas de metadata.csv para una persona, a partir de lo que ya
tiene en su carpeta data/<persona>/. Pensado para copiar/pegar el resultado
directo en el editor web de GitHub (no hace falta git ni permisos de escritura
en el repo para usarlo).

Uso:
    python generar_metadata.py --persona garcia_juan
    python generar_metadata.py --persona garcia_juan --salida garcia_juan_metadata.csv
"""
import argparse
import sys
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description="Genera filas de metadata.csv para una persona.")
    parser.add_argument("--persona", required=True)
    parser.add_argument("--raiz", default="data")
    parser.add_argument("--salida", help="Si se indica, guarda el resultado en este archivo en vez de imprimirlo")
    args = parser.parse_args()

    carpeta_persona = Path(args.raiz) / args.persona
    if not carpeta_persona.is_dir():
        sys.exit(f"Error: no existe '{carpeta_persona}'")

    sets = sorted(p for p in carpeta_persona.iterdir() if p.is_dir())
    if not sets:
        sys.exit(f"Error: '{carpeta_persona}' no tiene carpetas de set")

    lineas = []
    for set_dir in sets:
        for foto in sorted(set_dir.glob("*.jpg")):
            lineas.append(f"{args.persona},{set_dir.name},{foto.name}")

    if not lineas:
        sys.exit("Error: no se encontraron fotos .jpg")

    resultado = "\n".join(lineas)

    if args.salida:
        Path(args.salida).write_text(resultado + "\n", encoding="utf-8")
        print(f"OK: {len(lineas)} filas guardadas en {args.salida}")
    else:
        print(f"--- Copia estas {len(lineas)} filas al final de metadata.csv ---")
        print(resultado)


if __name__ == "__main__":
    main()
