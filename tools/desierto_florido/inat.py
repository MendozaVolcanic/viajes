"""Observaciones de plantas en iNaturalist en la zona del viaje, temporada 2026."""
import json, urllib.request, urllib.parse, time, sys
sys.stdout.reconfigure(encoding='utf-8')
UA = {'User-Agent': 'viajes-nicolas/1.0 (personal trip guide)'}
base = 'https://api.inaturalist.org/v1/observations'
params = dict(swlat=-28.75, swlng=-71.40, nelat=-26.85, nelng=-70.30, iconic_taxa='Plantae', d1='2026-08-15', d2='2026-10-08',
              per_page=200, order_by='id', order='asc', locale='es', geo='true')
obs = []; id_above = 0
while True:
    q = dict(params, id_above=id_above)
    r = json.load(urllib.request.urlopen(urllib.request.Request(base + '?' + urllib.parse.urlencode(q), headers=UA), timeout=60))
    res = r['results']
    if not res: break
    for o in res:
        t = o.get('taxon') or {}
        if not o.get('geojson'): continue
        lo, la = o['geojson']['coordinates']
        ph = (o.get('photos') or [{}])[0]
        obs.append(dict(id=o['id'], date=o.get('observed_on'), lat=la, lon=lo, taxon=t.get('name'), rank=t.get('rank'), tid=t.get('id'),
                        common=t.get('preferred_common_name'), iconic=t.get('iconic_taxon_name'), user=(o.get('user') or {}).get('login'),
                        ph_url=ph.get('url'), ph_lic=ph.get('license_code'), ph_attr=ph.get('attribution'), qg=o.get('quality_grade'),
                        place=o.get('place_guess')))
    id_above = res[-1]['id']
    print('lote', len(res), 'total', len(obs), flush=True)
    time.sleep(1.2)
    if len(res) < 200: break
json.dump(obs, open('inat_obs.json', 'w', encoding='utf-8'), ensure_ascii=False)
from collections import Counter
c = Counter((o['taxon'], o['common']) for o in obs if o['rank'] in ('species', 'subspecies', 'variety'))
print('observaciones', len(obs), 'usuarios', len({o['user'] for o in obs}), 'especies', len(c))
for (t, cm), n in c.most_common(45): print(f'{n:4d}  {t}  ({cm})')
