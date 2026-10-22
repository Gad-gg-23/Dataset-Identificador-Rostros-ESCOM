# Dataset: Identificación de compañeros por rostro (con disfraz)

Repo **privado**, **solo de datos**, compartido por los 3 equipos de la práctica de Machine Learning (ESCOM).

## Enlaces rápidos

| Qué | Link |
|---|---|
| Repo (código + metadata) | https://github.com/Gad-gg-23/Dataset-Identificador-Rostros-ESCOM |
| Notebook de Colab (prepara tus fotos sin instalar nada) | [`colab/Identificador_Rostros_Colab.ipynb`](colab/Identificador_Rostros_Colab.ipynb) |
| Script: redimensionar fotos | [`scripts/redimensionar.py`](scripts/redimensionar.py) |
| Script: validar antes de entregar | [`scripts/validar_dataset.py`](scripts/validar_dataset.py) |
| Script: recortar rostros (opcional) | [`scripts/recortar_rostros.py`](scripts/recortar_rostros.py) |
| Script: descargar el dataset ya armado | [`descargar_datos.py`](descargar_datos.py) |
| Dataset (fotos, privado) | https://huggingface.co/datasets/GadiGG/identificador-rostros-escom |
| Metadata del dataset | [`metadata.csv`](metadata.csv) |

## 1. Contexto de la práctica

- El día de la entrega el profesor tomará una foto a un compañero **elegido al azar** y le pondrá algún disfraz o accesorio (peluca, sombrero/gorra, lentes, maquillaje, bigote/barba postiza, bufanda, etc.). El modelo debe identificar **de quién se trata**.
- Se pueden usar **redes neuronales** (ventaja frente a ML clásico para este problema).
- Son **3 equipos**, cada uno con su propio algoritmo/repo de código. Este repo **no tiene algoritmos**, solo datos.
- El disfraz es la condición de **examen** (una sorpresa puntual, no sistemática): el dataset de entrenamiento debe ser mayormente fotos **limpias**, variadas en ropa/ángulo/fondo, para que el modelo aprenda rasgos faciales y de forma reales de la persona. No se busca entrenar "invariancia a disfraces" con volumen de fotos disfrazadas, sino que el modelo sea tan bueno reconociendo rasgos que el disfraz no le afecte.

## 2. Reglas de captura (por persona)

| Parámetro | Valor recomendado |
|---|---|
| Fotos totales | ~1000-1100 (mínimo 1000) |
| Sets | 8-10 sesiones distintas (cambio de ropa entre cada una) |
| Fotos por set | ~110 |
| Disfraz/accesorios | minoritario: como mucho 1 set (o una porción pequeña de fotos dentro de algún set) con gorra/lentes/similar, solo para variar de forma natural — no es el eje del dataset |
| Encuadre | mayoría de 3/4 de cuerpo (rostro con buena resolución y suficiente contexto corporal) |
| Ángulos | Frente, 3/4 izquierda y derecha, perfil, espalda |
| Entornos | Interior y exterior, fondos e iluminación distintos |
| Poses | De pie, caminando, brazos en distintas posiciones |
| Rostro | Visible y nítido en la gran mayoría de las fotos |

**Cómo tomarlas:** fotos directas con el celular (sin video), idealmente que otra persona las tome. Cambiar de pose, ángulo y distancia entre cada foto, evitando el modo ráfaga para no generar fotos casi idénticas. Cada set se puede dividir en 2-3 lugares para ganar variedad de fondo e iluminación.

**Formato uniforme:** JPG calidad 90, ~768×1536 px (vertical) para las de cuerpo completo; las de rostro/medio cuerpo pueden ser más cuadradas, pero misma calidad. Nombres `001.jpg`, `002.jpg`, etc.

> Importante: variedad de ropa, ángulos y fondos pesa más que la cantidad. El objetivo es que el modelo aprenda rasgos faciales/forma de la persona, no a asociarla con una prenda o un fondo — por eso 1000 fotos con 2 outfits son peores que 300 con 10.

## 3. Estructura del repo

```
Identificador_Rostros/
├── README.md             # este archivo
├── CHANGELOG.md          # versiones del dataset
├── metadata.csv          # persona, set_id, accesorios, archivo
├── requirements.txt
├── descargar_datos.py    # baja y descomprime los datos en data/
├── scripts/
│   ├── redimensionar.py      # normaliza tamaño/formato y renombra a 001.jpg, 002.jpg...
│   ├── recortar_rostros.py   # genera faces/ con recortes de rostro (opcional)
│   └── validar_dataset.py    # revisa reglas antes de agregar a alguien
├── .gitignore            # ignora data/ y faces/
├── data/                 # NO va en git, se descarga
│   └── apellido_nombre/
│       ├── set_01/
│       │   ├── 001.jpg
│       │   └── ...
│       ├── set_02/
│       └── ...
└── faces/                # NO va en git, recortes de rostro (opcional)
    └── apellido_nombre/
```

**Convenciones de nombres**
- Carpeta de persona: `apellido_nombre`, minúsculas, sin acentos ni espacios (ej. `garcia_juan`). Así `ImageFolder` de PyTorch/Keras la lee directo como clase.
- Sets: `set_01`, `set_02`, ...

## 4. Alojamiento de los datos (~10-20 GB estimados, ~30,000 fotos)

GitHub no está pensado para esto (recomendado <1 GB por repo, archivos <100 MB; Git LFS gratis da solo 1 GB de almacenamiento y 1 GB de descarga al mes).

**Separar código y datos:**
- **GitHub (este repo, privado):** README, scripts, `metadata.csv`.
- **Datos:** Hugging Face Datasets, repo **privado**: https://huggingface.co/datasets/GadiGG/identificador-rostros-escom
- `descargar_datos.py` baja y descomprime todo en `data/`.

### Cómo se usa (Hugging Face)

**Dar acceso (una vez, lo hace el responsable):**
1. En el dataset → **Settings → Collaborators** → agregar a cada integrante de los 3 equipos por su usuario de Hugging Face (necesitan cuenta propia, gratis).
2. Cada quien genera su token en https://huggingface.co/settings/tokens: el responsable uno con permiso **Write** (para subir), los demás con **Read** (para descargar).

**Subir datos (solo el responsable, cuando reúna las carpetas validadas de varios compañeros en su `data/` local):**
```bash
hf auth login                 # pega tu token Write
hf upload GadiGG/identificador-rostros-escom ./data --repo-type=dataset
```

**Etiquetar una versión:**
```bash
hf repo tag create GadiGG/identificador-rostros-escom v1.0 --repo-type=dataset
```

**Descargar (cada equipo):**
```bash
hf auth login                 # con su propio token Read
python descargar_datos.py --repo GadiGG/identificador-rostros-escom --version v1.0
```

> Nota: `hf` es el CLI nuevo de Hugging Face (antes `huggingface-cli`, sigue funcionando igual). `descargar_datos.py` usa internamente `huggingface_hub.snapshot_download`, ya incluido en `requirements.txt`.

## 5. Metadata

**`metadata.csv`** (una fila por imagen):

```
persona,set_id,archivo
garcia_juan,set_01,001.jpg
garcia_juan,set_02,001.jpg
```

- No se etiqueta ángulo, entorno, fecha ni disfraz: la variedad se logra al **capturar** (cambiar de pose, ángulo y fondo entre fotos), no al etiquetar. El disfraz es la excepción puntual del día del examen, no una categoría del dataset que haya que balancear o marcar.
- El repo **no define splits de train/val/test**: cada equipo usa los datos como quiera.

## 6. Scripts

1. **`scripts/redimensionar.py`**: recibe una carpeta de fotos originales del celular (persona + set), las convierte a JPG calidad 90, ajusta tamaño manteniendo proporción, corrige orientación EXIF y las renombra a `001.jpg`, `002.jpg`... en `data/<persona>/<set>/`.
2. **`scripts/recortar_rostros.py`**: detecta el rostro con MTCNN (`facenet-pytorch`) y guarda recortes en `faces/`. Registra las fotos donde no se detectó rostro (de espalda, mal ángulo, etc.) para que el equipo decida si las usa igual.
3. **`scripts/validar_dataset.py`**: por persona, verifica:
   - Nombre de carpeta válido (sin acentos ni espacios).
   - Mínimo 8 sets y ~1000 imágenes.
   - Todas las imágenes abren bien, formato y tamaño correctos.
   - Sin duplicados casi idénticos (hash perceptual).
   - Persona y sets presentes en `metadata.csv`.
   - Imprime reporte claro (OK / advertencia / error).
4. **`descargar_datos.py`**: descarga desde Hugging Face y descomprime en `data/`, con opción de elegir versión (tag).

## 7. Flujo de trabajo del equipo

### Paso a paso — cada compañero (aporta sus fotos)

1. Toma tus fotos **originales** (sin procesar) y organízalas en `apellido_nombre/set_01/`, `set_02/`... (una carpeta por sesión de ropa).
2. Corre [`scripts/redimensionar.py`](scripts/redimensionar.py) por cada set:
   ```
   python scripts/redimensionar.py --origen "<carpeta_del_set>" --persona apellido_nombre --set set_01
   ```
   Esto genera la versión final en `data/apellido_nombre/set_01/001.jpg, 002.jpg...` (normalizada, renombrada). **No comprime nada**, solo prepara las fotos.
3. Corre [`scripts/validar_dataset.py`](scripts/validar_dataset.py) sobre tu carpeta ya generada:
   ```
   python scripts/validar_dataset.py --persona apellido_nombre
   ```
4. Comprime a mano la carpeta resultante `data/apellido_nombre/` en un `.zip` (así: `apellido_nombre.zip` conteniendo `apellido_nombre/set_01/...`).
5. Entrega ese `.zip` al responsable del dataset (Drive, WhatsApp, etc. — el `.zip` **nunca** se sube al repo de git).

> Alternativa sin instalar nada: el notebook [`colab/Identificador_Rostros_Colab.ipynb`](colab/Identificador_Rostros_Colab.ipynb) hace los pasos 2-4 automáticamente — subes tus fotos originales a Google Drive y el notebook corre `redimensionar.py`, `validar_dataset.py` y te deja el `.zip` listo para descargar.

### Paso a paso — responsable del dataset

1. Recibe el `.zip` de cada compañero y revisa que `validar_dataset.py` no haya marcado errores.
2. Descomprime cada `.zip` dentro de su `data/` local (debe quedar `data/apellido_nombre/set_01/...`).
3. Cuando tenga varios compañeros reunidos, sube todo junto a Hugging Face:
   ```bash
   hf auth login
   hf upload GadiGG/identificador-rostros-escom ./data --repo-type=dataset
   ```
4. Agrega las filas correspondientes en [`metadata.csv`](metadata.csv) (`persona,set_id,archivo`) y súbelas a este repo normalmente (`git add metadata.csv && git commit && git push`).
5. Publica una nueva versión (tag):
   ```bash
   hf repo tag create GadiGG/identificador-rostros-escom v1.0 --repo-type=dataset
   ```
   Nadie cambia datos a media práctica sin avisar: cada equipo fija la versión que usa con [`descargar_datos.py`](descargar_datos.py). Detalle completo en la [sección 4](#4-alojamiento-de-los-datos-10-20-gb-estimados-30000-fotos).

## 8. Recomendación de uso (no es una regla)

Cada equipo decide cómo dividir y usar los datos. Un consejo para que los resultados sean confiables: **si dividen en train/val/test, háganlo por set (por ropa) y no por foto al azar.** Si el mismo set queda en train y en test, el modelo parece excelente en la práctica pero falla con ropa nueva el día del examen.

## 9. Privacidad y consentimiento

- Estas fotos son **datos biométricos** (rostro de compañeros identificables): repo y dataset deben mantenerse **privados**, sin excepción, solo accesibles a los 3 equipos y al profesor.
- Pedir **consentimiento por escrito** a cada compañero antes de incluir sus fotos (lista firmada guardada fuera del repo, no en git).
- El README y el consentimiento deben decir explícitamente: uso exclusivo para esta práctica, prohibido redistribuir o usar fuera del curso, prohibido usarlas para entrenar o alimentar cualquier sistema de reconocimiento facial fuera de esta práctica, y se borran todos los datos (en Hugging Face/Releases y copias locales) al terminar el curso.
