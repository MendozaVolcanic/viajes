# Traspaso: viaje Temuco, Jujuy, La Serena (25-sep al 13-oct 2026)

Este archivo lo lee `/retomar` al abrir sesion en este proyecto. Un traspaso nuevo se agrega arriba de este; el anterior baja a "Historico" al final, nunca se borra.

## 0. Traspaso vigente (25-sep-2026)

Estado fijado **sin trabajo en curso**: los siete subagentes de la sesion terminaron y reportaron, no hay servidor local ni procesos corriendo (`netstat` sin nada en el puerto 8899) y no hay ramas sin integrar. Sesion "plan viajes v2", abierta el 10-sep. El viaje parte el viernes 25-sep.

Los guiones, preguntas y tablas que solo vivian en la conversacion quedaron en `C:\Users\nmend\OneDrive\Escritorio\claude\Personal\Viajes\docs\GUIONES-Y-CHECKLIST.md`. **Ese archivo es solo local: esta en `.gitignore` porque el repo es publico y trae detalle de tarjeta y finanzas; lo respalda OneDrive.** Leerlo antes de responder cualquier pregunta sobre auto, plata, salon, baterias o dron.

### a. Todo en una pantalla

| Item | Estado | Evidencia |
|---|---|---|
| Visor publicado (111 panoramas) | Terminado | `git ls-remote origin -h refs/heads/main` igual a `git rev-parse HEAD` en el commit `7443695`. Pages `built` 2026-09-13T19:51:09Z. Repo PUBLICO. https://mendozavolcanic.github.io/viajes/ |
| Pestana "Mapa" (Leaflet + OpenStreetMap) | Terminado | Verificado en local el 13-sep con 103 pines. Los 8 panoramas posteriores pasaron el validador (lat y lon obligatorias) pero no se recontaron los pines |
| Temporada vs Peak en las fichas | Terminado | `winRow` y `WIN_HELP` en `assets/app.js`; verificado con Pinguino Rey (filas "Ventana completa" y "Mejor momento (peak)") |
| Guiones largos y medios en UI, README y app.js | Terminado | El conteo con `grep -c` da 0 en `assets/app.js`, `index.html` y `README.md` |
| Guiones largos dentro de `data/eventos.json` | **A medias, no tocado** | El conteo con `grep -c` del guion largo (U+2014) da 56 lineas, medido hoy |
| Lista "En el radar" (7 pistas sin operador) | Terminado | `_meta.seguimiento` en `data/eventos.json`, visible en la pestana "Como se usa" |
| Ida vie 25-sep (LA22 ZCO 08:06, LA370 SCL 12:55) | Comprado | Memoria del proyecto, seccion "Estado de compra" |
| CJC-LSC dom 4-oct | **Sin confirmar** | Nicolas solo confirmo explicitamente el del martes 13 |
| Regreso mar 13-oct | Comprado, **sin datos registrados** | Falta horario, vuelo y precio |
| Auto (MITTA C4 contra AVIS) | **SIN DECIDIR** | Ver decision 1. Retiro previsto sab 26-sep 10:00, Calama aeropuerto |
| Alojamiento Calama (25-sep y 3-oct) y Huasco (8 a 11-oct) | **Sin registro de reserva** | Nada en el repo ni en la memoria |
| Artefactos publicados (itinerario `93a1e591`, comparacion `47805acc`) | **DESACTUALIZADOS** | `Artifact list` del 10-sep los daba actualizados el 2026-09-08 y no se republicaron; contienen MasterRental, "deducible $0" y regreso del lunes 12, todo falso o viejo |
| Remote Control | **Encendido** | Verificado con las herramientas de la app; el detalle vive en la memoria privada del proyecto, no en este repo publico |
| Git | `main` unica, sin stash | `git branch -a` solo muestra `main` y `origin/main` |

**Remote Control, para que siga funcionando:** no crear en esta carpeta un `.claude/settings.json` con `remoteControlAtStartup: false`. Las condiciones operativas estan en la memoria privada del proyecto.

### b. Decisiones que espera el dueño

| # | Pregunta | Opciones | Recomendacion |
|---|---|---|---|
| 1 | ¿Que auto arriendan? (urgente: retiro sab 26-sep 10:00) | MITTA C4 ($462.947 con 35% Santander, sin neumaticos ni asistencia en Argentina, robo 50 UF) o AVIS con pack Total ($531.386, deducible cero, neumaticos y asistencia en Jujuy y Salta) | **AVIS pack Total** si hay ripio (Hornocal, Cusi Cusi) o quieren asistencia; la diferencia es de unos $68.000, unos $23.000 por persona entre tres. MITTA solo con respuesta escrita de Raul sobre deducible de choque en pesos, ripio y validez de la responsabilidad civil en Argentina |
| 2 | ¿Limpian los 56 guiones largos de `data/eventos.json`? | Ahora, en la proxima sesion, o dejarlos | **Proxima sesion, en una pasada dedicada** con el diff revisado: es tu regla global, es texto del visor publico, y hacerlo a mano en 56 lineas tiene riesgo de romper frases |
| 3 | ¿Republican los dos artefactos con las correcciones? | Si, solo la comparacion, o dejarlos | **Si, primero la comparacion** (es lo que leen los amigos) y despues el itinerario, en la misma URL, leyendo el HTML completo antes |
| 4 | ¿Reescriben la logistica del Desierto Florido en `eventos.json`? | Reescribir, o dejar | **Reescribir** cuando esten los datos del vuelo del 13: hoy habla de "dos pedidos" y de regreso el lunes 12, y ahora esta de vacaciones del 25-sep al 13-oct |

### c. Lo aprendido

**Reglas generales del workspace** (propuestas para el `CLAUDE.md` global, no editado por esta sesion):
1. **No arrastrar como hecho lo que esta escrito en otro documento o sesion sin abrir la fuente.** Asi entraron al itinerario publicado una "autorizacion de ripio" (producto no comprobado), MasterRental (no existe para una Visa) y un "deducible $0" que la ficha real desmentia. Quedo como `feedback_no_arrastrar_hechos_no_verificados.md`.
2. **Cuando dos cosas se parecen, comprobar pais y moneda de la fuente** antes de citar una fecha o un precio: casi se mezclan los tulipanes de Puyehue con los de Trevelin (Argentina).
3. **Antes de armar la ficha de un lugar, preguntar si se puede visitar de verdad**, y solo despues investigar la temporada.
4. Las paginas de Santander, LATAM y AFIP dan 403 a WebFetch: usar resumenes de busqueda **marcados como tales**, o pedir la captura.

**Propias del proyecto** (viven en `project_visor_viajes.md`):
5. Buscar por **nombre propio de caleta o comunidad** ("muelle de los pinguinos", cooperativa de pescadores mas turismo), no por categoria generica: los sitios comunitarios no aparecen en CONAF ni Ramsar (asi se encontro Maiquillahue).
6. Sin operador contactable no es un panorama: va a `_meta.seguimiento`.
7. Si ninguna fuente publica temporada, la ficha va todo el ano con una nota que lo dice.
8. Leaflet en pestanas `display:none`: inicializar al primer clic y llamar `invalidateSize()`.
9. La regla de guiones vale tambien para el texto de la interfaz, el README y los tooltips, no solo para los informes.

### d. Problemas abiertos e hipotesis

| Etiqueta | Afirmacion |
|---|---|
| **CONFIRMADO** | 56 lineas con guion largo en `data/eventos.json` (conteo con `grep -c`, hoy) |
| **CONFIRMADO** | La logistica del Desierto Florido en `eventos.json` todavia dice "dos pedidos" y "lunes 12" (comprobado hoy) |
| **CONFIRMADO** | Remote Control encendido y activo por defecto para las sesiones nuevas (herramientas de la app) |
| **CONFIRMADO** | Las paginas oficiales de Santander, LATAM y ARCA dieron 403 en esta sesion |
| **SOSPECHA** | El permiso de cruce a Argentina no se pidio a tiempo: MITTA exige 72 horas habiles y el retiro es el sab 26 a las 10:00. No hay registro de que se haya pedido |
| **SOSPECHA** | Los alojamientos de Calama y Huasco no estan reservados (sin registro) |
| **SOSPECHA** | La WorldMember Limited no cobra comision por compras afuera (Wise, marzo de 2024, fuente secundaria) |
| **SOSPECHA** | La temporada de Maiquillahue (sep a mar) es inferida por analogia con Punihuil |
| **SOSPECHA** | UF ~$40.840 y USD/CLP 961,73 son cifras no verificadas abriendo la fuente; el Paso de Jama podria no estar habilitado para Tax Free |

### e. Cerrado, no rehacer

- **Tulipanes de Puyehue y Osorno: fuera del visor** (cultivo privado, sin acceso). No confundir con Trevelin.
- **El dolar blue no rinde** (brecha 1,3% el 21-sep): no volver a compararlo como opcion principal. Western Union solo si la app muestra mas de 1,59 ARS por CLP.
- **MasterRental no aplica** (tarjeta Visa). El seguro de arriendo hay que resolverlo con la rentadora.
- Cruzan en **auto arrendado**, no bus mas auto argentino: sigue vigente.
- Notro, lavanda de Frutillar, almendros, Pichidangui, Puerto Gaviota, Proyecto Travesia, Mejillones y Canal de Chacao: **en el radar**, no repetir la busqueda hasta que aparezca una pista nueva.
- Pestana Mapa, explicacion Temporada/Peak, limpieza de guiones en UI y README: hechas y publicadas.
- Salon de Temuco: horario, llamada y tabla horaria ya documentados en `GUIONES-Y-CHECKLIST.md`.

### f. Prompt para la proxima sesion

```
Retomamos el viaje a Jujuy y el visor de panoramas (proyecto en
C:\Users\nmend\OneDrive\Escritorio\claude\Personal\Viajes). Usa /retomar.

Antes de creerle a nada, verifica el estado real:
1. git status -sb y git log --oneline -8 en esa carpeta, y compara
   git rev-parse HEAD con git ls-remote origin -h refs/heads/main.
2. gh api repos/MendozaVolcanic/viajes/pages/builds/latest (que el sitio haya
   construido el ultimo commit).
3. Pregunta a Nicolas en que punto del viaje va (salio el 25-sep de Temuco,
   vuelve el martes 13-oct): que auto arriendan, que respondieron MITTA y AVIS,
   si llego a Calama, y si reservo alojamiento. No lo des por hecho.

Lee en este orden: docs/PROXIMA-SESION.md (bloque 0), docs/GUIONES-Y-CHECKLIST.md (solo local),
y la memoria project_viaje_jujuy_octubre_2026.md, project_visor_viajes.md y
feedback_no_arrastrar_hechos_no_verificados.md.

Trabajo en este orden (prioriza 1 y 2 si la sesion es corta o desde el celular):
1. Cerrar la decision del auto con lo que responda Nicolas (decision 1 del traspaso).
2. Republicar el artefacto de comparacion 47805acc y despues el itinerario
   93a1e591 (misma URL, leyendo el HTML completo antes). Correcciones: MasterRental
   no aplica a una Visa, el deducible de MITTA no es $0 (robo 50 UF, sin
   neumaticos, sin asistencia en Argentina), no existe una "autorizacion de ripio"
   comprobada (se pregunta por la restriccion), total MITTA $462.947, totales AVIS,
   y el regreso es el martes 13.
3. Registrar el horario, vuelo y precio del regreso del 13 y del CJC-LSC del 4;
   reescribir la logistica del Desierto Florido en data/eventos.json.
4. Limpiar los 56 guiones largos de data/eventos.json con el diff revisado.
   Comprobar con grep que no queden los caracteres U+2014 ni U+2013.
5. Revisar _meta.seguimiento y agregar como panorama solo lo que consiga operador.
6. /cierre.

Reglas duras: nunca guiones largos ni medios; espanol de Chile con formas de tu;
ningun precio, fecha ni temporada sin fuente abierta y ano; una ficha nueva solo con
operador contactable; git add por archivo, nunca -A; rutas absolutas completas;
cotizar con link; la tarjeta de Nicolas es Visa, no Mastercard; no crear
.claude/settings.json con remoteControlAtStartup false en esta carpeta.

Si la sesion no alcanza: hacer /cierre con lo que quedo y dejar escrito en el
traspaso que puntos de la lista 1 a 6 no se tocaron.
```

## 1-prev. Plata para Argentina (21-sep-2026)

Nicolas pregunto como maximizar el poder adquisitivo en el viaje (tarjeta, dolar blue, etc.). Respuesta: **con la brecha blue oficial en 1,3% el blue no rinde**; la plata esta en el IVA del alojamiento (se quita al pagar con tarjeta del exterior), en la comision de la tarjeta y en no retirar de cajeros. Detalle, cifras y fuentes en la memoria del proyecto (`project_viaje_jujuy_octubre_2026.md`, seccion "Dinero en Argentina").

Western Union no se recomienda salvo que la app muestre mas de ~1,59 ARS por cada CLP enviado con todo incluido; el blue en Jujuy compra a 1.516, peor que la tarjeta.

Pendiente antes de salir el 25-sep:
1. Llamar a Santander (600 320 3000): confirmar comision 0 por compras en el extranjero con la WorldMember Limited, avisar el viaje, revisar cupo internacional, y saber si su debito cobra los USD 8 por giro.
2. Preguntar a cada alojamiento si aplica la exencion de IVA a turista extranjero pagando con tarjeta, y llevar cedula o pasaporte.
3. Retirar pesos una sola vez, en San Salvador de Jujuy, y pagar todo lo demas con la tarjeta, siempre en pesos argentinos.
4. Registrar el dron en ANAC antes de cruzar (declaracion jurada digital gratuita), no volarlo sobre parques ni areas protegidas, llevar todas las baterias en cabina con terminales protegidos, y preguntar a Santander cuantos de los 12 accesos Pacific Club lleva usados y desde cuando corre el ano.

## 2-prev. Visor: revision de metodo y tres busquedas nuevas (13-sep-2026, tarde)

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

## 3-prev. Visor: panoramas de agua y pingueras (13-sep-2026)

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

## 4-prev. Traspaso (10-sep-2026), degradado a historico el 25-sep-2026

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

Actualizacion del 25-sep-2026: los bloques `1-prev` a `4-prev` de arriba son el historico de esta sesion. Nada se borro; el `0` es el vigente.
