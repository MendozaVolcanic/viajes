import re
t = open('../tpl2.html', encoding='utf-8').read()
style = t[t.index('<style>'):t.index('</style>') + 8]
script = t[t.index('<script>'):t.index('</script>') + 9]
fonts = t[t.index('<link rel="preconnect"'):t.index('<style>')]
style = style.replace('--d1:#6E726D; --d2:#B03A78; --d3:#B86E0E; --d4:#2E6E8E;', '--d1:#6E726D; --d2:#B03A78; --d3:#B86E0E; --d4:#2E6E8E; --d5:#4F7A2E; --d6:#7A4FA0; --d7:#8A5A44;')
style = style.replace('--d1:#A3A8A2; --d2:#E07AB2; --d3:#E5A04A; --d4:#6FB2D3;', '--d1:#A3A8A2; --d2:#E07AB2; --d3:#E5A04A; --d4:#6FB2D3; --d5:#9BCB72; --d6:#C29BE5; --d7:#D9A88F;')
assert '--d5' in style
style = style.replace('.sea-bg{fill:var(--sea)}', '.sea-bg{fill:var(--sea)} .land-bg{fill:var(--land)} .sea-fill{fill:var(--sea)} .lake{fill:var(--sea);stroke:var(--road5);stroke-width:.4;fill-rule:evenodd}\n.route.boat{stroke-dasharray:8 6;stroke-width:3.5}')
script = script.replace("document.getElementById('ly-verde').addEventListener", "document.getElementById('ly-verde')?.addEventListener")
script = script.replace("fs.innerHTML='<div class=\"bar2\"><b>Ruta del Desierto Florido</b>", "fs.innerHTML='<div class=\"bar2\"><b>Magallanes en diciembre</b>")
S = 'stroke="currentColor" stroke-width="1.8"'
def item(svg, label): return f'<span class="lg"><svg width="28" height="18" viewBox="0 0 28 18" aria-hidden="true">{svg}</svg>{label}</span>'
legend = ''.join([
    item(f'<path d="M14,2 L21,15 L7,15 Z" fill="#FFFFFF" {S}/>', 'Mirador'),
    item(f'<rect x="7.5" y="2.5" width="13" height="13" rx="2.5" fill="#3E8A5B" {S}/>', 'Parque o monumento natural'),
    item(f'<path d="M14,2 L21,9 L14,16 L7,9 Z" fill="#D08A1E" {S}/>', 'Museo, historia o cueva'),
    item(f'<path d="M14,2 L21,8 L21,16 L7,16 L7,8 Z" fill="currentColor" {S}/>', 'Ciudad o alojamiento'),
    item(f'<circle cx="14" cy="9" r="6.5" fill="#C2457F" {S}/>', 'Parada de servicio'),
    item('<rect x="2" y="3" width="24" height="12" rx="2" fill="rgba(62,138,91,.16)" stroke="#2F6E47" stroke-width="2.4" stroke-dasharray="6 3"/>', 'Parque nacional'),
    item('<line x1="2" y1="9" x2="26" y2="9" stroke="currentColor" stroke-width="4" stroke-linecap="round"/>', 'Ruta en auto'),
    item('<line x1="2" y1="9" x2="26" y2="9" stroke="currentColor" stroke-width="3.5" stroke-dasharray="5 4"/>', 'Navegación'),
])
body = f'''<title>Magallanes en diciembre</title>
{fonts}{style}
<div class="wrap">
  <h1>Magallanes en diciembre</h1>
  <p class="lede">Siete días, del sábado 12 al viernes 18 de diciembre de 2026, para tres personas, con auto arrendado en Punta Arenas. Pensado para caminatas de no más de 45 minutos y no más de unas 4 horas de manejo al día, con un día de reserva por si el clima no acompaña en Torres del Paine. En diciembre hay luz de 5:10 a 22:00.</p>
  <ul class="facts">
    <li><b>Mayores de 60:</b> entran gratis a Torres del Paine y a la Cueva del Milodón</li>
    <li><b>Bencina:</b> no hay dentro del parque, se carga en Natales</li>
    <li><b>Viento:</b> diciembre es el mes más ventoso; ráfagas de hasta 100 km/h en el parque</li>
  </ul>
  <div class="tw"><table class="sum">
    <thead><tr><th>Día</th><th>Qué</th><th class="n">Km</th><th class="n">Horas de manejo</th><th class="n">Termina</th></tr></thead>
    <tbody>%%SUM%%</tbody>
  </table></div>
  <p class="hint">Clima de diciembre: la estación de la Dirección Meteorológica en Punta Arenas registra 7,5 días con lluvia de 1 mm o más y 232 horas de sol, unas 7,5 por día (1991-2020). Torres del Paine, junto a la cordillera, es más lluvioso y cambiante: por eso el martes 15 queda de reserva. Con el vuelo de llegada a las 16:00 del sábado no alcanza el Museo Borgatello, que cierra a las 17:30 y no abre domingo ni lunes.</p>
  <div class="bar" role="group" aria-label="Destacar un día en el mapa">
    <button type="button" class="all" id="btn-all">Todos los días</button>
    %%BTNS%%
  </div>
  <div class="grid">
    <figure class="map" style="margin:0">
      %%SVG%%
      <div class="layers">
        <button type="button" class="zoom-btn" id="open-fs">Agrandar mapa</button>
        <label><input type="checkbox" id="ly-prot" checked> Parque nacional</label>
      </div>
      <div class="lgd">{legend}</div>
      <p class="hint">Elige un día arriba para ver sus paradas numeradas.</p>
      <figcaption>Costa, lagos, caminos y límite del parque: OpenStreetMap. Rutas calculadas con OSRM; dentro del parque son de ripio y el ruteador es optimista: súmales 20 a 30 %.</figcaption>
    </figure>
    <div class="days">
      %%DAYS%%
    </div>
  </div>
  %%EXTRA%%
  <section class="notes">
    <h2>Antes de reservar</h2>
    <ul>
      <li><b>Pingüinos:</b> Isla Magdalena sigue abierta: CONAF descartó suspender el turismo y la Corte de Apelaciones de Punta Arenas rechazó el recurso que lo pedía (abril de 2026). La colonia sí está muy disminuida, unas 7.000 parejas según CONAF (feb-2026). Reserva con Comapa con tiempo y confirma el horario. Seno Otway está cerrado al turismo. Pingüino Rey, en Tierra del Fuego, son más de 9 horas de transporte en el día: no lo recomiendo para ellos.</li>
      <li><b>Alojamiento:</b> Natales y Torres del Paine tienen sobre 85 % de ocupación en temporada. Reserva Natales (días 3 y 5) y Río Serrano (día 4) apenas tengan fechas.</li>
      <li><b>Auto:</b> retíralo y devuélvelo en el aeropuerto de Punta Arenas para no pagar recargo de una vía. Mejor un SUV o un auto alto por el ripio del parque, con seguro de vidrios y neumáticos. Mitta, Europcar, Econorent y Avis atienden en el aeropuerto.</li>
      <li><b>Torres del Paine:</b> pases en pasesparques.cl; el hermano paga $9.400 por un día (adulto chileno, 2026) y los mayores de 60 entran liberados. El sitio del parque da horario de 8:00 a 19:00; Pases Parques da 7:00 a 21:00 en verano: confírmalo.</li>
      <li><b>Clima:</b> entre 6 y 15 °C, con viento fuerte. Lleva cortaviento, gorro y lentes de sol aunque sea verano.</li>
      <li><b>Cerrado:</b> el Palacio Braun-Menéndez (Museo Regional de Magallanes) está en restauración y reabriría en 2030.</li>
      <li><b>Versión de 6 días:</b> se saca el sábado libre. Funciona, pero se pierde el margen para elegir el día despejado en el parque.</li><li><b>Opcionales pagados</b>, fuera del plan base: navegación al glaciar Grey ($120.000), navegación Balmaceda-Serrano ($120.000) y catamarán del Pehoé ($27.000 por tramo la temporada pasada). Las Torres, los Cuernos y el glaciar se ven bien desde los miradores, Pudeto y la playa del Lago Grey.</li>
    </ul>
  </section>
  <p class="src">Fuentes: <a href="https://parquetorresdelpaine.cl/tarifas-y-horarios-2026/" target="_blank" rel="noopener">Parque Torres del Paine, tarifas 2026</a> · <a href="https://www.conaf.cl/parque_nacionales/monumento-natural-los-pinguinos/" target="_blank" rel="noopener">CONAF, Monumento Natural Los Pingüinos</a> · <a href="https://comapa.com/en/tours/penguin-tour/" target="_blank" rel="noopener">Comapa, tour a Isla Magdalena</a> · <a href="https://cuevadelmilodon.cl/horarios-y-precios/" target="_blank" rel="noopener">Cueva del Milodón, horarios</a> · <a href="https://www.museomaggiorinoborgatello.cl" target="_blank" rel="noopener">Museo Borgatello</a> · <a href="https://parquedelestrecho.cl" target="_blank" rel="noopener">Parque del Estrecho</a> · Mapa base © colaboradores de OpenStreetMap. Fotos de Wikimedia Commons con su autor y licencia al pie, recortadas para encajar.</p>
</div>
{script}
'''
open('tpl_pa.html', 'w', encoding='utf-8').write(body)
print('ok')
