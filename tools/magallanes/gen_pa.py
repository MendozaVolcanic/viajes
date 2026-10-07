"""Página del viaje a Magallanes (diciembre 2026) con mapa SVG, rutas OSRM y fotos de Commons."""
import json, math, html, os, urllib.request, base64, sys, re
sys.stdout.reconfigure(encoding='utf-8')
UA = {'User-Agent': 'viajes-nicolas/1.0'}
LON0, LON1, LAT0, LAT1, RES = json.load(open('mar_meta.json'))['grid']
K = math.cos(math.radians(-52.2)); W = 1000
H = round(W * (LAT1 - LAT0) / ((LON1 - LON0) * K))
def P(lat, lon): return ((lon - LON0) / (LON1 - LON0) * W, (LAT1 - lat) / (LAT1 - LAT0) * H)
def dp(pts, eps):
    if len(pts) < 3: return pts
    (x1, y1), (x2, y2) = pts[0], pts[-1]; dx, dy = x2 - x1, y2 - y1; L = math.hypot(dx, dy) or 1e-9
    i, m = 0, -1
    for k in range(1, len(pts) - 1):
        x, y = pts[k]; d = abs(dy * x - dx * y + x2 * y1 - y2 * x1) / L
        if d > m: i, m = k, d
    if m > eps: return dp(pts[:i + 1], eps)[:-1] + dp(pts[i:], eps)
    return [pts[0], pts[-1]]
def path(pts, eps=0.6, close=False):
    xy = [P(a, b) for a, b in pts]
    if len(xy) > 3 and xy[0] == xy[-1]:
        k = max(range(len(xy)), key=lambda i: (xy[i][0] - xy[0][0]) ** 2 + (xy[i][1] - xy[0][1]) ** 2)
        q = dp(xy[:k + 1], eps)[:-1] + dp(xy[k:], eps)
    else:
        q = dp(xy, eps)
    return 'M' + ' L'.join(f'{x:.1f},{y:.1f}' for x, y in q) + (' Z' if close else '')
def stitch(segs):
    segs = [list(s) for s in segs if len(s) > 1]; rings = []
    while segs:
        c = segs.pop(0); ch = True
        while ch and c[0] != c[-1]:
            ch = False
            for i, s in enumerate(segs):
                if s[0] == c[-1]: c = c + s[1:]; segs.pop(i); ch = True; break
                if s[-1] == c[-1]: c = c + s[::-1][1:]; segs.pop(i); ch = True; break
                if s[-1] == c[0]: c = s + c[1:]; segs.pop(i); ch = True; break
                if s[0] == c[0]: c = s[::-1] + c[1:]; segs.pop(i); ch = True; break
        rings.append(c)
    return rings

S = {
 'puq': ('Aeropuerto de Punta Arenas', -53.0038, -70.8465),
 'nao': ('Museo Nao Victoria', -53.1075, -70.8795),
 'pla': ('Plaza de Armas de Punta Arenas', -53.1627, -70.9081),
 'cru': ('Mirador Cerro de la Cruz', -53.1599, -70.9153),
 'mue': ('Costanera y Muelle Prat', -53.1690, -70.9072),
 'tpu': ('Terminal Tres Puentes (Comapa)', -53.1192, -70.8752),
 'mag': ('Isla Magdalena, Monumento Natural Los Pingüinos', -52.9190, -70.5768),
 'cem': ('Cementerio Sara Braun', -53.1530, -70.8976),
 'bor': ('Museo Salesiano Maggiorino Borgatello', -53.1556, -70.9023),
 'nat': ('Puerto Natales', -51.7264, -72.5062),
 'bri': ('Puerto Bories', -51.6899, -72.5364),
 'cas': ('Villa Cerro Castillo', -51.2562, -72.3447),
 'ama': ('Portería Laguna Amarga', -50.9798, -72.8001),
 'nor': ('Mirador Nordenskjöld', -51.0412, -72.9096),
 'sal': ('Salto Grande', -51.0677, -73.0066),
 'peh': ('Mirador Lago Pehoé', -51.0957, -72.9838),
 'ser': ('Villa Río Serrano', -51.2335, -72.9681),
 'gre': ('Lago Grey', -51.1218, -73.1298),
 'mil': ('Cueva del Milodón', -51.5653, -72.6192),
 'bul': ('Fuerte Bulnes y Parque del Estrecho', -53.6303, -70.9172),
 'pud': ('Pudeto, muelle del catamarán', -51.0623, -72.9937),
 'zof': ('Zona Franca de Punta Arenas', -53.1336, -70.8760),
}
# (parada, minutos, texto, modo)  modo 'barco' = no se maneja
DAYS = [
 dict(id='d1', tag='Sáb 12', title='Llegada, Nao Victoria y Punta Arenas al atardecer', col='--d1', start='16:00',
  stops=[('puq', 45, 'El vuelo llega a las 16:00. Retiro del auto en el aeropuerto.', ''),
         ('nao', 60, 'Réplicas a escala real de la nao Victoria de Magallanes y de la goleta Ancud, al aire libre junto al estrecho. De 9:00 a 19:00 de septiembre a marzo. Queda de camino desde el aeropuerto.', ''),
         ('pla', 30, 'Check-in en el hotel. El centro es plano.', ''),
         ('cru', 30, 'Mirador sobre la ciudad y el estrecho de Magallanes, con estacionamiento al lado.', ''),
         ('mue', 60, "Costanera y muelle al atardecer, que en diciembre es cerca de las 22:00. Para comer, Sotito's (O'Higgins 1138) es el clásico de centolla y cordero.", '')]),
 dict(id='d2', tag='Dom 13', title='Pingüinos de Isla Magdalena y cementerio', col='--d2', start='08:30',
  stops=[('pla', 0, 'Salida del hotel.', ''),
         ('tpu', 30, 'Embarque en el ferry de Comapa, que sale todos los días. Confirma el horario de diciembre (una fuente dice 9:30, otra 10:30).', ''),
         ('mag', 300, 'Navegación de 1 h 45 por tramo y una hora en la isla, por un sendero de 1,4 km que CONAF da como fácil, con una subida al final hacia el faro. La colonia cayó a unas 7.000 parejas según CONAF (feb-2026), frente a 63.000 en 2008-09: se ven menos pingüinos que antes. Se pidió suspender el turismo, pero CONAF lo descartó y la Corte de Apelaciones rechazó el recurso en abril de 2026. Reserva con anticipación, porque hay cupos.', 'barco'),
         ('cem', 60, 'Uno de los cementerios más bonitos de Sudamérica: avenidas de cipreses recortados y mausoleos de las familias pioneras. Abre de 8:00 a 19:00. Es plano.', ''),
         ('zof', 90, 'Opcional para la tarde libre: tiendas techadas y planas, abiertas el domingo de 10:30 a 19:30. El Museo Borgatello no abre los domingos.', '')]),
 dict(id='d3', tag='Lun 14', title='A Puerto Natales por la ruta 9', col='--d3', start='10:00',
  stops=[('pla', 0, 'Salida por la ruta 9 al norte. Si Isla Magdalena no operó ayer, esta mañana va Fuerte Bulnes (1 h por tramo) y se sale a Natales después de almuerzo.', ''),
         ('nat', 60, 'Unas 3 horas de ruta pavimentada. En diciembre empiezan a florecer los lupinos a orillas del camino: si aparecen, vale una parada. Check-in y almuerzo.', ''),
         ('bri', 45, 'Antiguo frigorífico de 1915, a 5 km por la costanera, con vista al seno Última Esperanza.', ''),
         ('nat', 0, 'Costanera de Natales: cisnes de cuello negro, flamencos y cormoranes en la orilla. Noche en Natales.', '')]),
 dict(id='d4', tag='Mar 15', title='Día libre en Natales, o de reserva por el clima', col='--d4', start='09:00',
  stops=[('nat', 240, 'Este día está para usarlo según el pronóstico. Si el miércoles viene malo y hoy está despejado, hagan hoy el día del parque y corran todo un día. Si no, descansar y recorrer Natales con calma. Opcional y pagado: la navegación express a los glaciares Balmaceda y Serrano, de 6:40 a 13:30 desde el muelle de Natales ($120.000).', ''),
         ('nat', 0, 'Noche en Natales.', '')]),
 dict(id='d5', tag='Mié 16', title='Torres del Paine en auto: miradores', col='--d5', start='08:00',
  stops=[('nat', 0, 'Llena el estanque: dentro del parque no hay bencina.', ''),
         ('cas', 25, 'Café y baño en el pueblo, junto al paso a Argentina.', ''),
         ('ama', 30, 'Portería del parque. Los mayores de 60 entran gratis; el hermano paga $9.400 (adulto chileno, 2026). Compra en pasesparques.cl. Primera vista de las Torres sobre la laguna.', ''),
         ('nor', 30, 'Mirador sobre el lago Nordenskjöld y los Cuernos, con estacionamiento y caminata mínima.', ''),
         ('sal', 40, 'Cascada del río Paine. Una fuente dice 5 minutos a pie desde el estacionamiento y otra 1,5 km desde Pudeto.', ''),
         ('pud', 40, 'Sector Pudeto: mirador sobre el lago Pehoé con los Cuernos de frente, cafetería y baños. Opcional y pagado: el catamarán a Paine Grande, unas 2 horas ida y vuelta sin bajarse (la temporada pasada, $27.000 por tramo).', ''),
         ('peh', 25, 'Lago turquesa con el macizo del Paine al fondo, al lado del camino.', ''),
         ('ser', 0, 'Noche en Villa Río Serrano, fuera del parque. Reserva ya: en diciembre se llena.', '')]),
 dict(id='d6', tag='Jue 17', title='Playa del Lago Grey y Cueva del Milodón', col='--d6', start='09:00',
  stops=[('ser', 0, 'Salida por la Y-150.', ''),
         ('gre', 150, 'Caminata plana de 30 a 45 minutos por la playa del lago, entre témpanos varados, con el glaciar Grey al fondo; se cruza un puente colgante. Almuerzo en el Hotel Lago Grey, abierto a visitantes. Opcional y pagado: la navegación de 3 horas al frente del glaciar ($120.000 por adulto, 2026-27).', ''),
         ('mil', 60, 'Cueva enorme donde se hallaron restos del milodón, un perezoso gigante. De 8:00 a 18:30; los mayores de 60 entran gratis. Desde junio hay un tramo interior restringido por grietas.', ''),
         ('nat', 0, 'Noche en Natales.', '')]),
 dict(id='d7', tag='Vie 18', title='Natales al aeropuerto', col='--d7', start='07:45',
  stops=[('nat', 0, 'Salida temprano: el vuelo sale a las 13:00.', ''),
         ('puq', 0, 'Unas 3 horas de ruta: llegan cerca de las 10:45, con tiempo para devolver el auto y hacer el check-in antes del vuelo de las 13:00.', '')]),
]
IMG = {
 'nao': ('Museo Nao Victoria Punta Arenas Chile La réplica de la Goleta Ancud, vista ', 'Réplica de la goleta Ancud en el Museo Nao Victoria'),
 'cru': ('Cerro La Cruz PUQ.jpg', 'Punta Arenas desde el Cerro de la Cruz'),
 'mag': ('Chile, Isla Magdalena, colonia de pingüinos (5820722909).jpg', 'Pingüinos de Magallanes en Isla Magdalena'),
 'cem': ('Antiguas tumbas en el Cementerio Municipal de Punta Arenas 04.jpg', 'Cementerio Sara Braun'),
 'bor': ('Museo Salesiano Maggiorino Borgatello.jpg', 'Museo Borgatello'),
 'bri': ('Puerto Bories-CTJ-IMG 6771.jpg', 'Puerto Bories'),
 'nat': ('Flamencos en la costanera de Puerto Natales.jpg', 'Flamencos en la costanera de Puerto Natales'),
 'cas': ('Cerro Castillo Chile.jpg', 'Villa Cerro Castillo'),
 'ama': ('Laguna Amarga, Torres Del Paine, Chile (40227664191).jpg', 'Laguna Amarga'),
 'nor': ('Lago Nordenskjöld e os Cuernos - panoramio.jpg', 'Lago Nordenskjöld y los Cuernos'),
 'sal': ('Salto Grande, Torres Del Paine, Chile.JPG', 'Salto Grande'),
 'peh': ('Cuernos del Paine (Lago Pehoé) - panoramio.jpg', 'Lago Pehoé'),
 'ser': ('Torres del Paine, Río Serrano 3.jpg', 'El macizo del Paine desde Río Serrano'),
 'gre': ('Iceberg en Lago Grey.jpg', 'Témpano en el Lago Grey'),
 'pud': ('Amancer en Lago Pehoé (cropped).jpg', 'Lago Pehoé al amanecer'),
 'mil': ('Cueva del Milodón, Puerto Natales, Chile2.jpg', 'Cueva del Milodón'),
 'bul': ('Fuerte Bulnes 1.jpg', 'Fuerte Bulnes'),
}
KIND = {'puq': 'casa', 'pla': 'casa', 'nat': 'casa', 'ser': 'casa', 'mag': 'par', 'ama': 'par', 'nor': 'mir', 'sal': 'mir', 'peh': 'mir', 'cru': 'mir',
        'gre': 'mir', 'mue': 'mir', 'pud': 'mir', 'zof': 'flo', 'nao': 'geo', 'cem': 'geo', 'bor': 'geo', 'bri': 'geo', 'mil': 'geo', 'cas': 'flo', 'tpu': 'flo', 'bul': 'geo'}
SHORT = {'puq': ('Aeropuerto', 'r'), 'nao': ('Nao Victoria', 'r'), 'pla': ('Punta Arenas', 'r'), 'cru': ('Cerro de la Cruz', 'l'), 'mue': ('Muelle', 'l'),
         'tpu': ('Tres Puentes', 'r'), 'mag': ('Isla Magdalena', 'r'), 'cem': ('Cementerio', 'r'), 'bor': ('Museo Borgatello', 'l'), 'nat': ('Puerto Natales', 'r'),
         'bri': ('Puerto Bories', 'l'), 'cas': ('Cerro Castillo', 'r'), 'ama': ('Laguna Amarga', 'r'), 'nor': ('Nordenskjöld', 'r'), 'sal': ('Salto Grande', 'l'),
         'peh': ('Pehoé', 'r'), 'ser': ('Río Serrano', 'r'), 'gre': ('Lago Grey', 'l'), 'pud': ('Pudeto', 'l'), 'zof': ('Zona Franca', 'r'), 'mil': ('Cueva del Milodón', 'l'), 'bul': ('Fuerte Bulnes (opción)', 'r')}
CM = {}
for v in json.load(open('commons_pa.json', encoding='utf-8')).values():
    for x in v: CM[x['t'][5:]] = x
LICURL = {'CC BY 2.0': 'https://creativecommons.org/licenses/by/2.0/', 'CC BY 3.0': 'https://creativecommons.org/licenses/by/3.0/', 'CC BY 4.0': 'https://creativecommons.org/licenses/by/4.0/',
          'CC BY-SA 2.0': 'https://creativecommons.org/licenses/by-sa/2.0/', 'CC BY-SA 3.0': 'https://creativecommons.org/licenses/by-sa/3.0/', 'CC BY-SA 4.0': 'https://creativecommons.org/licenses/by-sa/4.0/',
          'CC0': 'https://creativecommons.org/publicdomain/zero/1.0/'}
def find(prefix):
    for t, x in CM.items():
        if t.startswith(prefix): return x
def one(t, cap):
    x = find(t)
    if not x or not x.get('thumb'): return ''
    art0 = html.unescape(x['art']).strip() or 'autor en Commons'
    if len(art0) > 70: art0 = art0[:70].rsplit(',', 1)[0] + ' y otros'
    lu = LICURL.get(x['lic']); lic = f'<a href="{lu}" target="_blank" rel="noopener">{html.escape(x["lic"])}</a>' if lu else html.escape(x['lic'])
    return (f'<figure class="ph"><img src="{x["thumb"]}" alt="{html.escape(cap)}" loading="lazy"><figcaption>{html.escape(cap)}. Foto: '
            f'<a href="{x["page"]}" target="_blank" rel="noopener">{html.escape(art0)}</a>, {lic}</figcaption></figure>')
SHOWN = set()
def fig(s):
    if s not in IMG or s in SHOWN: return ''
    SHOWN.add(s); b = one(*IMG[s]); return f'<div class="phs">{b}</div>' if b else ''

def osrm(dd):
    fn = f"osrm_{dd['id']}.json"
    if os.path.exists(fn): return json.load(open(fn))
    pts = [s for s, _, _, m in dd['stops'] if m != 'barco']
    co = ';'.join(f"{S[s][2]},{S[s][1]}" for s in pts)
    r = json.load(urllib.request.urlopen(urllib.request.Request(f"https://router.project-osrm.org/route/v1/driving/{co}?overview=full&geometries=geojson&steps=true", headers=UA), timeout=90))['routes'][0]
    json.dump(r, open(fn, 'w')); return r
def hm(t): h, m = map(int, t.split(':')); return h * 60 + m
def fmt(m): m = int(round(m / 5.0) * 5); return f"{(m // 60) % 24:02d}:{m % 60:02d}"

routes_svg = []; numbered = []; cards = []; summary = []
for dd in DAYS:
    r = osrm(dd); legs = r['legs']
    coords = [(la, lo) for lo, la in r['geometry']['coordinates']]
    routes_svg.append(f'<path class="route pav" data-day="{dd["id"]}" style="stroke:var({dd["col"]})" d="{path(coords, eps=0.5)}"/>')
    t = hm(dd['start']); rows = []; li = 0; tot_km = 0; drive = 0; prev = None
    for i, (s, dwell, txt, mode) in enumerate(dd['stops']):
        if mode == 'barco':
            a = P(S[prev][1], S[prev][2]); b = P(S[s][1], S[s][2])
            routes_svg.append(f'<path class="route boat" data-day="{dd["id"]}" style="stroke:var({dd["col"]})" d="M{a[0]:.1f},{a[1]:.1f} L{b[0]:.1f},{b[1]:.1f}"/>')
            rows.append(('leg', 'Navegación en el ferry, ida y vuelta incluida en el tiempo de la parada'))
            rows.append(('stop', s, fmt(t), txt)); t += dwell; continue
        if prev is not None:
            leg = legs[li]; li += 1; km = leg['distance'] / 1000; mins = leg['duration'] / 60
            refs = {}
            for st in leg['steps']:
                k = st.get('ref') or st.get('name') or ''
                if k: refs[k] = refs.get(k, 0) + st['distance']
            main = [k.split(';')[0] for k, v in sorted(refs.items(), key=lambda x: -x[1]) if v > 2000][:2]
            rows.append(('leg', f"{km:.0f} km · {mins:.0f} min" + (f" · por {' y '.join(main)}" if main else '')))
            t += mins; tot_km += km; drive += mins
        rows.append(('stop', s, fmt(t), txt)); t += dwell; prev = s
    end = fmt(t)
    lis = []
    for row in rows:
        if row[0] == 'leg': lis.append(f'<li class="leg"><span>{row[1]}</span></li>')
        else:
            _, s, tt, txt = row
            lis.append(f'<li class="st"><span class="t">{tt}</span><div><b>{html.escape(S[s][0])}</b><p>{html.escape(txt)}</p>{fig(s)}</div></li>')
    gm = 'https://www.google.com/maps/dir/' + '/'.join(f'{S[s][1]},{S[s][2]}' for s, _, _, m in dd['stops'] if m != 'barco')
    meta = f"Salida {dd['start']} · {tot_km:.0f} km · {drive / 60:.1f} h de manejo · termina cerca de las {end}"
    summary.append((dd['tag'], dd['title'], tot_km, drive, end))
    cards.append(f'<section class="day" id="{dd["id"]}" style="--c:var({dd["col"]})"><header><span class="chip">{dd["tag"]}</span><h2>{dd["title"]}</h2><p class="meta">{meta}</p></header><ol>{"".join(lis)}</ol><a class="gm" href="{gm}" target="_blank" rel="noopener">Abrir el día en Google Maps</a></section>')
    g = []; seen = set()
    for n, (s, _, _, _) in enumerate(dd['stops'], 1):
        x, y = P(S[s][1], S[s][2]); key = (round(x), round(y)); off = 14 if key in seen else 0; seen.add(key)
        g.append(f'<g transform="translate({x + off:.1f},{y:.1f})"><circle r="11"/><text y="4" text-anchor="middle">{n}</text><title>{html.escape(S[s][0])}</title></g>')
    numbered.append(f'<g class="num" data-day="{dd["id"]}" style="--c:var({dd["col"]})">{"".join(g)}</g>')
    print(dd['id'], f"{tot_km:.0f} km", f"{drive / 60:.1f} h", 'fin', end)

# capas base
mag = json.load(open('mag.json', encoding='utf-8'))['elements']
roads = []; lakes = []; parks = []
for e in mag:
    t = e['tags']
    if e['type'] == 'way' and t.get('highway') and e.get('geometry'):
        cls = 'r5' if t.get('highway') in ('trunk', 'primary') else 'rc'
        roads.append(f'<path class="{cls}" d="{path([(p["lat"], p["lon"]) for p in e["geometry"]], eps=0.8)}"/>')
    elif t.get('natural') == 'water':
        if e['type'] == 'way' and e.get('geometry'): rings = [[(p['lat'], p['lon']) for p in e['geometry']]]
        elif e['type'] == 'relation': rings = stitch([[(p['lat'], p['lon']) for p in m['geometry']] for m in e.get('members', []) if m.get('role') == 'outer' and m.get('geometry')])
        else: continue
        lakes.append(f'<path class="lake" d="{" ".join(path(r, eps=0.4, close=True) for r in rings if len(r) > 3)}"><title>{html.escape(t.get("name", "lago"))}</title></path>')
    elif e['type'] == 'relation' and t.get('name') == 'Parque Nacional Torres del Paine':
        rings = stitch([[(p['lat'], p['lon']) for p in m['geometry']] for m in e.get('members', []) if m.get('role', 'outer') in ('outer', '') and m.get('geometry')])
        parks.append(f'<path class="prot pn" d="{" ".join(path(r, eps=0.4, close=True) for r in rings if len(r) > 3)}"><title>Parque Nacional Torres del Paine</title></path>')
        x, y = P(-50.93, -73.12); parks.append(f'<text class="plab" x="{x:.1f}" y="{y:.1f}" text-anchor="middle">PN Torres del Paine</text>')
mar = base64.b64encode(open('mar.png', 'rb').read()).decode()
sea = (f'<defs><mask id="seamask"><image href="data:image/png;base64,{mar}" x="0" y="0" width="{W}" height="{H}" preserveAspectRatio="none"/></mask></defs>'
       f'<rect class="land-bg" width="{W}" height="{H}"/><rect class="sea-fill" width="{W}" height="{H}" mask="url(#seamask)"/>')
def shape(k):
    return {'mir': '<path d="M0,-11 L10,7 L-10,7 Z"/>', 'geo': '<path d="M0,-11 L10,0 L0,11 L-10,0 Z"/>', 'par': '<rect x="-9" y="-9" width="18" height="18" rx="3"/>',
            'casa': '<path d="M0,-11 L10,-2 L10,9 L-10,9 L-10,-2 Z"/>'}.get(k, '<circle r="9"/>')
base = []
used = {s for dd in DAYS for s, _, _, _ in dd['stops']} | {'bul'}
for s in used:
    name, la, lo = S[s]; x, y = P(la, lo); k = KIND.get(s, 'flo'); tx, side = SHORT[s]
    days = ' '.join(dd['id'] for dd in DAYS if any(a == s for a, _, _, _ in dd['stops']))
    text = f'<text x="{14 if side == "r" else -14}" y="5" text-anchor="{"start" if side == "r" else "end"}">{html.escape(tx)}</text>'
    base.append(f'<g class="mk k-{k}" data-days="{days}" transform="translate({x:.1f},{y:.1f})">{shape(k)}{text}<title>{html.escape(name)}</title></g>')
labs = []
for tx, la, lo in [('Estrecho de Magallanes', -53.35, -70.45), ('Seno Otway', -52.95, -71.45), ('Seno Skyring', -52.55, -72.05), ('Última Esperanza', -51.85, -72.75), ('Tierra del Fuego', -53.25, -70.05)]:
    x, y = P(la, lo); labs.append(f'<text class="sea" x="{x:.1f}" y="{y:.1f}" text-anchor="middle">{tx}</text>')
km_px = W / ((LON1 - LON0) * 111.32 * K); sx, sy = 40, H - 40
scale = (f'<g class="scale"><line x1="{sx}" y1="{sy}" x2="{sx + 50 * km_px:.1f}" y2="{sy}"/><line x1="{sx}" y1="{sy - 5}" x2="{sx}" y2="{sy + 5}"/>'
         f'<line x1="{sx + 50 * km_px:.1f}" y1="{sy - 5}" x2="{sx + 50 * km_px:.1f}" y2="{sy + 5}"/><text x="{sx}" y="{sy - 10}">50 km</text></g>')
svg = (f'<svg viewBox="0 0 {W} {H}" role="img" aria-label="Mapa del viaje por Magallanes: Punta Arenas, Puerto Natales y Torres del Paine">{sea}'
       f'<g>{"".join(lakes)}</g><g class="prots">{"".join(p for p in parks if p.startswith("<path"))}</g><g>{"".join(roads)}</g><g>{"".join(routes_svg)}</g>'
       f'<g>{"".join(p for p in parks if p.startswith("<text"))}</g><g>{"".join(labs)}</g><g>{"".join(base)}</g>{"".join(numbered)}{scale}</svg>')
sumrows = ''.join(f'<tr><td>{a}</td><td>{html.escape(b)}</td><td class="n">{c:.0f}</td><td class="n">{d / 60:.1f}</td><td class="n">{e}</td></tr>' for a, b, c, d, e in summary)
btns = ''.join(f'<button type="button" class="dbtn" data-day="{dd["id"]}" style="--c:var({dd["col"]})" aria-pressed="false">{dd["tag"]}</button>' for dd in DAYS)
extra = f'<section class="notes gal"><h2>Si Isla Magdalena no opera</h2><div class="grid-pc"><article class="pc">{one(*IMG["bul"])}<h3>Fuerte Bulnes y Parque del Estrecho</h3><p>Réplica del fuerte de 1843 en la punta sur del continente, con miradores sobre el estrecho. 57 km al sur de Punta Arenas, una hora por tramo.</p><p class="hor">Horario y precio no confirmados: las fuentes dan cierre entre 17:30 y 19:00, y precios entre $10.000 y $12.000, o USD 22.</p><p class="ln"><a href="https://parquedelestrecho.cl" target="_blank" rel="noopener">parquedelestrecho.cl</a></p></article></div></section>'
tpl = open('tpl_pa.html', encoding='utf-8').read()
out = tpl.replace('%%SVG%%', svg).replace('%%DAYS%%', '\n'.join(cards)).replace('%%BTNS%%', btns).replace('%%SUM%%', sumrows).replace('%%EXTRA%%', extra)
open('magallanes-2026.html', 'w', encoding='utf-8').write('<!DOCTYPE html>\n<html lang="es-CL">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">\n' + out + '\n</html>\n')
print('bytes', len(out), 'H', H)
