"""dNDVI sobre tierra: (NDVI max reciente - NDVI max de marzo), enmascarado con la costa OSM y suavizado 3x3 ignorando NaN."""
import json, numpy as np
import rasterio.features as rf
from rasterio.transform import from_origin
from scipy.ndimage import generic_filter
LON0, LON1, LAT0, LAT1, RES = json.load(open('ndvi_meta.json'))['grid']
W = int(round((LON1 - LON0) / RES)); H = int(round((LAT1 - LAT0) / RES)); T = from_origin(LON0, LAT1, RES, RES)
d = np.load('ndvi_rec.npy') - np.load('ndvi_base.npy')
chains = json.load(open('coast_chains.json'))
main = [p for p in chains[0] if LAT0 - 0.3 < p[0] < LAT1 + 0.3]
ring = [(lo, la) for la, lo in main] + [(LON1 + 0.5, LAT0 - 0.3), (LON1 + 0.5, LAT1 + 0.3)]
land = rf.rasterize([({'type': 'Polygon', 'coordinates': [ring + [ring[0]]]}, 1)], out_shape=(H, W), transform=T, fill=0).astype(bool)
d = np.where(land, d, np.nan)
ds = generic_filter(d, np.nanmedian, size=3, mode='constant', cval=np.nan)
ds[~land] = np.nan
np.save('dndvi_land.npy', ds.astype('float32'))
v = ds[np.isfinite(ds)]
print('percentiles 5/25/50/75/95:', [round(float(np.percentile(v, q)), 3) for q in (5, 25, 50, 75, 95)])
