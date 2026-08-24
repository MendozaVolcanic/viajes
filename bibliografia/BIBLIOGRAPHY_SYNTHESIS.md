# Síntesis bibliográfica — Desierto Florido

Investigación del 2026-08-23 para responder: **¿qué tan confiable es el peak proyectado a mediados de octubre de 2026, y qué señal objetiva permite afinar fecha y sector con 7–10 días de anticipación?**

---

## Chávez et al. 2019 — Detección satelital de los "desiertos floridos" del Atacama

**Cita**: Chávez, R.O.; Moreira-Muñoz, A.; Galleguillos, M.; Olea, M.; Aguayo, J.; Latín, A.; Aguilera-Betti, I.; Muñoz, A. (2019). *GIMMS NDVI time series reveal the extent, duration, and intensity of "blooming desert" events in the hyper-arid Atacama Desert, Northern Chile*. **International Journal of Applied Earth Observation and Geoinformation**. DOI [10.1016/j.jag.2018.11.013](https://doi.org/10.1016/j.jag.2018.11.013). 65 citas (Semantic Scholar, ago-2026).

**Es el paper seminal del tema.** Primer trabajo que cuantifica el fenómeno en vez de describirlo.

### Método
Reconstruyen la fenología de superficie (Land Surface Phenology) del Atacama con series NDVI de GIMMS mediante un enfoque estadístico **no paramétrico**, y detectan los desiertos floridos como **anomalías positivas de NDVI**. Caracterizan cada evento en tres dimensiones: extensión temporal, intensidad del reverdecimiento y extensión espacial.

### Resultados que importan para planificar un viaje

| Hallazgo | Valor | Implicancia práctica |
|---|---|---|
| Eventos detectados 1981–2015 | **13** | Uno cada ~2,7 años en promedio |
| Eventos **mayores** | **3** (1997-98, 2002-03, 2011) | Un evento grande cada ~12 años. No es anual |
| Evento mayor del registro | **2011**: 180 días (julio–diciembre), **11.136 km²** | El techo medido del fenómeno |
| Disparador | Precipitación acumulada en una ventana de **2 a 12 meses** antes y durante el evento | No basta la lluvia de un mes; y la lluvia ya caída ya define el evento |

### Las dos correcciones que este paper le hace al relato de prensa

1. **La cifra de "hasta 15.000 km²" que circula para 2026 excedería en ~35 % el récord del registro satelital** (11.136 km² en 2011). Tratarla como aspiración promocional, no como medición.
2. **Un evento mayor dura meses, no semanas.** El de 2011 abarcó 180 días. Eso significa que el "peak" de mediados de octubre es un centro de masa, no una ventana estrecha: errar por una o dos semanas no arruina el viaje.

### Limitación de acceso (documentada para no reintentar)
El artículo es de pago en Elsevier. Unpaywall reporta **una sola** ubicación OA: el repositorio de la Universidad de Chile ([handle 2250/171758](https://repositorio.uchile.cl/handle/2250/171758)). Ese bitstream **devuelve HTML disfrazado de PDF** (7,3 KB, magic bytes `<!doc`) con y sin User-Agent de navegador, con Referer y con cookie jar. Verificado tres veces el 2026-08-23. Para conseguir el PDF completo hay que abrirlo desde un navegador con sesión, o pedirlo por otra vía. El abstract completo sí se obtuvo vía API de Semantic Scholar y contiene todos los números citados arriba.

---

## ENSO — el proxy popular no es confiable

**Fuente primaria**: NOAA Climate Prediction Center, tabla ONI basada en ERSST v6 — <https://www.cpc.ncep.noaa.gov/products/analysis_monitoring/enso/oni/v6/>

### ONI 2026 (consultado 2026-08-23)

| Trimestre | ONI |
|---|---|
| DJF | −0,4 |
| JFM | −0,2 |
| FMA | +0,1 |
| MAM | +0,5 |
| AMJ | +0,9 |
| **MJJ (último publicado)** | **+1,4** |

Transición de La Niña a El Niño en cinco meses. NOAA declaró condiciones de El Niño el 11 de junio de 2026.

### El contraejemplo que rompe la regla popular

Se repite mucho que "el desierto florido es un fenómeno de El Niño". Los ONI de los tres eventos mayores identificados por Chávez et al. dicen otra cosa:

| Evento mayor | ONI JJA | ONI OND | Fase |
|---|---|---|---|
| 1997 | +1,5 | +2,3 | El Niño muy fuerte |
| 2002 | +0,6 | +1,2 | El Niño moderado |
| **2011** | **−0,4** | **−1,0** | **La Niña** |

**El mayor desierto florido del registro satelital ocurrió en un año La Niña.** Coherente con la conclusión del propio paper: el disparador es la **precipitación acumulada**, no la etiqueta ENSO. ENSO modula la probabilidad de que llueva, pero una vez que la lluvia cayó, el índice deja de aportar información.

Para 2026 esto significa: El Niño está presente y ayuda, pero **el argumento fuerte es la lluvia ya medida**, no el pronóstico oceánico.

---

## Precipitación medida — invierno 2026 en Atacama

**Fuente**: Radio Atacama, 8 de agosto de 2026, con datos de la **Red Agrometeorológica de INIA Intihuasi**, Agroclima, DGA y CEAZA. Voceros: Giovanni Lobos y Víctor Muñoz (INIA Intihuasi).

| Localidad | Acumulado 2026 | Contexto |
|---|---|---|
| Alto del Carmen | **210,8 mm** | Mayor acumulado de la región |
| **Vallenar** | **186,9 mm** | Normal anual: **40,2 mm** → **4,6 veces la normal**. Año más lluvioso desde 2004 |
| Amolanas (Tierra Amarilla) | 109 mm | Sector alto del valle |
| **Copiapó** | **24,2 mm** | Muy por debajo del resto |

Años previos más lluviosos desde 2004: 2015 (115,6 mm) y 2017 (100,1 mm) en Vallenar — ambos años de desierto florido. **2026 casi duplica al mayor de los dos.**

### La conclusión operativa

**La lluvia cayó en la provincia de Huasco, no en Copiapó.** El gradiente es de casi un orden de magnitud entre Alto del Carmen y Copiapó. Por lo tanto la floración debería ser marcadamente más fuerte en el **sur de la región** — Vallenar, Alto del Carmen, Freirina, Huasco y el PN Llanos de Challe — que en el sector Travesía de Copiapó.

Umbral de germinación citado por la prensa regional: ~15 mm. Vallenar lo superó doce veces.

---

## Monitoreo operacional — qué existe y qué no

- **CONAF tiene un Sistema de Monitoreo Fenológico satelital** (MODIS, índices de vegetación, cadencia de 16 días, enfoque no paramétrico — el mismo del paper de Chávez) para unidades del SNASPE: <https://sites.google.com/conaf.cl/monitoreo-snaspe/>
- **Pero NO cubre Atacama.** Las unidades implementadas son La Campana, Río Clarillo, Nahuelbuta y Pumalín. **No sirve para el desierto florido.**
- La Comisión Regional del Desierto Florido declara "monitoreo permanente" de las floraciones, pero no publica un producto de datos abierto.

**Conclusión**: no hay un producto satelital público y operacional para seguir el desierto florido semana a semana. Los reportes regionales de CONAF son cualitativos.

### La alternativa que ya está instalada en el workspace

El método de Chávez et al. — anomalía positiva de NDVI contra la fenología esperada — es exactamente lo que hace el pipeline de **Copernicus-v1**, pero con Sentinel-2 a 10 m en vez de GIMMS a ~8 km. Apuntar ese pipeline a un par de polígonos (Llanos de Challe, costa de Huasco, costa de Freirina, Travesía) durante septiembre y octubre daría una serie de NDVI propia, con revisita de 5 días y resolución tres órdenes de magnitud mejor que la del paper. Es la manera de decidir el sector exacto con 7–10 días de anticipación en vez de depender de notas de prensa.

---

## Fuentes de prensa 2026 usadas (todas verificadas por fecha)

- [Atacama Noticias, 21-ago-2026](https://www.atacamanoticias.cl/2026/08/21/atacama-prepara-una-gran-temporada-del-desierto-florido-2026-con-coordinacion-regional-promocion-turistica-y-puntos-de-avistamiento/) — Comisión Regional, cinco puntos de avistamiento, normas para visitantes
- [ExtraNoticias, 22-ago-2026](https://www.extranoticias.cl/desierto-florido-anticipa-una-temporada-historica-en-atacama-con-brotes-desde-finales-de-agosto/) — brotes desde fines de agosto, peak a mediados de octubre, >200 variedades endémicas
- [Megatiempo, 21-ago-2026](https://www.megatiempo.cl/pronostico/13811-desierto-florido-chile-donde-queda-2026-1ab.html) — añañucas ya visibles, rol de la camanchaca en la franja costera
- [Radio Atacama, 8-ago-2026](https://www.radioatacama.cl/regional/provincia-huasco-concentro-mayores-precipitaciones-regionales) — acumulados por localidad

## ⚠️ Fuente descartada

[Ladera Sur — "Habrá Desierto Florido: las lluvias superaron el umbral necesario"](https://laderasur.com/articulo/habra-desierto-florido-las-lluvias-superaron-el-umbral-necesario-y-se-espera-floracion-desde-septiembre/) es del **11 de agosto de 2025**, no de 2026. Sus cifras (Vallenar 168,1 mm, 86 % de estaciones de Huasco con récord) corresponden a la temporada anterior y **no deben citarse para 2026**. Aparece alto en las búsquedas porque el título no lleva año.
