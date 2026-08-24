/* Visor de viajes y panoramas — Nicolas Mendoza
   Vanilla JS, sin dependencias. Los datos viven en data/*.json  */

const Y0 = 2026, Y1 = 2030;              // rango de expansion de temporadas
const TL_INI = '2026-08-01', TL_FIN = '2030-06-30';
const PXD = 2.15;                         // pixeles por dia en la linea de tiempo

const S = { ev: [], cat: {}, planes: [], parques: [], fer: {}, meta: {},
            wins: [], filt: { cat: new Set(), dur: new Set(), pais: new Set(), prio: 0, q: '', fer: false, mapa: false, sug: false },
            calY: 2027 };

const d  = s => new Date(s + 'T12:00:00');
const iso = dt => dt.toISOString().slice(0, 10);
const addD = (dt, n) => { const x = new Date(dt); x.setDate(x.getDate() + n); return x; };
const days = (a, b) => Math.round((d(b) - d(a)) / 864e5);
const MES = ['ene','feb','mar','abr','may','jun','jul','ago','sep','oct','nov','dic'];
const MESL = ['enero','febrero','marzo','abril','mayo','junio','julio','agosto','septiembre','octubre','noviembre','diciembre'];
const fmt = s => { const x = d(s); return `${x.getDate()} ${MES[x.getMonth()]} ${x.getFullYear()}`; };
const fmtR = (a, b) => a === b ? fmt(a) : (d(a).getFullYear() === d(b).getFullYear()
  ? `${d(a).getDate()} ${MES[d(a).getMonth()]} – ${fmt(b)}` : `${fmt(a)} – ${fmt(b)}`);
const esc = s => String(s ?? '').replace(/[&<>"]/g, c => ({ '&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;' }[c]));
const HOY = iso(new Date());

/* ---------------- carga ---------------- */
async function boot() {
  // cache-buster por minuto: sin esto el navegador sirve el JSON viejo despues de editarlo
  const v = '?t=' + Math.floor(Date.now() / 60000);
  const [ev, pk, fe] = await Promise.all([
    fetch('data/eventos.json' + v).then(r => r.json()),
    fetch('data/parques.json' + v).then(r => r.json()),
    fetch('data/feriados.json' + v).then(r => r.json()),
  ]);
  S.ev = ev.eventos; S.cat = ev.categorias; S.planes = ev.planes; S.meta = ev._meta;
  S.parques = pk.parques; S.pkMeta = pk._meta;
  S.fer = fe; S.ferMeta = fe._meta;
  S.wins = expandir(S.ev);
  document.getElementById('fuentes-note').innerHTML =
    `Feriados de Chile 2026 y 2027 desde <code>${esc(S.ferMeta.fuente_2026_2027)}</code>, consultados el ${S.ferMeta.consultado}. ` +
    `${esc(S.ferMeta.nota_2028)} Parques nacionales desde <a href="https://somosparques.cl/" target="_blank" rel="noopener">Somos Parques</a>. ` +
    `Cada ficha lleva sus propias fuentes cuando las tiene. Datos actualizados al ${S.meta.actualizado}.`;
  drawMapa();
  buildFilters(); buildTabs(); render(); scrollHoy();
}

/* Expande `temporada` (recurrente, con wrap de ano) y `fechas` (explicitas)
   a ventanas concretas {ev, ini, fin, tag, peak}. */
function expandir(evs) {
  const out = [];
  for (const e of evs) {
    for (const f of e.fechas || []) out.push({ ev: e, ini: f.ini, fin: f.fin, tag: f.tag, peak: false });
    const t = e.temporada;
    if (!t) continue;
    // md("10-15") -> 1015, para comparar dia-del-ano sin ano
    const md = s => { const [m, dd] = s.split('-').map(Number); return m * 100 + dd; };
    const wrap = md(t.fin) < md(t.ini);            // la temporada cruza el ano nuevo
    // si un ano ya tiene fecha confirmada, no dibujar encima la ventana generica
    const yaConfirmados = new Set((e.fechas || []).map(f => +f.ini.slice(0, 4)));
    for (let y = Y0; y <= Y1; y++) {
      if (yaConfirmados.has(y)) continue;
      // en una temporada que envuelve, todo lo anterior al inicio cae en el ano siguiente
      const yr = s => (wrap && md(s) < md(t.ini)) ? y + 1 : y;
      const ini = `${y}-${t.ini}`, fin = `${yr(t.fin)}-${t.fin}`;
      if (d(fin) >= d(TL_INI) && d(ini) <= d(TL_FIN))
        out.push({ ev: e, ini, fin, tag: 'Temporada', peak: false });
      for (const p of t.peak || []) {
        const pi = `${yr(p.ini)}-${p.ini}`, pf = `${yr(p.fin)}-${p.fin}`;
        if (d(pf) >= d(TL_INI) && d(pi) <= d(TL_FIN))
          out.push({ ev: e, ini: pi, fin: pf, tag: 'Peak', peak: true });
      }
    }
  }
  return out.filter(w => d(w.fin) >= d(TL_INI) && d(w.ini) <= d(TL_FIN))
            .sort((a, b) => a.ini < b.ini ? -1 : 1);
}

const winsDe = e => S.wins.filter(w => w.ev.id === e.id);
const proxima = e => winsDe(e).find(w => w.fin >= HOY) || null;

/* ---------------- filtros ---------------- */
function pasa(e) {
  const f = S.filt;
  if (f.cat.size && !f.cat.has(e.cat)) return false;
  if (f.dur.size && !f.dur.has(e.dur)) return false;
  if (f.pais.size && !f.pais.has(e.pais)) return false;
  if (e.prio < f.prio) return false;
  if (f.q) {
    const h = (e.nombre + ' ' + e.zona + ' ' + e.pais + ' ' + (e.porque || '') + ' ' + (e.logistica || '')).toLowerCase();
    if (!h.includes(f.q.toLowerCase())) return false;
  }
  if (f.fer && !tocaFeriado(e)) return false;
  if (f.mapa && !e.mapa) return false;
  if (f.sug && !e.similar_a) return false;
  return true;
}
const evsFiltrados = () => S.ev.filter(pasa);

const todosFer = () => Object.keys(S.fer).filter(k => k !== '_meta').flatMap(y => S.fer[y]);
function tocaFeriado(e) {
  return winsDe(e).some(w => todosFer().some(f => f.d >= w.ini && f.d <= w.fin));
}

function buildFilters() {
  const cats = Object.entries(S.cat);
  const paises = [...new Set(S.ev.map(e => e.pais))].sort();
  const box = document.getElementById('filters');
  box.innerHTML = `
    <div class="grp"><label>Tipo</label>${cats.map(([k, c]) =>
      `<span class="chip" data-f="cat" data-v="${k}" style="--c:${c.c}"><i class="dot" style="background:${c.c}"></i>${c.n}</span>`).join('')}</div>
    <div class="grp"><label>Duración</label>
      <span class="chip" data-f="dur" data-v="finde" style="--c:#94a3b8">Fin de semana</span>
      <span class="chip" data-f="dur" data-v="escapada" style="--c:#94a3b8">Escapada 3-6 d</span>
      <span class="chip" data-f="dur" data-v="grande" style="--c:#94a3b8">Viaje grande</span></div>
    <div class="grp"><label>País</label>${paises.map(p =>
      `<span class="chip" data-f="pais" data-v="${esc(p)}" style="--c:#94a3b8">${esc(p)}</span>`).join('')}</div>
    <div class="grp"><label>Prioridad ≥</label>
      <select id="fprio"><option value="0">todas</option><option value="3">3</option><option value="4">4</option><option value="5">5 (imperdibles)</option></select></div>
    <div class="grp"><span class="chip" data-f="fer" data-v="1" style="--c:#eab308">Cae en feriado</span>
      <span class="chip" data-f="mapa" data-v="1" style="--c:#38bdf8">De tu mapa</span>
      <span class="chip" data-f="sug" data-v="1" style="--c:#a78bfa">Sugeridos</span></div>
    <div class="grp"><input type="search" id="fq" placeholder="Buscar: volcán, carnaval, glaciar…"></div>
    <div class="spacer"></div><div class="count" id="fcount"></div>`;

  box.querySelectorAll('.chip').forEach(ch => ch.onclick = () => {
    const f = ch.dataset.f, v = ch.dataset.v;
    if (f === 'fer' || f === 'mapa' || f === 'sug') { S.filt[f] = !S.filt[f]; ch.classList.toggle('on', S.filt[f]); }
    else { const set = S.filt[f]; set.has(v) ? set.delete(v) : set.add(v); ch.classList.toggle('on', set.has(v)); }
    ch.style.background = ch.classList.contains('on') ? ch.style.getPropertyValue('--c') : '';
    render();
  });
  document.getElementById('fprio').onchange = e => { S.filt.prio = +e.target.value; render(); };
  let t; document.getElementById('fq').oninput = e => { clearTimeout(t); t = setTimeout(() => { S.filt.q = e.target.value; render(); }, 200); };
}

/* ---------------- tabs ---------------- */
function buildTabs() {
  document.querySelectorAll('nav.tabs button').forEach(b => b.onclick = () => {
    document.querySelectorAll('nav.tabs button').forEach(x => x.classList.remove('on'));
    document.querySelectorAll('section.view').forEach(x => x.classList.remove('on'));
    b.classList.add('on');
    document.getElementById('v-' + b.dataset.v).classList.add('on');
    document.getElementById('filters').style.display = ['tl','cal','fichas'].includes(b.dataset.v) ? '' : 'none';
    if (b.dataset.v === 'tl') scrollHoy();
  });
}

function render() {
  const evs = evsFiltrados();
  document.getElementById('fcount').textContent = `${evs.length} de ${S.ev.length} panoramas`;
  drawTL(evs); drawCal(evs); drawCards(evs);
  drawPlan(); drawConf(); drawParques();
}

/* ---------------- linea de tiempo ---------------- */
function meses() {
  const out = []; let c = d(TL_INI);
  while (c <= d(TL_FIN)) {
    const ini = iso(c), y = c.getFullYear(), m = c.getMonth();
    const fin = iso(new Date(y, m + 1, 0));
    out.push({ y, m, ini, fin, x: days(TL_INI, ini) * PXD, w: (days(ini, fin) + 1) * PXD });
    c = new Date(y, m + 1, 1);
  }
  return out;
}

function drawTL(evs) {
  const MS = meses(), W = days(TL_INI, TL_FIN) * PXD;
  const grid = MS.map(m => `<div class="mo ${m.m % 6 < 3 ? 'q' : ''}" style="left:${m.x}px;width:${m.w}px"></div>`).join('');
  const hoyX = days(TL_INI, HOY) * PXD;
  const hoyEl = (hoyX > 0 && hoyX < W) ? `<div class="hoy" style="left:${hoyX}px"></div>` : '';

  const head = `<div class="tl-row tl-head"><div class="tl-lbl"><span class="nm" style="color:var(--tx3);font-size:11px">Panorama · ventana óptima</span></div>
    <div class="tl-track" style="width:${W}px">
      ${MS.map(m => `<div class="mo ${m.m % 6 < 3 ? 'q' : ''}" style="left:${m.x}px;width:${m.w}px">
        ${m.m === 0 || m.ini === TL_INI ? `<span class="mo-y">${m.y}</span>` : ''}
        <span class="mo-m">${MES[m.m]}</span></div>`).join('')}
      ${todosFer().filter(f => f.d >= TL_INI && f.d <= TL_FIN)
        .map(f => `<div class="fer" style="left:${days(TL_INI, f.d) * PXD}px" title="${esc(f.n)} — ${fmt(f.d)}"></div>`).join('')}
      ${hoyEl}</div></div>`;

  const orden = [...evs].sort((a, b) => {
    const pa = proxima(a), pb = proxima(b);
    if (!pa && !pb) return 0; if (!pa) return 1; if (!pb) return -1;
    return pa.ini < pb.ini ? -1 : pa.ini > pb.ini ? 1 : b.prio - a.prio;
  });

  const rows = orden.map(e => {
    const col = S.cat[e.cat].c;
    const bars = winsDe(e).map(w => {
      const x = days(TL_INI, w.ini) * PXD, wd = Math.max((days(w.ini, w.fin) + 1) * PXD, 4);
      const pt = wd < 9;
      return `<div class="evb ${w.peak ? 'peak' : ''} ${pt ? 'pt' : ''}" data-id="${e.id}"
        style="left:${x}px;width:${wd}px;background:${col};opacity:${w.peak ? 1 : .62}"
        title="${esc(e.nombre)} — ${fmtR(w.ini, w.fin)}${w.tag ? ' · ' + esc(w.tag) : ''}">${!pt && wd > 60 ? esc(w.tag || '') : ''}</div>`;
    }).join('');
    return `<div class="tl-row">
      <div class="tl-lbl"><span class="bar" style="background:${col}"></span>
        <span><span class="nm" data-id="${e.id}">${esc(e.nombre)}</span>
        <span class="meta">${e.mapa ? '<b style="color:#38bdf8">⚑</b> ' : ''}${'★'.repeat(e.prio)} · ${e.pais}</span></span></div>
      <div class="tl-track" style="width:${W}px">${grid}${hoyEl}${bars}</div></div>`;
  }).join('');

  document.getElementById('tl').innerHTML = head + rows;
  document.querySelectorAll('#tl [data-id]').forEach(el => el.onclick = () => openModal(el.dataset.id));
}

function scrollHoy() {
  const w = document.querySelector('.tl-wrap'); if (!w) return;
  w.scrollLeft = Math.max(0, days(TL_INI, HOY) * PXD - 260);
}

/* ---------------- calendario ---------------- */
function drawCal(evs) {
  const years = [];
  for (let y = Y0; y <= Y1; y++) years.push(y);
  document.getElementById('cal-years').innerHTML = years.map(y =>
    `<span class="chip ${y === S.calY ? 'on' : ''}" data-y="${y}" style="${y === S.calY ? 'background:var(--acc)' : ''}">${y}</span>`).join('');
  document.querySelectorAll('#cal-years .chip').forEach(c => c.onclick = () => { S.calY = +c.dataset.y; drawCal(evsFiltrados()); });

  const fer = (S.fer[S.calY] || []).reduce((a, f) => (a[f.d] = f, a), {});
  const porDia = {};
  for (const w of S.wins) {
    if (!evs.includes(w.ev)) continue;
    let c = d(w.ini);
    while (iso(c) <= w.fin) { (porDia[iso(c)] ||= new Set()).add(w.ev.id); c = addD(c, 1); }
  }

  let html = '';
  for (let m = 0; m < 12; m++) {
    const first = new Date(S.calY, m, 1), last = new Date(S.calY, m + 1, 0);
    let off = (first.getDay() + 6) % 7;                 // lunes = 0
    let cells = '<span class="cal-d out"></span>'.repeat(off);
    for (let dd = 1; dd <= last.getDate(); dd++) {
      const k = `${S.calY}-${String(m + 1).padStart(2, '0')}-${String(dd).padStart(2, '0')}`;
      const wd = new Date(S.calY, m, dd).getDay(), fin = wd === 0 || wd === 6;
      const ids = [...(porDia[k] || [])];
      const dots = ids.slice(0, 4).map(id => `<i style="background:${S.cat[S.ev.find(e => e.id === id).cat].c}"></i>`).join('');
      cells += `<span class="cal-d ${fin ? 'wk' : ''} ${fer[k] ? 'fer' : ''} ${k === HOY ? 'hoy' : ''} ${ids.length ? 'has' : ''}"
        data-k="${k}" title="${fer[k] ? esc(fer[k].n) + (fer[k].est ? ' (estimado)' : '') : ''}">${dd}<span class="cal-dots">${dots}</span></span>`;
    }
    html += `<div class="cal-mo"><h3>${MESL[m]}</h3>
      <div class="cal-dow"><span>L</span><span>M</span><span>M</span><span>J</span><span>V</span><span>S</span><span>D</span></div>
      <div class="cal-days">${cells}</div></div>`;
  }
  document.getElementById('cal').innerHTML = html;
  document.querySelectorAll('#cal .cal-d.has').forEach(c => c.onclick = () => {
    const ids = [...porDia[c.dataset.k]];
    if (ids.length === 1) openModal(ids[0]); else openDia(c.dataset.k, ids);
  });
}

/* ---------------- fichas ---------------- */
function drawCards(evs) {
  const orden = [...evs].sort((a, b) => {
    const pa = proxima(a), pb = proxima(b);
    if (!pa) return 1; if (!pb) return -1;
    return pa.ini < pb.ini ? -1 : 1;
  });
  document.getElementById('cards').innerHTML = orden.map(cardHTML).join('');
  document.querySelectorAll('#cards [data-id]').forEach(el => el.onclick = e => {
    if (e.target.tagName === 'A' || e.target.closest('details')) return; openModal(el.dataset.id);
  });
}

const sugTag = e => e.similar_a ? '<span class="tag sug">✦ Sugerido</span>' : '';
const sugLinea = e => e.similar_a ? `<p class="p"><b>Se parece a:</b> ${esc(e.similar_a)}</p>` : '';
const mapaTag = e => e.mapa ? `<span class="tag mapa" title="${esc(e.mapa)}">⚑ De tu mapa</span>` : '';

const DUR = { finde: 'Fin de semana', escapada: 'Escapada 3-6 d', grande: 'Viaje grande' };
const CERT = { fija: 'Fecha fija', movil: 'Fecha calculada', estimada: 'Fecha por confirmar', clima: 'Depende del clima' };

function cardHTML(e) {
  const col = S.cat[e.cat].c, p = proxima(e), ws = winsDe(e);
  const dias = p ? days(HOY, p.ini) : null;
  const cuando = p
    ? `<div class="next ${dias < 0 ? 'pas' : ''}">${dias > 0 ? `En ${dias} días · ` : dias === 0 ? 'HOY · ' : 'En curso · '}${fmtR(p.ini, p.fin)}${p.tag ? ` · ${esc(p.tag)}` : ''}</div>`
    : `<div class="next pas">Sin ventana futura cargada</div>`;
  return `<article class="card" data-id="${e.id}"><div class="cbar" style="background:${col}"></div><div class="cin">
    <div class="tags"><span class="tag k" style="background:${col}">${S.cat[e.cat].n}</span>
      <span class="tag">${DUR[e.dur]}</span><span class="tag prio">${'★'.repeat(e.prio)}</span>
      <span class="tag">${CERT[e.certeza]}</span>${mapaTag(e)}${sugTag(e)}</div>
    <h3>${esc(e.nombre)}</h3>
    <div class="tag" style="align-self:flex-start">${esc(e.pais)} · ${esc(e.zona)}</div>
    ${cuando}
    ${sugLinea(e)}
    <p class="p"><b>Por qué:</b> ${esc(e.porque)}</p>
    ${e.alerta ? `<div class="alerta"><b>Ojo:</b> ${esc(e.alerta)}</div>` : ''}
    <details class="det"><summary>Logística, ventanas y fuentes</summary><div class="body">
      <p class="p">${esc(e.logistica || '')}</p>
      <div>${ws.map(w => `<div class="win"><b>${fmtR(w.ini, w.fin)}</b><span>${esc(w.tag || '')}</span></div>`).join('')}</div>
      ${e.temporada?.nota ? `<p class="p" style="color:var(--tx3)"><b>Nota de temporada:</b> ${esc(e.temporada.nota)}</p>` : ''}
      ${e.verificado ? `<p class="p" style="color:var(--tx3)"><b>Verificación:</b> ${esc(e.verificado)}</p>` : ''}
      ${e.lat ? `<a href="https://www.google.com/maps/@${e.lat},${e.lon},9z" target="_blank" rel="noopener">Ver ubicación en Google Maps ↗</a>` : ''}
      ${e.fuentes?.length ? `<div class="srcs">${e.fuentes.map(f => `<a href="${esc(f.u)}" target="_blank" rel="noopener">${esc(f.t)} ↗</a>`).join('')}</div>` : ''}
    </div></details></div></article>`;
}

/* ---------------- plan ---------------- */
function drawPlan() {
  document.getElementById('plan').innerHTML = S.planes.map(p => {
    const anc = S.ev.find(e => e.id === p.ancla);
    return `<div class="plan-y">
      <div class="plan-h"><span class="yr">${p.ano}</span><h3>${esc(p.titulo)}</h3>
        ${anc ? `<span class="tag k" style="background:${S.cat[anc.cat].c}">Ancla: ${esc(anc.nombre)}</span>` : ''}</div>
      <div class="plan-b"><p>${esc(p.texto)}</p>
        ${p.items.map(i => {
          const e = S.ev.find(x => x.id === i.id); if (!e) return '';
          return `<div class="plan-i"><span class="when">${esc(i.cuando)}</span>
            <span class="what"><a data-id="${e.id}">${esc(e.nombre)}</a>
            <span class="nt">${esc(i.nota || '')}</span></span></div>`;
        }).join('')}</div></div>`;
  }).join('');
  document.querySelectorAll('#plan [data-id]').forEach(a => a.onclick = () => openModal(a.dataset.id));
}

/* ---------------- conflictos ---------------- */
function drawConf() {
  const big = S.wins.filter(w => w.ev.prio >= 4 && w.fin >= HOY && (days(w.ini, w.fin) <= 40));
  const grupos = [];
  for (const a of big) {
    let g = grupos.find(g => g.some(b => !(b.fin < a.ini || b.ini > a.fin)));
    if (g) { if (!g.some(b => b.ev.id === a.ev.id)) g.push(a); } else grupos.push([a]);
  }
  const cs = grupos.filter(g => new Set(g.map(x => x.ev.id)).size > 1)
    .sort((a, b) => a[0].ini < b[0].ini ? -1 : 1);
  document.getElementById('conf').innerHTML = cs.length ? cs.map(g => {
    const ini = g.map(x => x.ini).sort()[0], fin = g.map(x => x.fin).sort().pop();
    return `<div class="conf"><h3>${fmtR(ini, fin)} — ${g.length} panoramas de prioridad alta se pisan</h3>
      <ul>${g.map(w => `<li><a data-id="${w.ev.id}">${esc(w.ev.nombre)}</a> · ${fmtR(w.ini, w.fin)} · ${w.ev.pais} · ${'★'.repeat(w.ev.prio)}
        ${w.ev.certeza === 'fija' ? ' <b style="color:var(--bad)">(fecha inamovible)</b>' : ''}</li>`).join('')}</ul></div>`;
  }).join('') : '<p class="note">Sin choques entre panoramas de prioridad 4 o 5 en las ventanas cargadas.</p>';
  document.querySelectorAll('#conf [data-id]').forEach(a => a.onclick = () => openModal(a.dataset.id));
}

/* ---------------- parques ---------------- */
function drawParques() {
  const box = document.getElementById('parques');
  if (box.dataset.done) return;
  box.dataset.done = '1';
  const zonas = [...new Set(S.parques.map(p => p.z))];
  box.innerHTML = `
    <p class="note" style="margin:0 0 14px">Los ${S.parques.length} parques nacionales publicados por
      <a href="https://somosparques.cl/" target="_blank" rel="noopener">Somos Parques</a>.
      ${esc(S.pkMeta.reservas)}<br>${esc(S.pkMeta.nota_temporada)}</p>
    <div class="filters" style="margin-bottom:14px">
      <div class="grp"><label>Zona</label>${zonas.map(z => `<span class="chip" data-z="${z}" style="--c:#94a3b8">${z}</span>`).join('')}</div>
      <div class="grp"><label>Desde Temuco</label>
        <span class="chip" data-d="cerca" style="--c:#22c55e">&lt; 3 h</span>
        <span class="chip" data-d="medio" style="--c:#eab308">3-8 h</span>
        <span class="chip" data-d="lejos" style="--c:#94a3b8">Vuelo</span></div>
    </div>
    <table class="pk"><thead><tr><th>Parque</th><th>Región</th><th>Zona</th><th>Desde Temuco</th><th>Temporada</th><th>Por qué</th></tr></thead>
    <tbody id="pkb"></tbody></table>`;
  const fz = new Set(), fd = new Set();
  const pinta = () => document.getElementById('pkb').innerHTML = S.parques
    .filter(p => (!fz.size || fz.has(p.z)) && (!fd.size || fd.has(p.d)))
    .map(p => `<tr><td class="nm">${esc(p.n)}</td><td>${esc(p.reg)}</td><td>${esc(p.z)}</td>
      <td><span class="pill ${p.d}">${p.d === 'cerca' ? '< 3 h' : p.d === 'medio' ? '3-8 h' : 'vuelo'}</span></td>
      <td>${esc(p.temp)}</td><td class="nt">${esc(p.nota)}</td></tr>`).join('');
  box.querySelectorAll('.chip').forEach(c => c.onclick = () => {
    const set = c.dataset.z ? fz : fd, v = c.dataset.z || c.dataset.d;
    set.has(v) ? set.delete(v) : set.add(v);
    c.classList.toggle('on', set.has(v));
    c.style.background = c.classList.contains('on') ? c.style.getPropertyValue('--c') : '';
    pinta();
  });
  pinta();
}

/* ---------------- modal ---------------- */
function openModal(id) {
  const e = S.ev.find(x => x.id === id); if (!e) return;
  const col = S.cat[e.cat].c, ws = winsDe(e);
  const combos = (e.combo || []).map(c => S.ev.find(x => x.id === c)).filter(Boolean);
  document.getElementById('modal').innerHTML = `
    <div class="cbar" style="background:${col}"></div>
    <div class="mh"><div><h2 style="font-size:19px">${esc(e.nombre)}</h2>
      <div class="tags" style="margin-top:8px"><span class="tag k" style="background:${col}">${S.cat[e.cat].n}</span>
        <span class="tag">${esc(e.pais)} · ${esc(e.zona)}</span><span class="tag">${DUR[e.dur]} (${e.dias[0]}-${e.dias[1]} días)</span>
        <span class="tag prio">${'★'.repeat(e.prio)}</span><span class="tag">${CERT[e.certeza]}</span>${mapaTag(e)}${sugTag(e)}</div></div>
      <button class="x" onclick="cerrar()">×</button></div>
    <div class="mb">
      ${sugLinea(e)}
      <p class="p"><b>Por qué vale la pena:</b> ${esc(e.porque)}</p>
      ${e.alerta ? `<div class="alerta"><b>Ojo:</b> ${esc(e.alerta)}</div>` : ''}
      <p class="p"><b>Logística:</b> ${esc(e.logistica || '—')}</p>
      <div><b style="font-size:12px;color:var(--tx3);text-transform:uppercase;letter-spacing:.06em">Ventanas</b>
        ${ws.map(w => `<div class="win"><b>${fmtR(w.ini, w.fin)}</b><span>${esc(w.tag || '')}</span></div>`).join('')}</div>
      ${e.temporada?.nota ? `<p class="p" style="color:var(--tx3)"><b>Nota de temporada:</b> ${esc(e.temporada.nota)}</p>` : ''}
      ${e.verificado ? `<p class="p" style="color:var(--tx3)"><b>Verificación:</b> ${esc(e.verificado)}</p>` : ''}
      ${combos.length ? `<p class="p"><b>Se encadena bien con:</b> ${combos.map(c => `<a data-id="${c.id}">${esc(c.nombre)}</a>`).join(' · ')}</p>` : ''}
      ${e.lat ? `<a href="https://www.google.com/maps/@${e.lat},${e.lon},9z" target="_blank" rel="noopener">Abrir en Google Maps ↗</a>` : ''}
      ${e.fuentes?.length ? `<div class="srcs"><b style="font-size:12px;color:var(--tx3)">Fuentes</b>
        ${e.fuentes.map(f => `<a href="${esc(f.u)}" target="_blank" rel="noopener">${esc(f.t)} ↗</a>`).join('')}</div>` : ''}
    </div>`;
  document.querySelectorAll('#modal [data-id]').forEach(a => a.onclick = () => openModal(a.dataset.id));
  document.getElementById('mask').classList.add('on');
}

function openDia(k, ids) {
  const fer = (S.fer[k.slice(0, 4)] || []).find(f => f.d === k);
  document.getElementById('modal').innerHTML = `
    <div class="cbar" style="background:var(--acc)"></div>
    <div class="mh"><div><h2 style="font-size:19px">${fmt(k)}</h2>
      ${fer ? `<div class="tag" style="margin-top:6px;background:rgba(234,179,8,.16);color:var(--warn)">Feriado: ${esc(fer.n)}${fer.est ? ' (estimado)' : ''}</div>` : ''}</div>
      <button class="x" onclick="cerrar()">×</button></div>
    <div class="mb">${ids.map(id => {
      const e = S.ev.find(x => x.id === id);
      return `<div class="plan-i"><span class="when" style="min-width:130px;color:${S.cat[e.cat].c}">${S.cat[e.cat].n}</span>
        <span class="what"><a data-id="${e.id}">${esc(e.nombre)}</a><span class="nt">${esc(e.zona)} · ${DUR[e.dur]}</span></span></div>`;
    }).join('')}</div>`;
  document.querySelectorAll('#modal [data-id]').forEach(a => a.onclick = () => openModal(a.dataset.id));
  document.getElementById('mask').classList.add('on');
}

function cerrar() { document.getElementById('mask').classList.remove('on'); }
document.addEventListener('keydown', e => e.key === 'Escape' && cerrar());
document.getElementById('mask').onclick = e => { if (e.target.id === 'mask') cerrar(); };

boot();

/* ---------------- pines del mapa del usuario ---------------- */
function drawMapa() {
  const m = S.meta.mapa_usuario; if (!m) return;
  document.getElementById('mapa-user').innerHTML = `
    <h2 style="font-size:16px">Tu lista de Google Maps</h2>
    <p class="p">De <b>${esc(m.lista)}</b> se leyeron <b>${m.leidos} de ${m.total_declarado}</b> sitios el ${m.leido}.
      ${esc(m.nota)}</p>
    <div>${(m.racimos || []).map(r => `<div class="plan-i">
      <span class="when" style="min-width:230px">${esc(r.n)} · ${r.c} pines</span>
      <span class="what"><span class="nt" style="margin:0">${esc(r.detalle)}</span></span></div>`).join('')}</div>
    ${(m.pines_resueltos || []).map(r => `<div class="alerta" style="background:rgba(34,197,94,.1);border-left-color:var(--ok);color:#86efac">
      <b>${esc(r.pin)} → ${esc(r.coordenadas)}</b><br>${esc(r.ubicacion)}<br>
      <span style="color:var(--tx2)">${esc(r.distancias)}</span><br>
      <span style="color:var(--tx2)">${esc(r.relevancia)}</span><br>
      <span style="color:var(--tx3);font-size:11px">Verificado ${esc(r.verificado)}</span></div>`).join('')}
    <h3 style="font-size:13.5px;margin-top:6px">Pines que no se pudieron ubicar con certeza</h3>
    <p class="note" style="margin:0 0 8px">Estos no se agendaron: sin ubicación confirmada no hay temporada que asignar.</p>
    ${m.pines_ambiguos.map(a => `<div class="plan-i"><span class="when" style="min-width:230px">${esc(a.pin)}</span>
      <span class="what"><span class="nt" style="margin:0">${esc(a.duda)}</span></span></div>`).join('')}
    <p class="p" style="margin-top:12px"><a href="${esc(m.url)}" target="_blank" rel="noopener">Abrir la lista en Google Maps ↗</a></p>
    ${sugPanel()}`;
}

/* ---------------- sitios analogos sugeridos ---------------- */
function sugPanel() {
  const g = S.meta.sugerencias; if (!g) return '';
  const sug = S.ev.filter(e => e.similar_a);
  const paises = [...new Set(sug.map(e => e.pais))];
  return `<hr style="border:0;border-top:1px solid var(--line);margin:20px 0 4px">
    <h2 style="font-size:16px">Sitios análogos que no tienes marcados</h2>
    <p class="p">${esc(g.que_es)}</p>
    <p class="note" style="margin:0">${esc(g.como_verlos)}</p>
    ${paises.map(pa => `<div style="margin-top:12px">
      <b style="font-size:12px;color:var(--tx3);text-transform:uppercase;letter-spacing:.06em">${esc(pa)} · ${sug.filter(e => e.pais === pa).length}</b>
      ${sug.filter(e => e.pais === pa).map(e => `<div class="plan-i">
        <span class="when" style="min-width:230px"><a data-id="${e.id}">${esc(e.nombre)}</a></span>
        <span class="what"><span class="nt" style="margin:0">Se parece a: ${esc(e.similar_a)}</span></span></div>`).join('')}
    </div>`).join('')}`;
}
