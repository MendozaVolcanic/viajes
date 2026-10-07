# Generador de la página del Desierto Florido 2026

Genera `desierto-florido-2026.html` (raíz del repo) desde `tpl2.html` y los datos de abajo.

Orden: `python ndvi.py` (Sentinel-2, tarda unos 10 min) → `python mask.py` → `python verde.py` → `IMGS=1 python gen2.py`.

Datos de entrada que no van al repo (se regeneran; ver `.gitignore`): `osm.json`, `hw.json`, `prot.json`,
`coast_chains.json` (OpenStreetMap vía Overpass), `osrm_*.json` (rutas OSRM, se recalculan si se borran),
`commons.json` (fotos de Wikimedia Commons), `ndvi_*.npy`, `dndvi_land.npy`, `verde.png`.
