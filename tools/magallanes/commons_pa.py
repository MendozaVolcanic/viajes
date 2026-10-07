import json, urllib.request, urllib.parse, sys, time, re
sys.stdout.reconfigure(encoding='utf-8')
UA = {'User-Agent': 'viajes-nicolas/1.0 (personal trip map)'}
def q(params):
    url = 'https://commons.wikimedia.org/w/api.php?' + urllib.parse.urlencode(params)
    for i in range(5):
        try:
            return json.load(urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60))
        except urllib.error.HTTPError as e:
            if e.code == 429: time.sleep(10 * (i + 1)); continue
            raise
def parse(r):
    c = []
    for p in r.get('query', {}).get('pages', {}).values():
        if 'imageinfo' not in p: continue
        ii = p['imageinfo'][0]; m = ii.get('extmetadata', {})
        if not p['title'].lower().endswith(('.jpg', '.jpeg', '.png')): continue
        c.append(dict(t=p['title'], thumb=ii.get('thumburl'), page=ii['descriptionurl'], lic=m.get('LicenseShortName', {}).get('value', ''),
                      art=re.sub('<[^>]+>', '', m.get('Artist', {}).get('value', '')).strip(), desc=re.sub('<[^>]+>', '', m.get('ImageDescription', {}).get('value', ''))[:90]))
    return c
out = {}
for term in ['Nao Victoria Punta Arenas museo', 'Cerro de la Cruz Punta Arenas mirador', 'Cementerio Municipal Punta Arenas', 'Isla Magdalena pingüinos',
             'Museo Salesiano Maggiorino Borgatello', 'Fuerte Bulnes', 'Puerto Natales costanera', 'Cueva del Milodón', 'Villa Cerro Castillo Torres del Paine',
             'Laguna Amarga Torres del Paine', 'Lago Nordenskjöld Cuernos del Paine', 'Salto Grande Paine', 'Lago Pehoé', 'Lago Grey icebergs', 'Puerto Bories',
             'Río Serrano Torres del Paine']:
    c = parse(q({'action': 'query', 'format': 'json', 'generator': 'search', 'gsrsearch': term, 'gsrnamespace': '6', 'gsrlimit': '8',
                 'prop': 'imageinfo', 'iiprop': 'url|extmetadata', 'iiurlwidth': '640'}))
    out[term] = c; print('Q', term, len(c))
    for x in c[:6]: print('   ', x['t'][5:75], '|', x['lic'], '|', x['art'][:22], '|', x['desc'][:45])
    time.sleep(2)
json.dump(out, open('commons_pa.json', 'w', encoding='utf-8'), ensure_ascii=False)
