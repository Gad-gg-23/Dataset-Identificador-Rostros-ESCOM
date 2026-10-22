# Guía paso a paso — Identificador de rostros (ESCOM)

Esta guía es para los **3 líderes de equipo** y para **cada compañero** que va a aportar sus fotos. Sigue tu sección según tu rol.

## Enlaces que vas a usar

| Qué | Link |
|---|---|
| Repo de código (GitHub, privado) | https://github.com/Gad-gg-23/Dataset-Identificador-Rostros-ESCOM |
| Dataset de fotos (Hugging Face, privado) | https://huggingface.co/datasets/GadiGG/identificador-rostros-escom |
| Notebook de Colab | https://colab.research.google.com/github/Gad-gg-23/Dataset-Identificador-Rostros-ESCOM/blob/main/colab/Identificador_Rostros_Colab.ipynb |
| Editar `metadata.csv` directo en el navegador | https://github.com/Gad-gg-23/Dataset-Identificador-Rostros-ESCOM/edit/main/metadata.csv |
| Generar token de GitHub | https://github.com/settings/tokens |
| Generar token de Hugging Face | https://huggingface.co/settings/tokens |

---

## Parte 1 — Qué hace CADA COMPAÑERO (aporte tus fotos)

No necesitas cuenta de GitHub ni de Hugging Face para esta parte. Solo necesitas una cuenta de Google (para Colab/Drive) **o** tener Python instalado si lo vas a hacer en tu computadora.

### 1.1 Toma tus fotos

- 8 a 10 sets (sesiones con ropa distinta), ~110 fotos por set, ~1000-1100 fotos en total.
- La mayoría **3/4 de cuerpo**, rostro visible y nítido.
- Varía ángulo (frente, 3/4, perfil, espalda), pose, fondo e iluminación entre fotos.
- Como mucho **1 set** (o parte de uno) con algo de disfraz (gorra, lentes, etc.) — no es el foco, el disfraz es la sorpresa del examen, no algo que haya que repetir mucho en las fotos de entrenamiento.
- Evita modo ráfaga (fotos casi idénticas).

Guía completa de reglas: sección 2 del [README](https://github.com/Gad-gg-23/Dataset-Identificador-Rostros-ESCOM#2-reglas-de-captura-por-persona).

### 1.2 Organiza las fotos originales (sin procesar todavía)

Crea una carpeta por set:

```
set_01/   (fotos de esa sesión, tal como salieron del celular)
set_02/
set_03/
...
```

### 1.3 Procesa tus fotos — elige UNA opción

**Opción A: Google Colab (no instalas nada)**

1. Sube la carpeta de arriba a tu Google Drive, en esta ruta exacta:
   ```
   MyDrive/FotosIdentificador/<apellido_nombre>/set_01/
   MyDrive/FotosIdentificador/<apellido_nombre>/set_02/
   ...
   ```
   `<apellido_nombre>` = tu nombre en minúsculas, sin acentos ni espacios (ej. `garcia_juan`).
2. Abre el notebook: https://colab.research.google.com/github/Gad-gg-23/Dataset-Identificador-Rostros-ESCOM/blob/main/colab/Identificador_Rostros_Colab.ipynb
   - Si te abre como vista previa de GitHub en vez de Colab, copia esa misma URL y pégala directo en una pestaña nueva del navegador.
   - Como el repo es privado, la primera vez te va a pedir **autorizar a Colab a usar tu cuenta de GitHub**: dale clic a "Autorizar con GitHub" y acepta en la ventana que se abre. Si después de autorizar sigue sin cargar, descarga el `.ipynb` del repo (botón de descarga en GitHub) y súbelo a Colab con Archivo → Subir cuaderno → pestaña Subir.
3. Corre las celdas **en orden**, de arriba hacia abajo:
   - **Celda "Clonar el repo"**: te pide tu usuario de GitHub y un Personal Access Token. Genera el token en https://github.com/settings/tokens → "Generate new token (classic)" → marca el scope `repo`. (Necesitas que tu líder de equipo ya te haya dado acceso de colaborador al repo — si no, pídeselo antes de este paso.)
   - **Instalar dependencias**: solo corre la celda, no pide nada.
   - **Montar Google Drive**: te va a pedir permiso, acéptalo.
   - **Configurar tus datos**: cambia `PERSONA = "apellido_nombre"` por tu nombre real.
   - **Redimensionar cada set**: lo hace automático, tarda un rato si tienes muchas fotos.
   - **Validar**: revisa el reporte. Si salió algún **error**, corrige tus fotos en Drive y vuelve a correr la celda de redimensionar.
   - **Generar tus filas para metadata.csv**: imprime texto, cópialo (lo usas en el paso 1.4).
   - **Comprimir y descargar tu .zip**: te descarga `<tu_nombre>.zip` a tu computadora.

**Opción B: en tu computadora (si tienes Python instalado)**

1. Clona el repo una vez:
   ```bash
   git clone https://github.com/Gad-gg-23/Dataset-Identificador-Rostros-ESCOM.git
   cd Dataset-Identificador-Rostros-ESCOM
   pip install -r requirements.txt
   ```
2. Por cada set, corre:
   ```bash
   python scripts/redimensionar.py --origen "<ruta_a_tu_set>" --persona apellido_nombre --set set_01
   ```
3. Valida:
   ```bash
   python scripts/validar_dataset.py --persona apellido_nombre
   ```
4. Genera tus filas de metadata:
   ```bash
   python scripts/generar_metadata.py --persona apellido_nombre
   ```
5. Comprime la carpeta `data/apellido_nombre/` en un `.zip`.

### 1.4 Entrega tu parte a tu líder de equipo

Mándale a tu líder, por WhatsApp/Drive/lo que usen:
1. Tu archivo `apellido_nombre.zip`.
2. El texto que te imprimió `generar_metadata.py` (las líneas `apellido_nombre,set_XX,archivo.jpg`).

Si **a ti** también te dieron acceso de colaborador en GitHub, puedes pegar esas líneas tú mismo en https://github.com/Gad-gg-23/Dataset-Identificador-Rostros-ESCOM/edit/main/metadata.csv (al final del archivo) y darle "Commit changes directly to the main branch" — en ese caso no hace falta que se las mandes a tu líder.

**El `.zip` nunca se sube a GitHub** (ni tú ni tu líder lo suben ahí) — GitHub solo guarda código y `metadata.csv`. Las fotos van a Hugging Face (lo hace tu líder, parte 2).

---

## Parte 2 — Qué hace CADA LÍDER DE EQUIPO (3 personas)

Tú haces todo lo de la Parte 1 para tus propias fotos, **más** lo siguiente para juntar a tu equipo y subirlo.

### 2.1 Cuentas que necesitas

1. **Cuenta de GitHub** (si no tienes, créala gratis en https://github.com/join).
2. **Cuenta de Hugging Face** (gratis, en https://huggingface.co/join).
3. Pide a quien administra el repo (`Gad-gg-23` / `GadiGG`) que te agregue como colaborador en:
   - GitHub: repo → Settings → Collaborators → te manda invitación → la aceptas (correo o notificación en GitHub).
   - Hugging Face: dataset → Settings → Collaborators → te manda invitación → la aceptas.
   
   > Nota: en repos de cuenta personal (como este) GitHub no deja elegir un "rol" al invitar — todo colaborador agregado ahí recibe automáticamente permiso de escritura (push), así que no falta ningún paso si no ves selector de rol.
4. Genera tus tokens:
   - GitHub: https://github.com/settings/tokens → "Generate new token (classic)" → scope `repo`.
   - Hugging Face: https://huggingface.co/settings/tokens → tipo **Write**.

### 2.2 Pide los datos a tu equipo

Manda a cada integrante de tu equipo las instrucciones de la **Parte 1** de esta guía (o directo el link de esta guía). Pídeles específicamente:
- Su `apellido_nombre.zip`.
- El texto que les imprimió `generar_metadata.py`.

Dales una fecha límite para que no se junte todo al final.

### 2.3 Junta las filas de metadata.csv

Por cada compañero que te mandó sus líneas (y las tuyas propias):
1. Ve a https://github.com/Gad-gg-23/Dataset-Identificador-Rostros-ESCOM/edit/main/metadata.csv (abre el editor web directo).
2. Pega todas las líneas nuevas al final del archivo (una por imagen).
3. Hasta abajo de la página, en "Commit changes" → escribe un mensaje corto (ej. "Agrega fotos de equipo X") → "Commit directly to the main branch".

### 2.4 Junta las fotos en tu computadora

1. Descomprime cada `.zip` que te mandaron (incluyendo el tuyo) **dentro de una carpeta `data/`**, de forma que quede así:
   ```
   data/
   ├── apellido_nombre_1/
   │   ├── set_01/
   │   └── ...
   ├── apellido_nombre_2/
   │   ├── set_01/
   │   └── ...
   └── ...
   ```
   (Si ya tenías el repo clonado de la Parte 1, úsalo ahí mismo; `data/` está en `.gitignore`, así que no se sube a GitHub aunque esté dentro del repo clonado.)

### 2.5 Sube las fotos de tu equipo a Hugging Face

```bash
pip install -U huggingface_hub   # si no lo tienes instalado
hf auth login                    # pega tu token con permiso Write
hf upload GadiGG/identificador-rostros-escom ./data --repo-type=dataset
```

Esto sube **solo lo que está en tu carpeta `data/` local** (tu equipo). No borra ni toca lo que ya subieron los otros 2 líderes, así que los 3 pueden hacer esto por su cuenta sin coordinarse en el momento exacto.

### 2.6 Avisa a los otros 2 líderes

Cuando termines, avísales (chat del grupo) que ya subiste tu equipo completo, para llevar control de quién falta.

### 2.7 Cuando los 3 equipos ya subieron: publiquen una versión

Cualquiera de los 3 líderes corre (una sola vez, cuando ya esté todo reunido):

```bash
hf repo tag create GadiGG/identificador-rostros-escom v1.0 --repo-type=dataset
```

Avisen a todo el salón qué versión (`v1.0`, `v1.1`...) usar para descargar y entrenar:

```bash
python descargar_datos.py --repo GadiGG/identificador-rostros-escom --version v1.0
```

### 2.8 Si más adelante van a entrenar modelos (cada equipo)

Cuando los integrantes de tu equipo necesiten descargar el dataset completo para entrenar (no solo subir sus propias fotos), van a necesitar acceso de **Read** al dataset de Hugging Face. Agrégalos ahí (dataset → Settings → Collaborators → rol Read) cuando llegue esa etapa — no hace falta dárselo antes.

---

## Resumen ultra-corto

```
Compañero:  fotos → (Colab o local) redimensionar → validar → generar_metadata → zip
                 → manda zip + líneas de metadata a su líder

Líder:      recibe zips y líneas de todo su equipo
                 → pega las líneas en metadata.csv (GitHub)
                 → junta los zips en su carpeta data/
                 → hf upload a Hugging Face
                 → avisa que terminó

3 líderes listos → uno publica el tag de versión (v1.0) → todo el salón descarga para entrenar
```
