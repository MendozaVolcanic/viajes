"""Reverdecimiento Sentinel-2: NDVI maximo reciente menos NDVI maximo de marzo (estacion seca).
Lee overviews de los COG publicos de Element84 (~160 m), compone por maximo para quitar nubes y camanchaca."""
import os, sys, json
os.environ['AWS_NO_SIGN_REQUEST'] = 'YES'
os.environ['GDAL_DISABLE_READDIR_ON_OPEN'] = 'EMPTY_DIR'
os.environ['CPL_VSIL_CURL_ALLOWED_EXTENSIONS'] = '.tif'
import numpy as np, rasterio
from rasterio.warp import reproject, Resampling
from rasterio.transform import from_origin
from pystac_client import Client
sys.stdout.reconfigure(encoding='utf-8')
LON0, LON1, LAT0, LAT1, RES = -71.36, -70.36, -28.72, -26.84, 0.0015
W = int(round((LON1 - LON0) / RES)); H = int(round((LAT1 - LAT0) / RES))
DST = from_origin(LON0, LAT1, RES, RES)
c = Client.open('https://earth-search.aws.element84.com/v1')

def band(href):
    out = np.full((H, W), np.nan, 'float32')
    with rasterio.open(href, OVERVIEW_LEVEL=2) as src:
        a = src.read(1).astype('float32')
        a[a == 0] = np.nan
        a = np.clip(a - 1000.0, 1.0, None)  # offset BOA de Sentinel-2 (baseline >= 04.00): reflectancia = (DN - 1000) / 10000
        reproject(a, out, src_transform=src.transform, src_crs=src.crs, dst_transform=DST,
                  dst_crs='EPSG:4326', resampling=Resampling.average, src_nodata=np.nan, dst_nodata=np.nan)
    return out

def composite(rng, maxcc):
    items = list(c.search(collections=['sentinel-2-l2a'], bbox=[LON0, LAT0, LON1, LAT1], datetime=rng,
                          query={'eo:cloud_cover': {'lt': maxcc}}, max_items=60).items())
    best = np.full((H, W), np.nan, 'float32'); used = []
    for it in items:
        try:
            r = band(it.assets['red'].href); n = band(it.assets['nir'].href)
        except Exception as e:
            print('  falla', it.id, e); continue
        nd = (n - r) / (n + r)
        best = np.fmax(best, nd); used.append(f"{it.datetime.date()} {it.id.split('_')[1]}")
        print('  ok', used[-1], flush=True)
    return best, used

rec, ur = composite('2026-09-20/2026-10-09', 60)
base, ub = composite('2026-03-01/2026-03-25', 5)
np.save('ndvi_rec.npy', rec); np.save('ndvi_base.npy', base)
json.dump({'reciente': ur, 'base': ub, 'grid': [LON0, LON1, LAT0, LAT1, RES]}, open('ndvi_meta.json', 'w'))
d = rec - base
print('pixeles validos', np.isfinite(d).sum(), 'de', d.size)
for t in (0.03, 0.05, 0.08, 0.12, 0.2):
    print(f'  dNDVI > {t}: {np.nansum(d > t) * (RES * 111.32) ** 2 * 0.885:.0f} km2')
