### Permite obtener el padron electoral del Servel

Se ha probado con la data de:
"padron definitivo de elecciones de convencionales constituyentes, gobernadores regionales, alcaldes y concejales 2021"

Última fecha de funcionamiento: 11 de Mayo 2021

#### Corriendo el script

Se requiere python 3.8 o superior

Primero debes instalar las dependencias

```bash
pip install -r ./requirements.txt
```

Luego puedes crear tu script customizado

```python
from servel_scraper.servel_pipeline.servel_pipeline import ServelPipeline, PipelineStage

# Aqui se descargaran los pdfs
DEFAULT_PDF_DOWNLOAD_PATH = "../out/raw"

# Aquí se guardarán los csv generados
DEFAULT_GENERATED_CSV_PATH = '../out/clean'

p = ServelPipeline(DEFAULT_PDF_DOWNLOAD_PATH, DEFAULT_GENERATED_CSV_PATH)
p.run_pipeline([
    PipelineStage.DOWNLOAD_PDFS,
    PipelineStage.EXTRACT_CSV_FROM_PDF
])
```

#### ¿De donde se obtiene esta data?:

Los ficheros del padrón electoral son públicos y están almacenados en una url como la siguiente

"http://cdn.servel.cl/padron/CODIGO_UNICO_TERRITORIAL.pdf"

Donde CODIGO_UNICO_TERRITORIAL se puede obtener del fichero "data/codigo_de_comunas.csv"

Ejemplo:

http://cdn.servel.cl/padron/A01107.pdf

#### ¿Como funciona este script?

1: Descarga cada uno de los pdfs

2: Por cada pdf descargado genera un csv con la data

#### Notas:

Este repositorio tiene fines puramente académicos.

La utilización de este código y de la data recabada es de responsabilidad exclusiva del usuario.