# Panoramas — calendario de viajes 2026–2030

Visor estático de las **ventanas óptimas** para viajes, fiestas y fenómenos naturales en Chile y el Cono Sur,
armado desde Temuco. Sin build, sin dependencias, sin backend: HTML + CSS + JS vanilla + tres JSON.

**Visor publicado:** https://mendozavolcanic.github.io/viajes/

## Qué resuelve

El problema no es no saber qué hacer, es que las ventanas buenas se pierden por no verlas a tiempo.
El desierto florido dura seis semanas y depende de la lluvia del invierno anterior; el eclipse anular
del 6 de febrero de 2027 ocurre un solo día; la fiesta de la longaniza de Chillán se anuncia con dos
meses de aviso. Este visor pone todo eso en una línea de tiempo común, con los feriados chilenos
superpuestos, y marca dónde dos cosas buenas se pisan.

## Vistas

| Vista | Para qué |
|---|---|
| **Plan por año** | La recomendación: un viaje ancla por año más escapadas alrededor. |
| **Línea de tiempo** | Gantt de 2026 a 2030. Cada barra es una ventana; la barra con borde blanco es el peak. |
| **Calendario** | Rejilla mensual por año con feriados legales y puntos de categoría por día. |
| **Fichas** | Detalle: por qué vale la pena, logística, ventanas y fuentes. |
| **Choques de fecha** | Ventanas de prioridad alta que se solapan y obligan a elegir. |
| **Parques nacionales** | Los 46 parques publicados por Somos Parques, con región, temporada y distancia desde Temuco. |
| **Tu mapa** | Qué se leyó de la lista «Planes de viajes» de Google Maps, y qué pines quedaron sin ubicar. |

## Estructura

```
index.html            estructura y navegación
assets/styles.css     estilos
assets/app.js         carga, expansión de temporadas y render de las 6 vistas
data/eventos.json     panoramas + planes por año  ← lo que se edita normalmente
data/feriados.json    feriados legales de Chile 2026-2028
data/parques.json     parques nacionales (fuente: somosparques.cl)
```

## Agregar un panorama

Todo se edita en `data/eventos.json`. Campos mínimos:

```jsonc
{
  "id": "slug-unico",
  "nombre": "Nombre visible",
  "cat": "astro | geo | paisaje | cultural | gastro | roadtrip | fauna",
  "pais": "Chile", "zona": "Región o localidad",
  "lat": -38.7, "lon": -72.6,
  "dur": "finde | escapada | grande",
  "dias": [3, 5],
  "prio": 1,            // 1 a 5, mueve el orden y los filtros
  "certeza": "fija | movil | estimada | clima",
  "porque": "Por qué vale la pena. El fenómeno antes que el itinerario.",
  "logistica": "Cómo se llega, desde cuándo hay que reservar.",

  // una de estas dos, o ambas:
  "fechas":    [{ "ini": "2027-02-06", "fin": "2027-02-06", "tag": "etiqueta" }],
  "temporada": { "ini": "10-15", "fin": "04-15", "peak": [{ "ini": "10-20", "fin": "11-30" }], "nota": "…" },

  "alerta": "Advertencia destacada en rojo (opcional)",
  "combo":  ["otro-id"],                                    // se encadena bien con
  "mapa":   "Planes de viajes (Google Maps)",               // muestra la insignia «De tu mapa»
  "fuentes":[{ "t": "Título", "u": "https://…" }]
}
```

`temporada` usa `MM-DD` y el visor la repite cada año entre 2026 y 2030, incluso si cruza el año nuevo
(`"ini": "12-01", "fin": "03-15"` genera diciembre-2026 → marzo-2027, y así). Si un año tiene una entrada
explícita en `fechas`, ese año no se dibuja además la ventana genérica.

## Convención de certeza

No todas las fechas merecen la misma confianza, y el visor lo dice explícitamente:

- **fija** — efeméride astronómica o fecha oficial confirmada.
- **movil** — calculable desde un ciclo (Pascua, solsticio). Calculada aquí, no publicada por el organizador.
- **estimada** — se repite en la misma época todos los años, pero cada edición anuncia su fecha con pocos meses. **Verificar antes de comprar.**
- **clima** — no hay fecha, hay probabilidad: floración, nieve, espejo de agua.

## Fuentes

- Feriados legales de Chile 2026–2027: `api.boostr.cl/holidays/{año}.json`. **Los de 2028 son calculados**, no oficiales.
- Parques nacionales: [Somos Parques](https://somosparques.cl/). Entradas y reservas oficiales del SNASPE en [Pases Parques](https://www.pasesparques.cl/).
- Pines del usuario: lista «Planes de viajes» de Google Maps, leída el 2026-08-23. **Solo 20 de los 45 sitios**: Maps no carga el resto en la vista de lista compartida. Detalle en la vista «Tu mapa» y en `_meta.mapa_usuario` de `data/eventos.json`.
- Cada ficha lleva sus propias fuentes cuando las tiene.

## Desarrollo local

```bash
python -m http.server 8899
```

Luego abrir http://localhost:8899. Cualquier cambio en los JSON se ve recargando.
