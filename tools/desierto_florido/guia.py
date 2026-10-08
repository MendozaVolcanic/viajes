"""Guía de flores para ir marcando y capa de observaciones, desde iNaturalist (temporada 2026).
Se importa desde gen2.py: build(S, used, P, route_pts) devuelve (html_guia, svg_puntos, html_hotspots)."""
import json, math, html
from collections import defaultdict, Counter

GENUS_ES = {'Leucocoryne': 'huilli', 'Nolana': 'suspiro', 'Zephyra': 'azulillo', 'Zephyranthes': 'añañuca', 'Rhodophiala': 'añañuca',
            'Alstroemeria': 'lirio del campo', 'Schizanthus': 'mariposita', 'Copiapoa': 'copiapoa (cactus)', 'Eriosyce': 'quisco chico (cactus)',
            'Heliotropium': 'heliotropo', 'Cristaria': 'malvilla', 'Oenothera': 'don diego de la noche', 'Viola': 'violeta', 'Calandrinia': 'pata de guanaco',
            'Cistanthe': 'pata de guanaco', 'Bomarea': 'garra de león', 'Encelia': 'coronilla de fraile', 'Argylia': 'terciopelo'}
LICOK = ('cc0', 'cc-by', 'cc-by-sa', 'cc-by-nc', 'cc-by-nc-sa', 'cc-by-nd', 'cc-by-nc-nd')
LICURL = {'cc0': 'https://creativecommons.org/publicdomain/zero/1.0/', 'cc-by': 'https://creativecommons.org/licenses/by/4.0/',
          'cc-by-sa': 'https://creativecommons.org/licenses/by-sa/4.0/', 'cc-by-nc': 'https://creativecommons.org/licenses/by-nc/4.0/',
          'cc-by-nc-sa': 'https://creativecommons.org/licenses/by-nc-sa/4.0/', 'cc-by-nd': 'https://creativecommons.org/licenses/by-nd/4.0/',
          'cc-by-nc-nd': 'https://creativecommons.org/licenses/by-nc-nd/4.0/'}
BBOX = 'swlat=-28.75&swlng=-71.40&nelat=-26.85&nelng=-70.30&d1=2026-08-15'

def km(a, b, c, d): return math.hypot((a - c) * 111, (b - d) * 111 * 0.885)

def build(S, used, P, route_pts, n_species=40):
    obs = json.load(open('inat_obs.json', encoding='utf-8'))
    stops = [(s, S[s][0], S[s][1], S[s][2]) for s in used if S[s][1] > -29]
    def near(la, lo):
        d, s = min((km(la, lo, a, b), n) for _, n, a, b in stops)
        return s if d <= 12 else None
    def droute(la, lo): return min(km(la, lo, a, b) for a, b in route_pts)
    sp = defaultdict(list)
    for o in obs:
        if o['rank'] in ('species', 'subspecies', 'variety') and o['taxon']:
            sp[o['taxon'].split(' ')[0] + ' ' + o['taxon'].split(' ')[1]].append(o)
    top = sorted(sp.items(), key=lambda kv: -len(kv[1]))[:n_species]
    cards = []
    for name, lst in top:
        genus = name.split(' ')[0]
        common = next((o['common'] for o in lst if o['common']), None) or GENUS_ES.get(genus)
        tid = lst[0]['tid']
        places = Counter()
        for o in lst:
            n = near(o['lat'], o['lon'])
            places[n or ((o['place'] or '').split(',')[0] or 'otro lugar')] += 1
        dmin = min(droute(o['lat'], o['lon']) for o in lst)
        last = max(o['date'] for o in lst if o['date'])
        ph = sorted([o for o in lst if o.get('ph_url') and o.get('ph_lic') in LICOK], key=lambda o: LICOK.index(o['ph_lic']))
        img = ''
        if ph:
            o = ph[0]; url = o['ph_url'].replace('/square.', '/medium.')
            attr = html.escape((o.get('ph_attr') or '').replace('(c) ', '').split(',')[0])
            img = (f'<figure class="ph"><img src="{url}" alt="{html.escape(name)}" loading="lazy"><figcaption>Foto: '
                   f'<a href="https://www.inaturalist.org/observations/{o["id"]}" target="_blank" rel="noopener">{attr}</a>, '
                   f'<a href="{LICURL[o["ph_lic"]]}" target="_blank" rel="noopener">{o["ph_lic"].upper()}</a>, vía iNaturalist</figcaption></figure>')
        where = ', '.join(f'{html.escape(p)} ({n})' for p, n in places.most_common(3))
        ruta = 'junto a tu ruta' if dmin < 1.5 else f'a {dmin:.0f} km de tu ruta'
        title = f'{html.escape(common.capitalize())} <i>{html.escape(name)}</i>' if common else f'<i>{html.escape(name)}</i>'
        cards.append(f'<article class="sp" data-t="{tid}"><label class="chk"><input type="checkbox" data-k="{tid}"> <span>Vista</span></label>'
                     f'{img}<h3>{title}</h3><p>{len(lst)} registros este año, el último el {last[8:10]}-{last[5:7]}. Más vista en: {where}. El registro más cercano está {ruta}.</p>'
                     f'<p class="ln"><button type="button" class="see" data-t="{tid}">Ver en el mapa</button> · '
                     f'<a href="https://www.inaturalist.org/observations?taxon_id={tid}&{BBOX}" target="_blank" rel="noopener">registros en iNaturalist</a></p></article>')
    # puntos para el mapa
    pts = []
    for o in obs:
        x, y = P(o['lat'], o['lon'])
        pts.append(f'<circle class="obs" data-t="{o["tid"] or 0}" cx="{x:.1f}" cy="{y:.1f}" r="2.6"/>')
    svg_pts = '<g class="obsl">' + ''.join(pts) + '</g>'
    # dónde se juntó la gente
    g = defaultdict(list)
    for o in obs: g[(round(o['lat'] / 0.04), round(o['lon'] / 0.04))].append(o)
    rows = []
    for c in sorted(g.values(), key=len, reverse=True)[:12]:
        la = sum(o['lat'] for o in c) / len(c); lo = sum(o['lon'] for o in c) / len(c)
        d = droute(la, lo); n = near(la, lo)
        estado = 'en tu ruta' if d < 1.5 else f'a {d:.0f} km de tu ruta'
        rows.append(f'<tr><td>{html.escape(n or (c[0]["place"] or "").split(",")[0])}</td><td class="n">{len(c)}</td><td class="n">{len({o["user"] for o in c})}</td>'
                    f'<td class="n">{len({o["taxon"] for o in c})}</td><td>{estado}</td>'
                    f'<td><a href="https://www.google.com/maps/search/?api=1&query={la:.4f},{lo:.4f}" target="_blank" rel="noopener">{la:.3f}, {lo:.3f}</a></td></tr>')
    total = len(obs); users = len({o['user'] for o in obs}); nsp = len(sp)
    hot = ('<section class="notes gal"><h2>Dónde se detuvo la gente a fotografiar flores</h2>'
           f'<p class="hint" style="margin:0 0 10px">{total} registros de plantas que subieron {users} personas a iNaturalist entre el 15 de agosto y el 8 de octubre de 2026, de {nsp} especies. '
           'Cada fila agrupa los registros en celdas de unos 4 km; el nombre es la parada del plan más cercana (hasta 12 km).</p>'
           '<div class="tw"><table class="sum"><thead><tr><th>Sector</th><th class="n">Registros</th><th class="n">Personas</th><th class="n">Especies</th><th>Respecto del plan</th><th>Ubicación</th></tr></thead>'
           f'<tbody>{"".join(rows)}</tbody></table></div></section>')
    guia = ('<section class="notes gal" id="guia"><h2>Guía de flores para ir marcando</h2>'
            f'<p class="hint" style="margin:0 0 10px">Las {len(top)} especies con más registros este año en la zona, según iNaturalist. Marca las que vayas viendo: '
            'queda guardado en este celular. «Ver en el mapa» destaca dónde se registró cada una. <b id="cnt">0</b> vistas de ' + str(len(top)) + '.</p>'
            f'<div class="grid-sp">{"".join(cards)}</div></section>')
    return guia, svg_pts, hot
