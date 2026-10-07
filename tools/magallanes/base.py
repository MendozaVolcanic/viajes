"""Mascara de mar para Magallanes.
La costa de OSM va con la tierra a la izquierda y el mar a la derecha. Se marcan puntos a cada lado de
cada tramo y cada pixel toma la clase del marcador mas cercano (asi no hay fugas por el borde del mapa)."""
import json, math, numpy as np
from scipy.ndimage import distance_transform_edt
from PIL import Image
LAT0, LAT1, LON0, LON1, RES = -53.72, -50.75, -73.45, -69.85, 0.003
W = int(round((LON1 - LON0) / RES)); H = int(round((LAT1 - LAT0) / RES))
K = math.cos(math.radians(-52.2))
d = json.load(open('coast.json', encoding='utf-8'))['elements']
mark = np.zeros((H, W), 'int8')  # 1 tierra, 2 mar
OFF = 1.5 * RES
def put(la, lo, v):
    i = int((LAT1 - la) / RES); j = int((lo - LON0) / RES)
    if 0 <= i < H and 0 <= j < W and mark[i, j] == 0:
        mark[i, j] = v
for e in d:
    g = e.get('geometry') or []
    for a, b in zip(g, g[1:]):
        x = (b['lon'] - a['lon']) * K; y = b['lat'] - a['lat']; L = math.hypot(x, y)
        if L == 0: continue
        nsteps = max(1, int(L / RES))
        for s in range(nsteps):
            t = (s + 0.5) / nsteps
            lo = a['lon'] + (b['lon'] - a['lon']) * t; la = a['lat'] + (b['lat'] - a['lat']) * t
            rx, ry = y / L, -x / L  # normal a la derecha (mar)
            put(la + ry * OFF, lo + rx * OFF / K, 2)
            put(la - ry * OFF, lo - rx * OFF / K, 1)
_, (ii, jj) = distance_transform_edt(mark == 0, return_indices=True)
cls = mark[ii, jj]
sea = cls == 2
print('fraccion mar', round(float(sea.mean()), 3), 'grid', W, H)
for n, la, lo in [('Punta Arenas', -53.16, -70.95), ('Natales', -51.73, -72.49), ('Laguna Amarga', -50.97, -72.75),
                  ('Estrecho', -53.30, -70.60), ('Pacifico', -52.4, -73.40), ('Seno Otway', -52.85, -71.30), ('Ultima Esperanza', -51.70, -72.56)]:
    i = int((LAT1 - la) / RES); j = int((lo - LON0) / RES); print(f'  {n}: {"mar" if sea[i, j] else "tierra"}')
rgba = np.zeros((H, W, 4), 'uint8'); rgba[sea] = (255, 255, 255, 255)
Image.fromarray(rgba, 'RGBA').save('mar.png', optimize=True)
json.dump({'grid': [LON0, LON1, LAT0, LAT1, RES]}, open('mar_meta.json', 'w'))
