"""
Descarga y descomprime el dataset en data/.

Fuente: Hugging Face Datasets (repo privado) - https://huggingface.co/datasets/escom-identificador-rostros/identificador-rostros-escom
Requiere haber hecho login antes: hf auth login (o variable HF_TOKEN).

Uso:
    python descargar_datos.py --repo escom-identificador-rostros/identificador-rostros-escom --version v1.0

--zip queda como alternativa si en algún momento se reparte un .zip por otro medio (Drive, etc.):
    python descargar_datos.py --zip "https://.../data.zip"
"""
import argparse
import sys
import zipfile
from pathlib import Path

import requests
from tqdm import tqdm


def descargar_desde_huggingface(repo: str, version: str, destino: Path):
    try:
        from huggingface_hub import snapshot_download
    except ImportError:
        sys.exit("Error: falta huggingface_hub. Instala con: pip install huggingface_hub")

    print(f"Descargando '{repo}' (revisión: {version}) desde Hugging Face...")
    ruta_local = snapshot_download(
        repo_id=repo,
        repo_type="dataset",
        revision=version,
        local_dir=destino,
    )
    print(f"OK: datos descargados en {ruta_local}")


def descargar_zip(url: str, destino: Path):
    destino.mkdir(parents=True, exist_ok=True)
    nombre_zip = destino / "data_descarga.zip"

    print(f"Descargando {url} ...")
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        total = int(r.headers.get("content-length", 0))
        with open(nombre_zip, "wb") as f, tqdm(total=total, unit="B", unit_scale=True) as barra:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
                barra.update(len(chunk))

    print("Descomprimiendo...")
    with zipfile.ZipFile(nombre_zip) as z:
        z.extractall(destino)
    nombre_zip.unlink()
    print(f"OK: datos descomprimidos en {destino}")


def main():
    parser = argparse.ArgumentParser(description="Descarga el dataset a data/.")
    parser.add_argument("--repo", help="Repo de Hugging Face Datasets, ej. mi-org/identificador-rostros-escom")
    parser.add_argument("--version", default="main", help="Tag/revisión a descargar (default: main)")
    parser.add_argument("--zip", help="URL directa a un .zip (alternativa a --repo, ej. GitHub Releases)")
    parser.add_argument("--destino", default="data", help="Carpeta destino (default: data)")
    args = parser.parse_args()

    destino = Path(args.destino)

    if args.zip:
        descargar_zip(args.zip, destino)
    elif args.repo:
        descargar_desde_huggingface(args.repo, args.version, destino)
    else:
        sys.exit("Error: especifica --repo (Hugging Face) o --zip (descarga directa)")


if __name__ == "__main__":
    main()
