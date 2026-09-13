# Traspaso: viaje Temuco, Jujuy, La Serena (25-sep al 13-oct 2026)

Este archivo lo lee `/retomar` al abrir sesion en este proyecto. Un traspaso nuevo se agrega arriba de este; el anterior baja a "Historico" al final, nunca se borra.

## Visor: revision de metodo y tres busquedas nuevas (13-sep-2026, tarde)

Nicolas pregunto por tulipanes del sur y pingüinos de Maiquillahue, y pidio revisar que le faltaba al metodo de busqueda de la sesion anterior. Hallazgo: **Maiquillahue no habria aparecido con busquedas genericas** ("kayak humedal Chile", "pingueras Chile"), porque no tiene pagina CONAF ni Ramsar; solo salio porque el pregunto por el nombre exacto. Eso reveló tres sesgos: busqueda sesgada a sitios grandes indexados, sesgada a la categoria "humedal + kayak" sin cubrir flores ni ballenas, y sin chequear primero si un lugar es realmente visitable antes de armar la ficha (casi paso con los tulipanes).

**Tulipanes de Puyehue/Osorno: quedan fuera del visor.** Es cultivo comercial de exportacion de Southern Tulips (Ruta 215, Osorno-Puyehue), sin entrada ni horario: se ve desde la berma del camino, y un articulo de Ladera Sur (2015) dice que molesta a los duenos. Las fuentes ademas se contradicen sobre el mes (sep-oct vs dic-ene). A punto de confundirlo con los tulipanes de Trevelin, Argentina (7-oct a 7-nov 2026, con entrada real): son cosas distintas, ojo si se retoma el tema.

**7 fichas nuevas de tres busquedas paralelas**, ademas de Maiquillahue (ya cargada antes):
- Cerro Nielol (copihue silvestre a pie, dentro de Temuco mismo, CONAF)
- Casa Pupuya (lavanda familiar, O'Higgins, con visita guiada real)
- Lupinos silvestres de la Carretera Austral y Ruta 9 (publico, sin operador, distinto de los tulipanes porque es flora de borde de camino, no cultivo privado)
- Golfo de Corcovado (ballena azul y delfines, Queilen, Chiloe)
- Parque Marino Francisco Coloane (ballena jorobada, Punta Arenas)
- Melinka (ballena azul con pescadores de Guaitecas, fuente de 2019, alerta de reconfirmar)
- Delfines residentes agregados a la ficha de Isla Damas (Refugio Humboldt)

**Descartado por falta de operador o vigencia dudosa**, para no repetir la busqueda: notro (sin sitio especifico), Parque Lavanda Frutillar (posible cierre), almendros en flor del Norte Chico (no existe nada parecido a una ruta del almendro), Pichidangui, Puerto Gaviota, Proyecto Travesia Valdivia-Corral, Mejillones y el Canal de Chacao (todos sin operador contactable u oferta formal).

**Publicado: commits `b136813` (Maiquillahue) y `9a40999` (los 6 restantes), push verificado contra el remoto.** El visor pasa de 103 a 110 eventos.

**Leccion de metodo para la proxima busqueda de este estilo:** buscar por nombre propio de caleta/comunidad, no solo por categoria generica; probar variantes como "muelle de los [animal]" o cooperativa de pescadores + turismo; y chequear "es esto visitable de verdad" antes de investigar temporada.

## Visor: panoramas de agua y pingueras (13-sep-2026)

Nicolas pidio mas panoramas como el humedal Monkul (kayak guiado, aves, comunidad local) y despues pingueras que no estuvieran en el visor. Se cargaron **22 fichas nuevas** en `data/eventos.json` (de 81 a 103), todas con fuentes y con el ano de cada precio.

- Araucania y Biobio: humedal Monkul, Lago Budi, Lago Lleu Lleu.
- Los Rios y Los Lagos: Rio Cruces en Valdivia (con Angachilla adentro), Chepu, Rio Maullin, Cucao y Huillinco, Reloncavi.
- Aysen y Magallanes: Raul Marin Balmaceda, Puyuhuapi, Tortel, fiordo Eberhard, canal Beagle.
- Norte y centro: Laguna de Cahuil, Laguna Grande de San Pedro, Bahia Inglesa, Arica.
- Pingueras: Punihuil, Isla Damas, Isla Magdalena, Pinguino Rey, Isla Cachagua.

Verificado en el servidor local: las 22 cargan, todas generan ventanas, cero combos rotos, sin errores de consola, y el peak que cruza el ano (Pinguino Rey, dic-ene) se dibuja bien.

**Publicado el 13-sep-2026** (commit 55b3941, push verificado contra el remoto). El visor en GitHub Pages ya muestra los 103 panoramas.

**Se agrego ademas una pestana "Mapa"**: vista geografica con Leaflet y tiles de OpenStreetMap, con los mismos filtros de categoria/duracion/pais que el resto del visor. Cada pin muestra la distancia en linea recta (no de ruta) desde Temuco y un enlace a la ficha completa. Verificado en el servidor local: los 103 eventos con coordenadas cargan como pines, sin errores de consola.

**Dejadas fuera a proposito, por falta de oferta verificada:** Queule, El Yali, Laguna Torca, Itata, Laguna Avendano, Tubul-Raqui (humedal lafkenche, vigilar @humedal_tubulraqui), Puerto Cisnes, Navegacion Ancestral de Neltume (sin rastro despues de 2020), Islotes Tuckers (solo en crucero, desde USD 1.955). Isla Chanaral y Parque Ahuenco quedaron como dato dentro de las fichas de Isla Damas y Chepu.

**Temporadas:** donde ninguna fuente publica temporada (Monkul, Bahia Inglesa, Arica, Laguna Grande, Cachagua) la ficha se marco todo el ano y la nota lo dice explicitamente. No son datos: hay que confirmar al reservar.

## Traspaso vigente (10-sep-2026)

### Que cambio hoy

1. **El regreso se corrio del lunes 12 al martes 13 de octubre.** Nicolas pidio dia administrativo, entra a trabajar el 15. Todo lo investigado antes sobre horarios y precios del "lunes 12" queda como referencia, no como dato vigente: falta reverificar para el martes 13.
2. **Decidido: cruzan a Argentina en auto propio arrendado.** Se descarto la alternativa de bus en Chile + auto en Argentina (que un excel de una amiga, Constanza, cotizaba casi al mismo precio pero sin el riesgo del cruce).
3. **Se hizo la comparacion completa MITTA vs AVIS** para el auto que cruza a Jujuy. Resultado, sin poder cerrar todavia porque faltan dos llamadas:

| | MITTA (Clase C3, Kia Sonet) | AVIS (Peugeot 2008 Crossover) |
|---|---|---|
| Precio publico, 8 dias | $345.100 | $291.466 |
| Con 35% Santander (visto, no confirmado) | ~$251.359 estimado | no aplica, Santander no tiene convenio con AVIS |
| Deducible por choque | $0 (CDW incluido) | $486.000 (10 UF+IVA) |
| Deducible vuelco/robo | $0 | $1.459.000 (30 UF+IVA) |
| Garantia/cargo por cruzar | USD 2.000, se devuelve si vuelven a tiempo (confirmado por escrito) | $120.000, probablemente NO se devuelve (inferido del lenguaje del contrato, no confirmado literal) |
| Soporte en Argentina | Ninguno (sin sucursales, textual en sus terminos) | Oficinas en Jujuy y Salta |
| Autoriza manejar en ripio (Hornocal, Cusi Cusi) | No confirmado | No confirmado |

Ambos artefactos con el detalle completo:
- Itinerario del viaje: https://claude.ai/code/artifact/93a1e591-ac3b-460f-b1db-f434cdb1216c
- Comparacion para mandar a los amigos: https://claude.ai/code/artifact/47805acc-55fb-4d9b-a622-5b3524ae509b

### Pendiente, en orden

1. **Nicolas llama a MITTA** (800 370 111 o +56 2 2360 8666): el % de descuento real y sobre que monto se aplica, el deducible del CDW en la Clase C3 especifica, si autorizan manejar en ripio para Hornocal y Cusi Cusi y con que categoria de auto, si el permiso incluye la Carta Verde/RCI, si hay retiro en Calama centro o solo aeropuerto.
2. **Los amigos preguntan a AVIS** (crossborder@avisbudget.cl): si el cargo de $120.000 se devuelve, si incluye la Carta Verde/RCI, si autorizan ripio, si cobran algo extra si el paso cierra estando ellos ya en Argentina.
3. Con esas dos respuestas, **decidir MITTA o AVIS**.
4. Comprar el vuelo CJC-LSC del domingo 4 de octubre (cotizado ~16:55-18:32, LA395). **Estado sin confirmar**: Nicolas dijo el 10-sep que los pasajes ya estaban listos, pero solo confirmo explicitamente el del martes 13. Preguntar antes de comprar nada.
5. ~~Comprar el vuelo de vuelta del martes 13~~ **COMPRADO** (confirmado por Nicolas el 10-sep). Falta registrar aca el horario, el numero de vuelo y el precio: no los tengo, se compraron fuera de esta sesion. Mientras no esten escritos, el itinerario publicado y `data/eventos.json` siguen mostrando el regreso viejo del lunes 12.
6. Confirmar el salon Pacific Club de La Serena para el dia del regreso (deberia aplicar igual un martes: horario 08:00-21:00, o hasta 1,5 h antes del primer vuelo).
7. Reservar alojamiento: Calama noches del 25 de sep y del 3 de oct; Huasco para el Desierto Florido (8, 9 y 10 de oct).

### Estado de compra de los tres tramos (al 10-sep-2026)

| Tramo | Estado | Detalle |
|---|---|---|
| ZCO-CJC, viernes 25 sep | **COMPRADO** | LA22 ZCO 08:06 a SCL 09:32, escala de 3 h 23 elegida a proposito por el salon (no la de 2 h 07), LA370 SCL 12:55 a CJC 15:07 |
| CJC-LSC, domingo 4 oct | Sin confirmar | Cotizado ~16:55-18:32, LA395 |
| Regreso, martes 13 oct | **COMPRADO** | Horario, vuelo y precio pendientes de registrar |

### Prompt para abrir la proxima sesion

```
Retomamos el viaje a Jujuy. El vuelo de vuelta del martes 13 ya esta comprado:
pideme los datos si todavia no estan en docs/PROXIMA-SESION.md. Sigue con las dos
llamadas a MITTA y AVIS y con la decision de cual auto arrendar. Y ojo: el
itinerario publicado y data/eventos.json todavia muestran el regreso del lunes 12.
```

## Historico

(vacio: este es el primer traspaso de este proyecto)
