"""
Detecta y recorta el rostro de cada foto en data/, guardando el resultado en faces/.
Útil para equipos que entrenen directamente sobre el rostro en vez de la imagen completa.

Requiere: facenet-pytorch (pip install facenet-pytorch)

Uso:
    python recortar_rostros.py --raiz data --destino faces
"""
import argparse
import sys
from pathlib import Path

from PIL import Image

try:
    from facenet_pytorch import MTCNN
except ImportError:
    sys.exit("Error: falta facenet-pytorch. Instala con: pip install facenet-pytorch")

MARGEN = 0.3  # margen extra alrededor del rostro detectado, proporcional a su tamaño


def recortar_con_margen(img: Image.Image, caja, margen: float) -> Image.Image:
    x1, y1, x2, y2 = caja
    ancho_margen = (x2 - x1) * margen
    alto_margen = (y2 - y1) * margen
    x1 = max(0, x1 - ancho_margen)
    y1 = max(0, y1 - alto_margen)
    x2 = min(img.width, x2 + ancho_margen)
    y2 = min(img.height, y2 + alto_margen)
    return img.crop((int(x1), int(y1), int(x2), int(y2)))


def main():
    parser = argparse.ArgumentParser(description="Recorta rostros detectados en el dataset.")
    parser.add_argument("--raiz", default="data", help="Carpeta raíz data/ (default: data)")
    parser.add_argument("--destino", default="faces", help="Carpeta raíz faces/ (default: faces)")
    args = parser.parse_args()

    raiz = Path(args.raiz)
    destino = Path(args.destino)
    if not raiz.is_dir():
        sys.exit(f"Error: no existe '{raiz}'")

    mtcnn = MTCNN(keep_all=False)

    sin_rostro = []
    procesadas = 0

    for persona_dir in sorted(raiz.iterdir()):
        if not persona_dir.is_dir():
            continue
        for set_dir in sorted(persona_dir.iterdir()):
            if not set_dir.is_dir():
                continue
            carpeta_salida = destino / persona_dir.name / set_dir.name
            carpeta_salida.mkdir(parents=True, exist_ok=True)
            for foto in sorted(set_dir.glob("*.jpg")):
                try:
                    with Image.open(foto) as img:
                        caja, _ = mtcnn.detect(img)
                        if caja is None:
                            sin_rostro.append(str(foto))
                            continue
                        recorte = recortar_con_margen(img, caja[0], MARGEN)
                        recorte.save(carpeta_salida / foto.name, "JPEG", quality=90)
                        procesadas += 1
                except Exception as e:
                    print(f"Error en {foto}: {e}")

    print(f"OK: {procesadas} rostros recortados en {destino}")
    if sin_rostro:
        print(f"Advertencia: {len(sin_rostro)} fotos sin rostro detectado (disfraz, de espalda, etc.):")
        for ruta in sin_rostro[:20]:
            print(f"  - {ruta}")
        if len(sin_rostro) > 20:
            print(f"  ... y {len(sin_rostro) - 20} más")


if __name__ == "__main__":
    main()
