Title: APIs espaciales, JSON y REST (SOCIS 2017)
Date: 2017-07-25 14:00
Category: SOCIS
Tags: SOCIS, ESA, poliastro, NASA, APIs, open data
slug: 2017-07-25-space-apis-json-and-rest-socis
lang: es
Author: Antonio Hidalgo Galindo

Después de montar el blog, era el momento de empezar con la primera semana de mi [timeline](https://github.com/poliastro/poliastro/wiki/SOCIS-2017-Antonio-Hidalgo#timeline). La tarea de esta semana era investigar las APIs de la NASA disponibles y otras bases de datos de NEOs que pudiesen ser útiles para este proyecto.

Ya había estudiado algunas APIs y echado un vistazo a sus posibilidades, pero hacía falta una investigación más profunda. Como mi [propuesta](https://github.com/poliastro/poliastro/wiki/SOCIS-2017-Antonio-Hidalgo#proposal) se componía de 3 páginas diferentes, decidí analizar cada una por separado.

## CNEOS
En la página del [CNEOS](https://cneos.jpl.nasa.gov/orbits/) hay una lista de distintas herramientas, pero puede ser acortada a las siguientes APIs:

* [JPL Small-Body Database Browser](https://ssd.jpl.nasa.gov/sbdb.cgi): permite buscar cualquier cuerpo menor (como los NEOs) mediante su número IAU, nombre o designación, y también soporta los caracteres comodín `*` y/o `?`. Los datos disponibles incluyen, citando a la propia página:
> * elementos orbitales
> * diagramas orbitales
> * parámetros físicos
> * circunstancias sobre el descubrimiento
>
> Los nuevos objetos descubiertos y sus órbitas son añadidos de forma diaria.

* [JPL Small-Body Database Search Engine](https://ssd.jpl.nasa.gov/sbdb_query.cgi): permite generar tablas personalizadas con datos orbitales y parámetros físicos de un subconjunto de todos los asteroides y cometas. Permite una gran cantidad de restricciones de búsqueda, por ejemplo:
![Figure 1]({filename}/images/sbdb_constraints.jpg "Figure 1")

También permite seleccionar los datos de salida, y elegir entre HTML y CSV.

* [Horizons](https://ssd.jpl.nasa.gov/?horizons): proporciona acceso a efemérides de alta precisión para objetos del sistema solar, no solo cuerpos menores. Se puede acceder mediante telnet, email y una interfaz web.

## NEOWS
Entre las APIs de la NASA, está [NeoWs]https://api.nasa.gov/neo/?api_key=DEMO_KEY). Se puede utilizar para listar NEOs y obtener sus elementos orbitales y próximas aproximaciones (valga la redundancia) a la Tierra, dado un SPK-ID (número que el [JPL](https://www.jpl.nasa.gov/) usa para identificar objetos). A pesar de su nombre, sólo funciona con NEAs (Near Earth Asteroids), y por tanto no proporciona información sobre cometas.

## JPL SSD/CNEOS API SERVICE
Como dice su web, el [JPL SSD/CNEOS API SERVICE](https://ssd-api.jpl.nasa.gov/)
> proporciona una interfaz para datos en formato JSON relacionados con el [SSD](https://ssd.jpl.nasa.gov/) y el [CNEOS](https://cneos.jpl.nasa.gov/).

Las APIs más relevantes son:

* [Close-Approach Data (CAD)](https://ssd-api.jpl.nasa.gov/doc/cad.html): proporciona datos sobre aproximaciones a la tierra para todos los asteroides y cometas en la base de datos del JPL.

* [Accessible NEAs (NHATS)](https://cneos.jpl.nasa.gov/nhats/): está operado por el Near-Earth Object Human Space Flight Accessible Targets Study ([NHATS](https://cneos.jpl.nasa.gov/nhats/intro.html)), y se puede utilizar para identificar NEAs que pueden ser aptos para futuras misiones tripuladas.

* [Scout](https://ssd-api.jpl.nasa.gov/doc/scout.html): el sistema Scout propociona análisis de trayectorias y evaluación de riesgos en objetos descubiertos recientemente.

* [Sentry](https://cneos.jpl.nasa.gov/sentry/): Sentry es un sistema de monitorización de colisiones automático, que escanea continuamente el catálogo más actual de asteroides y analiza las posibilidades de un futuro impacto.

## Eligiendo las APIs
Una vez estudiadas todas las posibilidades, era momento de elegir las APIs que parecían más adecuadas para nuestro propósito.

Ya que el núcleo de `poliastro` son los objetos [Orbit](https://poliastro.readthedocs.io/en/latest/api.html#poliastro.twobody.orbit.Orbit), nuestro objetivo principal es crear automáticamente las órbitas de los NEOs, usando los datos obtenidos de APIs de internet. Para conseguir esto, se necesitan o bien los elementos orbitales o bien los vectores de posición y velocidad, así que el primer requisito que tenían que cumplir las APIs, era proporcionar alguno de estos datos.

Por tanto, varias APIs podían ser descartadas por no proporcionar la información necesaria: `Accesible NEAs`, `Scout`, `Sentry` y `Close-Approach Data`.

Ya que preferíamos no tener que lidiar con intrincadas peticiones POST, otro requisito importante que las APIs tenían que cumplir era proporcionar una buena interfaz (la "I" de API significa interfaz, así que...), y, a ser posible, algo que se acercase a un [Servicio REST](https://es.wikipedia.org/wiki/Transferencia_de_Estado_Representacional).

`JPL Small-Body Database Search Engine` requiere peticiones POST de más de 150 líneas, así que la descartamos automáticamente.

Finalmente, el tercer requisito, considerando que escribimos software en Python, era que la información fuese proporcionada `machine-readable` (en formato fácil de leer y manipular para el ordenador), siendo JSON el formato preferido, y un código HTML mal escrito el peor formato.

Tanto `JPL Small-Body Database Browser` como `Horizons` proporcionan la salida en HTML, el cual tiene que ser parseado, con todos los riesgos que ésto implica, por lo que fueron descartados.

Para clarificar toda esta la retahíla de datos, hice una tabla:


|                  API                  | Elementos orbitales? | REST? | Machine-readable? |              Otras              |
|:-------------------------------------:|:--------------------:|:-----:|:-----------------:|:-------------------------------:|
|    JPL Small-Body Database Browser    |          Sí          |   Sí  |         No        |       No se limita a NEOs       |
| JPL Small-Body Database Search Engine |          Sí          |   No  |      Sí (CSV)     |       No se limita a NEOs       |
|                Horizons               |          Sí          |   No  |         No        | [ya existe una interfaz Python] |
|                 NeoWs                 |          Sí          |   Sí  |     Sí (JSON)     |   Solo para NEAs (asteroides)   |
|       Close-Approach Data (CAD)       |          No          |   Sí  |     Sí (JSON)     |                                 |
|        Accessible NEAs (NHATS)        |          No          |   Sí  |     Sí (JSON)     |                                 |
|                 Scout                 |          No          |   Sí  |     Sí (JSON)     |                                 |
|                 Sentry                |          No          |   Sí  |     Sí (JSON)     |                                 |
[ya existe una interfaz Python]: https://github.com/mommermi/callhorizons

Teniendo todos estos requisitos en mente, la mejor opción parecía ser `NeoWs`. Aunque no proporciona información sobre NECs (cometas), éstos solo representan un 0.7% del total de los NEOs, por tanto podían ser descartados (sólo de momento :P). Otro problema relacionado con `NeoWs` es el hecho de que sólo permite buscar por número SPK-ID (no confundir con número IAU), el cuál es desconocido para la mayoría de la gente, por tanto, antes de hacer ninguna petición a la API, se necesita encontrar el número SPK-ID.

Y eso ha sido todo esta semana. La próxima, empezaremos con la programación propiamente dicha, añadiendo una función `orbit_from_spk_id` que haga una petición a la API `NeoWs` ¡Nos vemos!