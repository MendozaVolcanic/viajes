# Traspaso: viaje Temuco, Jujuy, La Serena (25-sep al 13-oct 2026)

Este archivo lo lee `/retomar` al abrir sesion en este proyecto. Un traspaso nuevo se agrega arriba de este; el anterior baja a "Historico" al final, nunca se borra.

## Visor: panoramas de agua y pingueras (13-sep-2026)

Nicolas pidio mas panoramas como el humedal Monkul (kayak guiado, aves, comunidad local) y despues pingueras que no estuvieran en el visor. Se cargaron **22 fichas nuevas** en `data/eventos.json` (de 81 a 103), todas con fuentes y con el ano de cada precio.

- Araucania y Biobio: humedal Monkul, Lago Budi, Lago Lleu Lleu.
- Los Rios y Los Lagos: Rio Cruces en Valdivia (con Angachilla adentro), Chepu, Rio Maullin, Cucao y Huillinco, Reloncavi.
- Aysen y Magallanes: Raul Marin Balmaceda, Puyuhuapi, Tortel, fiordo Eberhard, canal Beagle.
- Norte y centro: Laguna de Cahuil, Laguna Grande de San Pedro, Bahia Inglesa, Arica.
- Pingueras: Punihuil, Isla Damas, Isla Magdalena, Pinguino Rey, Isla Cachagua.

Verificado en el servidor local: las 22 cargan, todas generan ventanas, cero combos rotos, sin errores de consola, y el peak que cruza el ano (Pinguino Rey, dic-ene) se dibuja bien.

**Sin publicar.** Los cambios no estan commiteados: subirlos publica el visor en GitHub Pages. Decision de Nicolas.

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
