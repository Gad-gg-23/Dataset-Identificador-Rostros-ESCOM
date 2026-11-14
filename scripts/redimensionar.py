"""
Normaliza fotos originales del celular a data/<persona>/<set_id>/001.jpg, 002.jpg...

Uso:
    python redimensionar.py --origen "C:/fotos/garcia_juan/set_01" --persona garcia_juan --set set_01
"""
import argparse
import sys
import unicodedata
from pathlib import Path

from PIL import Image, ImageOps

try:
    from pillow_heif import register_heif_opener
    register_heif_opener()
except ImportError:
    pass  # fotos .heic/.heif fallaran si falta "pip install pillow-heif"

EXTENSIONES_VALIDAS = {".jpg", ".jpeg", ".png", ".heic", ".heif", ".webp"}
ANCHO_OBJETIVO = 768
ALTO_OBJETIVO = 1536
CALIDAD_JPG = 90


def es_nombre_valido(nombre: str) -> bool:
    normalizado = unicodedata.normalize("NFKD", nombre)
    sin_acentos = "".join(c for c in normalizado if not unicodedata.combining(c))
    return sin_acentos == nombre and " " not in nombre and nombre == nombre.lower()


def redimensionar_manteniendo_proporcion(img: Image.Image, ancho_max: int, alto_max: int) -> Image.Image:
    img = ImageOps.exif_transpose(img)
    proporcion = min(ancho_max / img.width, alto_max / img.height)
    if proporcion < 1:
        nuevo_tamano = (int(img.width * proporcion), int(img.height * proporcion))
        img = img.resize(nuevo_tamano, Image.LANCZOS)
    return img.convert("RGB")


def main():
    parser = argparse.ArgumentParser(description="Normaliza fotos a formato uniforme del dataset.")
    parser.add_argument("--origen", required=True, help="Carpeta con las fotos originales del celular")
    parser.add_argument("--persona", required=True, help="apellido_nombre, sin acentos ni espacios")
    parser.add_argument("--set", dest="set_id", required=True, help="Identificador del set, ej. set_01")
    parser.add_argument("--destino", default="data", help="Carpeta raíz de datos (default: data)")
    args = parser.parse_args()

    if not es_nombre_valido(args.persona):
        sys.exit(f"Error: '{args.persona}' debe ser minúsculas, sin acentos ni espacios (ej. garcia_juan)")

    origen = Path(args.origen)
    if not origen.is_dir():
        sys.exit(f"Error: no existe la carpeta de origen '{origen}'")

    destino = Path(args.destino) / args.persona / args.set_id
    destino.mkdir(parents=True, exist_ok=True)

    archivos = sorted(
        p for p in origen.iterdir() if p.suffix.lower() in EXTENSIONES_VALIDAS
    )
    if not archivos:
        sys.exit(f"Error: no se encontraron imágenes en '{origen}'")

    convertidas = 0
    errores = []
    for i, archivo in enumerate(archivos, start=1):
        try:
            with Image.open(archivo) as img:
                img = redimensionar_manteniendo_proporcion(img, ANCHO_OBJETIVO, ALTO_OBJETIVO)
                salida = destino / f"{i:03d}.jpg"
                img.save(salida, "JPEG", quality=CALIDAD_JPG)
                convertidas += 1
        except Exception as e:
            errores.append((archivo.name, str(e)))

    print(f"OK: {convertidas} fotos guardadas en {destino}")
    if errores:
        print(f"Advertencia: {len(errores)} fotos no se pudieron procesar:")
        for nombre, error in errores:
            print(f"  - {nombre}: {error}")


if __name__ == "__main__":
    main()
