import numpy as np
from PIL import Image
ds = np.load('dndvi_land.npy')
H, W = ds.shape
rgba = np.zeros((H, W, 4), 'uint8')
for t, c in [(0.20, (46, 140, 70, 70)), (0.30, (36, 125, 60, 125)), (0.45, (20, 100, 45, 185))]:
    rgba[ds > t] = c
Image.fromarray(rgba, 'RGBA').save('verde.png', optimize=True)
res = 0.0015
for t in (0.20, 0.30, 0.45):
    print(t, round(float(np.nansum(ds > t)) * (res * 111.32) ** 2 * 0.885), 'km2')
