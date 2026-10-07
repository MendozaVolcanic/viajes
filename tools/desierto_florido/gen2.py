import json, math, html, os, urllib.request, urllib.parse, sys, time
sys.stdout.reconfigure(encoding='utf-8')
UA={'User-Agent':'viajes-nicolas/1.0'}
d=json.load(open('osm.json',encoding='utf-8'))['elements']
chains=json.load(open('coast_chains.json'))
LAT0,LAT1,LON0,LON1=-28.72,-26.84,-71.36,-70.36
K=math.cos(math.radians(-27.8)); W=1000
H=round(W*(LAT1-LAT0)/((LON1-LON0)*K))
def P(lat,lon): return ((lon-LON0)/(LON1-LON0)*W, (LAT1-lat)/(LAT1-LAT0)*H)
def dp(pts,eps):
    if len(pts)<3: return pts
    (x1,y1),(x2,y2)=pts[0],pts[-1]; dx,dy=x2-x1,y2-y1; L=math.hypot(dx,dy) or 1e-9
    i,m=0,-1
    for k in range(1,len(pts)-1):
        x,y=pts[k]; dd=abs(dy*x-dx*y+x2*y1-y2*x1)/L
        if dd>m: i,m=k,dd
    if m>eps: return dp(pts[:i+1],eps)[:-1]+dp(pts[i:],eps)
    return [pts[0],pts[-1]]
def path(pts,eps=0.6,close=False):
    xy=[P(a,b) for a,b in pts]
    if len(xy)>3 and xy[0]==xy[-1]:
        k=max(range(len(xy)),key=lambda i:(xy[i][0]-xy[0][0])**2+(xy[i][1]-xy[0][1])**2)
        q=dp(xy[:k+1],eps)[:-1]+dp(xy[k:],eps)
    else:
        q=dp(xy,eps)
    return 'M'+' L'.join(f'{x:.1f},{y:.1f}' for x,y in q)+(' Z' if close else '')
def hav(a,b):
    R=6371.0; la1,lo1,la2,lo2=map(math.radians,(a[0],a[1],b[0],b[1]))
    h=math.sin((la2-la1)/2)**2+math.cos(la1)*math.cos(la2)*math.sin((lo2-lo1)/2)**2
    return 2*R*math.asin(math.sqrt(h))

S={
 'ls':('La Serena',-29.904,-71.252),
 'val':('Vallenar',-28.575,-70.762),
 'paj':('Ruta 5 en Pajaritos, junto al peaje Totoral',-27.9712,-70.5578),
 'bi':('Cabaña en Bahía Inglesa',-27.102,-70.856),
 'cho':('Mirador Aguada de Chorrillos y Salto del Gato',-27.2123,-70.9504),
 'mbc':('Mirador Bahía Cisne',-27.2347,-70.9437),
 'pir':('Pirámides y Casa de Sal',-27.2714,-70.9087),
 'est':('Mirador del estuario del río Copiapó',-27.3117,-70.9277),
 'bar':('Barranquilla',-27.515,-70.892),
 'bs':('Bahía Salada',-27.643,-70.916),
 'ct':('Caleta Totoral',-27.830,-71.090),
 'cb':('Carrizal Bajo, humedal y miradores',-28.0850,-71.1430),
 'pb':('Llanos de Challe: Playa Blanca y sendero Centenario',-28.181,-71.162),
 'lag':('Llano El Lagarto',-28.157,-70.862),
 'pdf':('Parque Nacional Desierto Florido',-27.566,-70.581),
 'hc':('Hacienda Castilla',-27.904,-70.679),
 'tot':('Oasis de Totoral',-27.902,-70.960),
 'ton':('Santuario Granito Orbicular',-26.9724,-70.7956),
 'pc':('Pampa Caracoles',-27.0127,-70.6549),
 'lvi':('Playa La Virgen',-27.3597,-70.9555),
 'fc':('Costa de Freirina por la C-480',-28.604,-71.204),
 'ded':('Parque Paleontológico Los Dedos',-27.1526,-70.8862),
 'msj':('Mina San José, memorial de los 33',-27.1568,-70.4984),
 'mra':('Museo Regional de Atacama',-27.3625,-70.3421),
 'dun':('Dunas del cerro Bramador',-27.3167,-70.4200),
 'mus':('Museo Paleontológico de Caldera',-27.0649,-70.8234),
 'clb':('Caleta Los Bronces',-28.6561,-71.2887),
 'fre':('Freirina',-28.509,-71.079),
 'toy':('Los Toyos, costa de Huasco',-28.382,-71.182),
 'mhu':('Mirador Huasco',-28.4607,-71.2238),
}
# (stop, minutes spent there, text)
DAYS=[
 dict(id='vie',tag='Viernes 9',title='La Serena a Bahía Inglesa',col='--d1',start='14:00',
  stops=[('ls',0,'Salida por la ruta 5 al norte.'),
         ('val',20,'Bencina. Entre Vallenar y el cruce a Llanos de Challe el satélite marca algunos de los llanos más verdes de la zona, a los dos lados de la ruta 5: si ves un manto, para en una berma ancha.'),
         ('bi',0,'Llegada a la cabaña, ya de noche.')]),
 dict(id='sab',tag='Sábado 10',title='SUP, mina San José, dunas, parque nacional y fósiles',col='--d2',start='07:30',
  stops=[('bi',60,'SUP en Bahía Inglesa a primera hora, cuando el agua está quieta y todavía no sube el viento.'),
         ('ton',30,'Santuario de la Naturaleza Granito Orbicular, 11 km al norte de Caldera por la C-316: orbículos de unos 7 cm de hornblenda, ortoclasa, biotita y cuarzo. Al aire libre, sin horario.'),
         ('ded',50,'Formación Bahía Inglesa al aire libre: perezosos marinos, tiburones y aves gigantes como Pelagornis. Abre de martes a domingo; las fuentes dan cierre entre 17:30 y 18:00, así que mejor en la mañana, apenas abre.'),
         ('msj',60,'Memorial del rescate de los 33: banderas, monumento y salas con fotos y videos. Abre de jueves a domingo, cerca de 10:00 a 17:00 según operadores; confírmalo. El camino cruza un mar de dunas. La cápsula Fénix no está aquí: está en el Museo Regional de Copiapó.'),
         ('dun',40,'Dunas del cerro Bramador, frente a Copiapó. Con la 4x4 llega solo hasta donde el camino es firme: en la arena suelta se entierra cualquiera.'),
         ('mra',45,'Museo Regional de Atacama, reabierto en enero de 2026: aquí está la cápsula Fénix 2 del rescate de los 33. Los sábados abría de 10:00 a 17:30 en mayo; confirma el horario de octubre.'),
         ('pdf',90,'Parque nacional por la C-382, abierto de martes a domingo de 9:00 a 18:00, sin baños ni senderos habilitados: lleva agua. Llegas cuando las flores ya abrieron. Pregunta aquí por Hacienda Castilla, el sector más fotografiado según Andeshandbook: una fuente lo pone en el km 18 de esta misma C-382. La hacienda que marca OpenStreetMap queda 130 km al sur y no la incluí.'),
         ('cho',60,'Atardecer en el Mirador Aguada de Chorrillos y el Salto del Gato. El sol se pone cerca de las 19:47 y hay luz hasta las 20:10.'),
         ('bi',0,'Cabaña.')]),
 dict(id='dom',tag='Domingo 11',title='Quebrada Totoral y Llanos de Challe',col='--d3',start='08:00',
  stops=[('bi',0,'Salida por la ruta 5 al sur.'),
         ('paj',15,'Ruta 5 en Pajaritos, sector oficial de Sernatur, junto al peaje Totoral. Aquí nace la C-416, que Vialidad no nombra entre las rutas habilitadas: pregunta en la posada si está transitable.'),
         ('tot',35,'Bajas por la C-416, que recorre la Quebrada Totoral hasta el mar. Sector oficial. Si la C-416 está cortada, vuelve a la ruta 5 y entra a la costa por la C-370 en Barranquilla.'),
         ('ct',25,'Desembocadura de la quebrada: las praderas llegan casi al mar. Zona de garra de león.'),
         ('cb',45,'Almuerzo. Dos miradores sobre la bahía y el humedal. El 30 de septiembre ya había mantos de flores aquí.'),
         ('pb',150,'Parque nacional, cerrado los lunes. Camina el sendero Centenario hasta el mirador sobre Playa Blanca. Compra la entrada ya en pasesparques.cl (el portal de CONAF desde 2024): abre de martes a domingo de 9:00 a 18:00 y es fin de semana largo. Su administrador dijo que el peak partía el 3 y 4 de octubre.'),
         ('lag',30,'Sales al interior por el camino a Carrizal Bajo (C-440) y cruzas los llanos con luz de tarde. Según el satélite, aquí está el foco más verde de toda la zona. El punto queda fuera del parque, en el cruce con la C-432, ambas pavimentadas según OpenStreetMap.'),
         ('bi',0,'Vuelta de noche por la C-432 y la ruta 5, pavimentadas. Sales con el estanque lleno desde Copiapó: entre Copiapó y la vuelta a la ruta 5 no encontré bencinera.')]),
 dict(id='lun',tag='Lunes 12',title='Costa hasta Huasco, costa de Freirina y vuelta',col='--d4',start='08:00',
  stops=[('bi',0,'Salida por la C-302 al sur, por la costa.'),
         ('est',10,'Mirador sobre la desembocadura del río Copiapó.'),
         ('bar',10,'Llanos costeros por la C-10.'),
         ('bs',15,'Andeshandbook recomienda los llanos interiores entre Caldera y Bahía Salada.'),
         ('toy',20,'Costa de Huasco, punto oficial de información.'),
         ('mhu',45,'Mirador sobre el puerto y almuerzo en Huasco.'),
         ('fc',45,'La C-480 baja por la costa de Freirina, una de las zonas que más reverdeció según el satélite, y Vialidad la dio por habilitada. Sector oficial de Sernatur.'),
         ('clb',20,'Caleta Los Bronces, fin de la costa. De aquí vuelves por la C-480 y la C-46 a Vallenar.'),
         ('ls',0,'Llegada a La Serena. El vuelo es el martes 13.')]),
]

IMGS=os.environ.get('IMGS')=='1'
CM={}
if IMGS:
    for v in json.load(open('commons.json',encoding='utf-8')).values():
        for x in v: CM[x['t'][5:]]=x
IMG={'cho':[('Valeriana integrifolia Phil. - Flickr - Pato Novoa.jpg','Acantilados de Chorrillos')],
 'mbc':[('Desierto florido 2015 (22109458955).jpg','Desierto florido de 2015 cerca de Bahía Inglesa')],
 'bi':[('Bahia Inglesa.JPG','Bahía Inglesa')],
 'est':[('Puerto Viejo 2016.JPG','Puerto Viejo, febrero de 2016')],
 'bar':[('Desierto florido 2010.jpg','Desierto florido de 2010 en Barranquilla')],
 'ct':[('GARRA DE LEÓN, PARQUE NACIONAL LLANOS DE CHALLE - panoramio.jpg','Garra de león en Llanos de Challe')],
 'cb':[('CARRIZAL BAJO - HUMEDAL - panoramio.jpg','Humedal de Carrizal Bajo')],
 'pb':[('Desierto Florido Llanos de Challe.jpg','Desierto florido en Llanos de Challe'),('Pata de Guanaco Parque Nacional Llanos de Challe 16.jpg','Pata de guanaco en Llanos de Challe')],
 'lag':[('Guanacos Parque Nacional Llanos de Challe 23.jpg','Guanacos en Llanos de Challe')],
 'tot':[('Eriosyce crispa totoralensis.jpg','Eriosyce crispa totoralensis, cactus que lleva el nombre de Totoral')],
 'pdf':[('Desierto florido.jpg','Desierto florido en Atacama, de otro año')],
 'ton':[('Granito Orbicular.jpg','Afloramiento del Santuario de la Naturaleza Granito Orbicular')],
 'mus':[('Fosiles interior Museo Paleontologico.jpg','Fósiles en el Museo Paleontológico de Caldera'),('Balaenopterid specimens (Cerro Ballena).png','Ballenas fósiles en el yacimiento de Cerro Ballena')],
 'ded':[('Parque Los Dedos (1).png','Senderos del Parque Paleontológico Los Dedos')],
 'toy':[('CARRETERA COSTERA HUASCO CALDERA III REGION CHILE - panoramio.jpg','La costera C-10 cerca de Huasco')],
 'mhu':[('Faro De Huasco, Región de Atacama, Chile - panoramio.jpg','Faro de Huasco')],
 'fc':[('Zephyra elegans Desierto Florido 2011 costa de Huasco 01.jpg','Zephyra elegans en la costa de Huasco, desierto florido de 2011')],
 'fre':[('Freirina, Chile - panoramio.jpg','Freirina')],
 'msj':[('Mina San José de Copiapó en 2010.jpg','Mina San José en 2010')]}
SHOWN=set()
LICURL={'CC BY 2.0':'https://creativecommons.org/licenses/by/2.0/','CC BY 3.0':'https://creativecommons.org/licenses/by/3.0/','CC BY 4.0':'https://creativecommons.org/licenses/by/4.0/',
 'CC BY-SA 2.0':'https://creativecommons.org/licenses/by-sa/2.0/','CC BY-SA 3.0':'https://creativecommons.org/licenses/by-sa/3.0/','CC BY-SA 4.0':'https://creativecommons.org/licenses/by-sa/4.0/',
 'CC0':'https://creativecommons.org/publicdomain/zero/1.0/'}
def one(t,cap):
    x=CM.get(t)
    if not x or not x.get('thumb'): return ''
    art0=html.unescape(x['art']).strip() or 'autor en Commons'
    if len(art0)>70:
        art0=art0[:70].rsplit(',',1)[0].rsplit(';',1)[0]+' y otros'
    art=html.escape(art0)
    lic=x['lic']; lu=LICURL.get(lic)
    licH=f'<a href="{lu}" target="_blank" rel="noopener">{html.escape(lic)}</a>' if lu else html.escape(lic)
    return (f'<figure class="ph"><img src="{x["thumb"]}" alt="{html.escape(cap)}" loading="lazy">'
            f'<figcaption>{html.escape(cap)}. Foto: <a href="{x["page"]}" target="_blank" rel="noopener">{art}</a>, {licH}</figcaption></figure>')
def fig(s):
    if not IMGS or s not in IMG or s in SHOWN: return ''
    SHOWN.add(s)
    body=''.join(one(t,c) for t,c in IMG[s])
    return f'<div class="phs">{body}</div>' if body else ''
FLORES=[('Zephyranthes (Rhodophiala) bagnoldii (Herb.) Nic.García.jpg','Añañuca amarilla (Zephyranthes bagnoldii)'),
 ('Pata de Guanaco Parque Nacional Llanos de Challe 16.jpg','Pata de guanaco'),
 ('Garra de León Bomarea ovallei.jpg','Garra de león (Bomarea ovallei), en peligro'),
 ('Nolana paradoxa kz02.jpg','Suspiro de mar (Nolana paradoxa)'),
 ('Zephyra elegans Desierto Florido 2011 Costa de Huasco 05.jpg','Azulillo (Zephyra elegans), costa de Huasco'),
 ('Alstroemeria kingii (8383813801).jpg','Lirio amarillo (Alstroemeria kingii)')]
def flores_html():
    if not IMGS: return ''
    cards=''.join(one(t,c) for t,c in FLORES)
    return ('<section class="notes gal"><h2>Flores que puedes encontrar</h2><p class="hint" style="margin:0 0 10px">Fotos de otros años y lugares, '
            'para reconocerlas en terreno. Añañucas y huilles se ven desde fines de agosto; la garra de león, hasta fines de noviembre.</p>'
            f'<div class="grid-ph">{cards}</div></section>')
PALEO=[('Museo Paleontológico de Caldera (cerrado)','Fosiles interior Museo Paleontologico.jpg',
  'Primer museo paleontológico de Chile, con fósiles de la Formación Bahía Inglesa y de Cerro Ballena. El Registro de Museos de Chile lo da temporalmente cerrado por riesgo de derrumbe, con traslado de colecciones a un edificio nuevo previsto para mayo de 2026, y no encontré aviso de reapertura. Por eso salió del plan; llama antes si te interesa.',
  'Cerrado según el Registro de Museos de Chile (consultado el 7 de octubre).',
  [('Wikipedia','https://es.wikipedia.org/wiki/Museo_Paleontol%C3%B3gico_de_Caldera'),('Registro de Museos de Chile','https://www.registromuseoschile.cl/663/w3-article-50701.html')]),
 ('Parque Paleontológico Los Dedos','Parque Los Dedos (1).png',
  'Afloramiento al aire libre de la Formación Bahía Inglesa, entre Caldera y Bahía Inglesa, con senderos interpretativos: perezosos marinos (Thalassocnus), tiburones y aves gigantes como Pelagornis.',
  'Martes a domingo desde las 10:00; las fuentes dan cierre entre 17:30 y 18:00.',
  [('Chile Travel','https://chile.travel/en/attractions/los-dedos-paleontological-park/'),('Wikipedia','https://en.wikipedia.org/wiki/Los_Dedos_Paleontological_Park'),('Formación Bahía Inglesa','https://en.wikipedia.org/wiki/Bah%C3%ADa_Inglesa_Formation')]),
 ('Cerro Ballena','Balaenopterid specimens (Cerro Ballena).png',
  'Más de 40 esqueletos de cetáceos del Mioceno tardío (entre 6 y 9 millones de años según la nota de prensa del estudio), en cuatro niveles de varamiento masivo. El paper de Pyenson y colegas (2014) lo atribuye a floraciones de algas tóxicas que mataron a los animales en el mar. El yacimiento está junto a la ruta 5, al norte de Caldera.',
  'No es un sitio abierto a visitas, y el museo que guarda sus fósiles está cerrado.',
  [('Wikipedia','https://es.wikipedia.org/wiki/Cerro_Ballena'),('Paper, Proc. R. Soc. B 2014','https://doi.org/10.1098/rspb.2013.3316')]),
 ('Santuario de la Naturaleza Granito Orbicular','Granito Orbicular.jpg',
  'Santuario costero de 2 hectáreas, 11 km al norte de Caldera por la C-316. Orbículos de unos 7 cm de hornblenda, ortoclasa, biotita y cuarzo. Santuario desde 1981.',
  'Al aire libre, sin horario.',
  [('SIMBIO, Ministerio del Medio Ambiente','https://simbio.mma.gob.cl/CbaAP/Details/1055')])]
def paleo_html():
    cards=[]
    for nm,ph,txt,hor,links in PALEO:
        im=one(ph,nm) if IMGS else ''
        ln=' · '.join(f'<a href="{u}" target="_blank" rel="noopener">{html.escape(t)}</a>' for t,u in links)
        cards.append(f'<article class="pc">{im}<h3>{html.escape(nm)}</h3><p>{html.escape(txt)}</p><p class="hor">{html.escape(hor)}</p><p class="ln">{ln}</p></article>')
    return ('<section class="notes gal"><h2>Geología y paleontología: para decidir</h2><p class="hint" style="margin:0 0 10px">Granito Orbicular y Los Dedos están en el plan del sábado; el museo de Caldera está cerrado. '
            'Si alguno no te convence, se saca sin mover el resto.</p>' f'<div class="grid-pc">{"".join(cards)}</div></section>')

PAVED={'asphalt','paved','concrete','chipseal','concrete:plates','paving_stones','sett','cobblestone'}
RIPIO={'gravel','unpaved','dirt','compacted','fine_gravel','ground','sand','salt','earth','pebblestone','rock','mud'}

def osrm(dd):
    fn=f"osrm_{dd['id']}.json"
    if os.path.exists(fn): return json.load(open(fn))
    co=';'.join(f"{S[s][2]},{S[s][1]}" for s,_,_ in dd['stops'])
    url=f"https://router.project-osrm.org/route/v1/driving/{co}?overview=full&geometries=geojson&steps=true"
    r=json.load(urllib.request.urlopen(urllib.request.Request(url,headers=UA),timeout=90))['routes'][0]
    json.dump(r,open(fn,'w')); time.sleep(1); return r

HW=None; GRID={}
def surfaces(dd,coords):
    global HW
    if HW is None:
        HW=[]
        for w in json.load(open('hw.json',encoding='utf-8'))['elements']:
            t=w['tags']; g=[(p['lat'],p['lon']) for p in w['geometry']]
            idx=len(HW); HW.append(dict(s=t.get('surface',''),hw=t.get('highway',''),ref=t.get('ref') or t.get('name','')))
            for i in range(len(g)-1):
                for p in (g[i],g[i+1],((g[i][0]+g[i+1][0])/2,(g[i][1]+g[i+1][1])/2)):
                    GRID.setdefault((int(p[0]*200),int(p[1]*200)),[]).append((p,idx))
    return HW
def classify(pt,ways):
    best,bd=None,1e9
    ci,cj=int(pt[0]*200),int(pt[1]*200)
    for di in (-1,0,1):
        for dj in (-1,0,1):
            for p,idx in GRID.get((ci+di,cj+dj),()):
                dd_=(p[0]-pt[0])**2+((p[1]-pt[1])*K)**2
                if dd_<bd: bd,best=dd_,HW[idx]
    if best is None or bd>(0.004)**2: return '?'
    s=best['s']
    if s in PAVED: return 'p'
    if s in RIPIO: return 'r'
    if best['hw']=='track': return 'r'
    if best['hw'] in ('motorway','motorway_link','trunk','trunk_link','primary','secondary') : return 'p'
    return '?'

def hm(t): h,m=map(int,t.split(':')); return h*60+m
def fmt(m): m=int(round(m/5.0)*5); return f"{(m//60)%24:02d}:{m%60:02d}"

routes_svg=[]; numbered=[]; cards=[]; summary=[]
for dd in DAYS:
    r=osrm(dd)
    coords=[(la,lo) for lo,la in r['geometry']['coordinates']]
    ways=surfaces(dd,coords)
    # surface per vertex segment
    cls=[]
    for i in range(len(coords)-1):
        mid=((coords[i][0]+coords[i+1][0])/2,(coords[i][1]+coords[i+1][1])/2)
        cls.append(classify(mid,ways))
    # smooth unknowns: inherit neighbour
    for i in range(len(cls)):
        if cls[i]=='?': cls[i]=cls[i-1] if i>0 and cls[i-1]!='?' else 'p'
    # leg boundaries by cumulative distance
    seglen=[hav(coords[i],coords[i+1]) for i in range(len(coords)-1)]
    legs=r['legs']; bounds=[]; acc=0; li=0; tgt=legs[0]['distance']/1000
    legrip=[0.0]*len(legs)
    for i,L in enumerate(seglen):
        if cls[i]=='r': legrip[min(li,len(legs)-1)]+=L
        acc+=L
        while li<len(legs)-1 and acc>=tgt: li+=1; tgt+=legs[li]['distance']/1000
    # draw runs
    runs=[]; cur=cls[0]; pts=[coords[0]]
    for i in range(len(cls)):
        pts.append(coords[i+1])
        if i==len(cls)-1 or cls[i+1]!=cur:
            runs.append((cur,pts));
            if i<len(cls)-1: cur=cls[i+1]; pts=[coords[i+1]]
    for c,pp in runs:
        parts=[];cur=[]
        for la,lo in pp:
            if la>=LAT0-0.02: cur.append((la,lo))
            else:
                if len(cur)>1: parts.append(cur)
                cur=[]
        if len(cur)>1: parts.append(cur)
        for part in parts:
            routes_svg.append(f'<path class="route {"rip" if c=="r" else "pav"}" data-day="{dd["id"]}" style="stroke:var({dd["col"]})" d="{path(part,eps=0.5)}"/>')
    # timetable
    t=hm(dd['start']); rows=[]; tot_km=0; tot_rip=0; drive=0
    for i,(s,dwell,txt) in enumerate(dd['stops']):
        if i>0:
            leg=legs[i-1]; km=leg['distance']/1000; mins=leg['duration']/60
            refs={}
            for st in leg['steps']:
                k=st.get('ref') or st.get('name') or ''
                if k: refs[k]=refs.get(k,0)+st['distance']
            main=[k.split(';')[0] for k,v in sorted(refs.items(),key=lambda x:-x[1]) if v>2000][:2]
            main=['ruta 5' if k=='5' else k for k in main]
            rip=legrip[i-1]
            rows.append(('leg',f"{km:.0f} km · {mins:.0f} min" + (f" · por {' y '.join(main)}" if main else '') + (f" · <b class=\"rp\">{rip:.0f} km de ripio</b>" if rip>=1.5 else '')))
            t+=mins; tot_km+=km; tot_rip+=rip; drive+=mins
        rows.append(('stop',s,fmt(t),txt))
        t+=dwell
    end=fmt(t)
    lis=[]
    for row in rows:
        if row[0]=='leg': lis.append(f'<li class="leg"><span>{row[1]}</span></li>')
        else:
            _,s,tt,txt=row
            lis.append(f'<li class="st"><span class="t">{tt}</span><div><b>{html.escape(S[s][0])}</b><p>{html.escape(txt)}</p>{fig(s)}</div></li>')
    pts=[f'{S[s][1]},{S[s][2]}' for s,_,_ in dd['stops']]
    gm='https://www.google.com/maps/dir/'+'/'.join(pts)
    meta=f"Salida {dd['start']} · {tot_km:.0f} km · {drive/60:.1f} h de manejo" + (f" · {tot_rip:.0f} km de ripio" if tot_rip>=1.5 else ' · todo pavimentado') + f" · termina cerca de las {end}"
    summary.append((dd['tag'],tot_km,drive,tot_rip,end))
    cards.append(f'<section class="day" id="{dd["id"]}" style="--c:var({dd["col"]})"><header><span class="chip">{dd["tag"]}</span><h2>{dd["title"]}</h2><p class="meta">{meta}</p></header><ol>{"".join(lis)}</ol><a class="gm" href="{gm}" target="_blank" rel="noopener">Abrir el día en Google Maps</a></section>')
    # numbered markers for this day
    seen=set(); n=0; g=[]
    for s,_,_ in dd['stops']:
        n+=1
        if S[s][1]<LAT0: continue
        x,y=P(S[s][1],S[s][2])
        key=(round(x),round(y))
        off=14 if key in seen else 0; seen.add(key)
        g.append(f'<g transform="translate({x+off:.1f},{y:.1f})"><circle r="11"/><text y="4" text-anchor="middle">{n}</text><title>{html.escape(S[s][0])}</title></g>')
    numbered.append(f'<g class="num" data-day="{dd["id"]}" style="--c:var({dd["col"]})">{"".join(g)}</g>')
    print(dd['id'],f"{tot_km:.0f} km",f"{drive/60:.1f} h",f"ripio {tot_rip:.0f}",'fin',end)


# ---- capas extra: areas protegidas y reverdecimiento ----
import base64
def stitch(segs):
    segs=[list(s) for s in segs if len(s)>1]; rings=[]
    while segs:
        c=segs.pop(0); ch=True
        while ch and c[0]!=c[-1]:
            ch=False
            for i,s in enumerate(segs):
                if s[0]==c[-1]: c=c+s[1:]; segs.pop(i); ch=True; break
                if s[-1]==c[-1]: c=c+s[::-1][1:]; segs.pop(i); ch=True; break
                if s[-1]==c[0]: c=s+c[1:]; segs.pop(i); ch=True; break
                if s[0]==c[0]: c=s[::-1]+c[1:]; segs.pop(i); ch=True; break
        rings.append(c)
    return rings
PROT_NAMES={'Parque Nacional Llanos de Challe':('PN Llanos de Challe','pn'),'Parque Nacional Desierto Florido':('PN Desierto Florido','pn'),
 'Santuario de la Naturaleza Granito Orbicular':('SN Granito Orbicular','sn'),'Santuario de la Naturaleza Humedal Costero Carrizal Bajo':('SN Humedal Carrizal Bajo','sn'),
 'Santuario de la Naturaleza Humedal Costero de Totoral':('SN Humedal de Totoral','sn'),'Santuario de la Naturaleza Desembocadura Río Copiapó':('SN Desembocadura río Copiapó','sn'),
 'Bien Nacional Protegido Yacimiento Paleontológico Cerro Ballena':('Cerro Ballena, ballenas fósiles','sn'),'Parque Paleontológico Los Dedos':('Parque Paleontológico Los Dedos','sn')}
prot_svg=[];prot_lab=[]
for e in json.load(open('prot.json',encoding='utf-8'))['elements']:
    nm=e['tags'].get('name')
    if nm not in PROT_NAMES: continue
    short,kind=PROT_NAMES[nm]
    if e['type']=='way': rings=[[(p['lat'],p['lon']) for p in e['geometry']]]
    else: rings=stitch([[(p['lat'],p['lon']) for p in m['geometry']] for m in e['members'] if m.get('role','outer') in ('outer','') and m.get('geometry')])
    dstr=' '.join(path(r,eps=0.4,close=True) for r in rings)
    prot_svg.append(f'<path class="prot {kind}" d="{dstr}"><title>{html.escape(short)}</title></path>')
    allp=[p for r in rings for p in r]; la=sum(p[0] for p in allp)/len(allp); lo=sum(p[1] for p in allp)/len(allp)
    if kind=='pn':
        x,y=P(la,lo); prot_lab.append(f'<text class="plab" x="{x:.1f}" y="{y+(34 if 'Challe' in short else 0):.1f}" text-anchor="middle">{html.escape(short)}</text>')
verde=base64.b64encode(open('verde.png','rb').read()).decode()
green_svg=f'<image class="verde" href="data:image/png;base64,{verde}" x="0" y="0" width="{W}" height="{H}" preserveAspectRatio="none"/>'

# base map
main=[p for p in chains[0] if LAT0-0.3<p[0]<LAT1+0.3]
land=path(main+[(LAT0-0.3,LON1+0.5),(LAT1+0.3,LON1+0.5)],close=True)
isl=[path(c,close=True) for c in chains[1:] if c[0]==c[-1] and LAT0<c[0][0]<LAT1]
roads=[]
for e in d:
    t=e['tags']; k=t.get('ref') or t.get('name')
    if t.get('natural') or 'geometry' not in e: continue
    g=[(p['lat'],p['lon']) for p in e['geometry']]
    if not any(LAT0-.1<a<LAT1+.1 and LON0-.1<b<LON1+.1 for a,b in g): continue
    roads.append(('r5' if k=='5' else 'rc', path(g,eps=0.8)))
road_svg=''.join(f'<path class="{c}" d="{p}"/>' for c,p in roads)
base=[]
KIND={'cho':'mir','mbc':'mir','est':'mir','mhu':'mir','cb':'mir',
      'pb':'par','pdf':'par','lag':'par',
      'paj':'flo','tot':'flo','ct':'flo','hc':'flo','bs':'flo','bar':'flo','toy':'flo','fre':'flo','fc':'flo','clb':'mir','pc':'flo',
      'pir':'geo','ton':'geo','ded':'geo','mus':'geo','msj':'geo','mra':'geo','dun':'mir','lvi':'sup','bi':'casa','val':'pue'}
SHORT={'cho':('Chorrillos','l'),'mbc':('Bahía Cisne','l'),'est':('Estuario','l'),'mhu':('Mirador Huasco','l'),'cb':('Carrizal Bajo','r'),
 'pb':('Playa Blanca','l'),'pdf':('PN Desierto Florido','r'),'lag':('Llano El Lagarto','r'),'paj':('Pajaritos','r'),'tot':('Oasis Totoral','r'),
 'ct':('Caleta Totoral','l'),'hc':('Hacienda Castilla','r'),'bs':('Bahía Salada','r'),'bar':('Barranquilla','r'),'toy':('Los Toyos','l'),
 'fre':('Freirina','r'),'fc':('Costa de Freirina','r'),'clb':('Caleta Los Bronces','l'),'pir':('Pirámides de sal','r'),'ton':('Granito Orbicular','r'),'ded':('Los Dedos, fósiles','l'),'mus':('Museo Paleontológico','r'),'msj':('Mina San José','r'),'mra':('Museo Regional','l'),'dun':('Dunas del Bramador','r'),'lvi':('Playa La Virgen · SUP','l'),'bi':('Cabaña','r'),'val':('Vallenar','r')}
def shape(kind):
    if kind=='mir': return '<path d="M0,-11 L10,7 L-10,7 Z"/>'
    if kind=='geo': return '<path d="M0,-11 L10,0 L0,11 L-10,0 Z"/>'
    if kind=='par': return '<rect x="-9" y="-9" width="18" height="18" rx="3"/>'
    if kind=='sup': return '<circle r="9"/><path class="in" d="M-5,0 L5,0"/>'
    if kind=='casa': return '<path d="M0,-11 L10,-2 L10,9 L-10,9 L-10,-2 Z"/>'
    return '<circle r="9"/>'
used=set(s for dd in DAYS for s,_,_ in dd['stops'])
for s,(name,la,lo) in S.items():
    if la<LAT0 or s not in used: continue
    x,y=P(la,lo); days=' '.join(dd['id'] for dd in DAYS if any(a==s for a,_,_ in dd['stops']))
    k=KIND.get(s,'flo'); t,side=SHORT.get(s,(name,'r'))
    tx=f'<text x="{14 if side=="r" else -14}" y="5" text-anchor="{"start" if side=="r" else "end"}">{html.escape(t)}</text>'
    base.append(f'<g class="mk k-{k}" data-days="{days}" transform="translate({x:.1f},{y:.1f})">{shape(k)}{tx}<title>{html.escape(name)}</title></g>')
labels=[('Caldera',-27.067,-70.825,'l'),('Copiapó',-27.366,-70.332,'l'),('Océano Pacífico',-27.55,-71.24,'c')]
lab=[]
for tx,la,lo,a in labels:
    x,y=P(la,lo); anchor={'r':'start','l':'end','c':'middle'}[a]; dx={'r':11,'l':-11,'c':0}[a]
    lab.append(f'<text class="{"sea" if a=="c" else "town"}" x="{x+dx:.1f}" y="{y+5:.1f}" text-anchor="{anchor}">{tx}</text>')
xb,yb=P(LAT0,-70.95)
lab.append(f'<text class="town" x="{xb:.1f}" y="{yb-12:.1f}" text-anchor="middle">↓ a La Serena, 190 km</text>')
km_px=W/((LON1-LON0)*111.32*K); sx,sy=40,H-40
scale=f'<g class="scale"><line x1="{sx}" y1="{sy}" x2="{sx+50*km_px:.1f}" y2="{sy}"/><line x1="{sx}" y1="{sy-5}" x2="{sx}" y2="{sy+5}"/><line x1="{sx+50*km_px:.1f}" y1="{sy-5}" x2="{sx+50*km_px:.1f}" y2="{sy+5}"/><text x="{sx}" y="{sy-10}">50 km</text></g>'
svg=(f'<svg viewBox="0 0 {W} {H}" role="img" aria-label="Mapa del itinerario por Atacama, de Bahía Inglesa a Huasco, con las rutas de cada día">'
 f'<rect class="sea-bg" width="{W}" height="{H}"/><path class="land" d="{land}"/>'+''.join(f'<path class="land" d="{p}"/>' for p in isl)
 +green_svg+'<g class="prots">'+''.join(prot_svg)+'</g>'+f'<g>{road_svg}</g><g>{"".join(routes_svg)}</g><g>{"".join(prot_lab)}</g><g>{"".join(lab)}</g><g>{"".join(base)}</g>{"".join(numbered)}{scale}</svg>')
sumrows=''.join(f'<tr><td>{a}</td><td class="n">{b:.0f}</td><td class="n">{c/60:.1f}</td><td class="n">{(e if e>=1.5 else 0):.0f}</td><td class="n">{f}</td></tr>' for a,b,c,e,f in summary)
btns=''.join(f'<button type="button" class="dbtn" data-day="{dd["id"]}" style="--c:var({dd["col"]})" aria-pressed="false">{dd["tag"]}</button>' for dd in DAYS)
tpl=open('tpl2.html',encoding='utf-8').read()
out=tpl.replace('%%PALEO%%',paleo_html()).replace('%%FLORES%%',flores_html()).replace('%%SVG%%',svg).replace('%%DAYS%%','\n'.join(cards)).replace('%%BTNS%%',btns).replace('%%SUM%%',sumrows)
open('desierto-florido-fotos.html' if IMGS else 'desierto-florido-mapa.html','w',encoding='utf-8').write(out)
if IMGS:
    open('desierto-florido-2026.html','w',encoding='utf-8').write('<!DOCTYPE html>\n<html lang="es-CL">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">\n'+out+'\n</html>\n')
print('bytes',len(out))
