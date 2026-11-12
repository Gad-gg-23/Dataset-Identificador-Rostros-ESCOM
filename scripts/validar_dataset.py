"""
Valida que una persona cumpla las reglas del dataset antes de integrarla.

Uso:
    python validar_dataset.py --persona garcia_juan --raiz data --metadata metadata.csv
"""
import argparse
import sys
import unicodedata
from pathlib import Path

import imagehash
import pandas as pd
from PIL import Image

MIN_SETS = 8
MIN_FOTOS = 1000
AREA_MIN = 400 * 400  # resolución mínima total, sin importar orientación
LADO_MIN = 200  # evita tiras extremadamente delgadas (panorámicas, recortes raros)
UMBRAL_HASH_DUPLICADO = 3  # distancia de Hamming entre hashes perceptuales


def es_nombre_valido(nombre: str) -> bool:
    normalizado = unicodedata.normalize("NFKD", nombre)
    sin_acentos = "".join(c for c in normalizado if not unicodedata.combining(c))
    return sin_acentos == nombre and " " not in nombre and nombre == nombre.lower()


def main():
    parser = argparse.ArgumentParser(description="Valida el dataset de una persona.")
    parser.add_argument("--persona", required=True)
    parser.add_argument("--raiz", default="data")
    parser.add_argument("--metadata", default="metadata.csv")
    args = parser.parse_args()

    errores = []
    advertencias = []

    if not es_nombre_valido(args.persona):
        errores.append(f"Nombre de carpeta inválido: '{args.persona}' (debe ser minúsculas, sin acentos/espacios)")

    carpeta_persona = Path(args.raiz) / args.persona
    if not carpeta_persona.is_dir():
        sys.exit(f"Error fatal: no existe '{carpeta_persona}'")

    sets = sorted(p for p in carpeta_persona.iterdir() if p.is_dir())
    if len(sets) < MIN_SETS:
        errores.append(f"Solo {len(sets)} sets, se requieren al menos {MIN_SETS}")

    todas_fotos = []
    for set_dir in sets:
        todas_fotos.extend(sorted(set_dir.glob("*.jpg")))

    if len(todas_fotos) < MIN_FOTOS:
        errores.append(f"Solo {len(todas_fotos)} fotos, se requieren al menos {MIN_FOTOS}")

    hashes = {}
    duplicados = 0
    fotos_invalidas = 0
    for foto in todas_fotos:
        try:
            with Image.open(foto) as img:
                img.verify()
            with Image.open(foto) as img:
                lado_corto = min(img.width, img.height)
                if img.width * img.height < AREA_MIN or lado_corto < LADO_MIN:
                    fotos_invalidas += 1
                    continue
                h = imagehash.phash(img)
                for h_previo in hashes.values():
                    if h - h_previo <= UMBRAL_HASH_DUPLICADO:
                        duplicados += 1
                        break
                hashes[str(foto)] = h
        except Exception:
            fotos_invalidas += 1

    if fotos_invalidas:
        errores.append(f"{fotos_invalidas} fotos no abren bien o son demasiado pequeñas")
    if duplicados:
        advertencias.append(f"{duplicados} fotos parecen casi duplicadas (hash perceptual)")

    metadata_path = Path(args.metadata)
    if metadata_path.is_file():
        df = pd.read_csv(metadata_path)
        filas_persona = df[df["persona"] == args.persona]
        if filas_persona.empty:
            errores.append(f"'{args.persona}' no aparece en {metadata_path}")
        else:
            sets_en_csv = set(filas_persona["set_id"])
            sets_en_disco = {s.name for s in sets}
            faltantes = sets_en_disco - sets_en_csv
            if faltantes:
                errores.append(f"Sets en disco pero no en metadata.csv: {sorted(faltantes)}")
    else:
        advertencias.append(f"No se encontró {metadata_path}, se omite el cruce de información")

    print(f"--- Validación de '{args.persona}' ---")
    print(f"Sets encontrados: {len(sets)}")
    print(f"Fotos encontradas: {len(todas_fotos)}")

    if not errores and not advertencias:
        print("OK: todo correcto")
    if advertencias:
        print("\nAdvertencias:")
        for a in advertencias:
            print(f"  - {a}")
    if errores:
        print("\nErrores:")
        for e in errores:
            print(f"  - {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
