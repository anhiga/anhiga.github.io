Title: NeoWs, SPK-ID y parsing (SOCIS 2017)
Date: 2017-07-31 22:30
Category: SOCIS
Tags: SOCIS, poliastro, NASA, NeoWs, APIs, HTML, parsing
slug: 2017-07-31-neows-spk-id-and-parsing-socis
lang: es
Author: Antonio Hidalgo Galindo

En la anterior entrada, estudiamos diferentes APIs relacionadas con NEOs, y finalmente elegimos [NeoWs](https://api.nasa.gov/neo/?api_key=DEMO_KEY) para empezar a trabajar.

Esta semana, nuestro objetivo era empezar con la propia programación, añadiendo una función de la forma `orbit_from_spk_id` al nuevo módulo `poliastro.neos`.

Para conseguir esto, el primer paso era investigar el funcionamiento exacto de la API NeoWs.

## Funcionamiento de NeoWs
En la anterior entrada de esta "serie", ya dijimos que esta API proporciona varias funcionalidades distintas, pero, por el momento, solo nos interesaba el servicio de búsqueda.

Además, también proporciona una documentación web, que es un buen sitio para empezar, como se puede ver:

![NeoWs Documentation]({filename}/images/neows_lookup.png "NeoWs Documentation")

Al usar el servicio de búsqueda (y cualquier otra API de la NASA), necesitas una `API key`, pero nosotro usamos `DEMO_KEY`, que únicamente límita las peticiones a 40 por hora. Con esto en mente, lo único que necesitas es hacer una petición con un SPK-ID (explicaremos este número después) y, si todo va bien, la API responderá con datos en formato JSON, que contienen la siguiente información:

* Información sobre el cuerpo

    * Nombre, ID, peligrosidad, ...

    * Datos orbitales

* Próximas aproximaciones

Nostros sólo estábamos interesados en los datos orbitales. Pero, ¿que querría decir exáctamente "datos orbitales"? Una simple petición usando el SPK-ID del asteroide [Eros](https://es.wikipedia.org/wiki/433_Eros) nos dio lo siguiente:

```JSON
'orbital_data': {
        'orbit_id': '611',
        'orbit_determination_date': '2017-06-06 06:20:43',
        'orbit_uncertainty': '0',
        'minimum_orbit_intersection': '.150505',
        'jupiter_tisserand_invariant': '4.583',
        'epoch_osculation': '2458000.5',
        'eccentricity': '.2225889698301071',
        'semi_major_axis': '1.457940027185708',
        'inclination': '10.82759100494802',
        'ascending_node_longitude': '304.3221633898424',
        'orbital_period': '642.9954742523677',
        'perihelion_distance': '1.133418658460363',
        'perihelion_argument': '178.8165910886752',
        'aphelion_distance': '1.782461395911054',
        'perihelion_time': '2457873.186399333365',
        'mean_anomaly': '71.28027812836476',
        'mean_motion': '.5598795239089109',
        'equinox': 'J2000'
    }
```
No está mal!

Si estás familiarizado con la astrofísica, probablemente sabrás lo que son los elementos orbitales keplerianos. Si eres más informático que astrofísico, los [elementos orbitales keplerianos](https://es.wikipedia.org/wiki/Elementos_orbitales) son simplemente seis parámetros que permiten determinar completamente una orbita y la posición del cuerpo en ella en cierto instante.

En poliastro hay varias formas de crear un objecto [Orbit](https://poliastro.readthedocs.io/en/latest/api.html#module-poliastro.twobody.orbit.Orbit), pero parecía que teníamos todos los parámetros necesarios para crear uno usando la función [from_classical()](https://poliastro.readthedocs.io/en/latest/api.html#module-poliastro.twobody.orbit.Orbit.from_classical).

Así que, después de recabar información sobre la API, ya estábamos listo para empezar a programar :)

## orbit_from_spk_id()

Ya que el código del módulo `neos.py` está disponible en [Github](https://github.com/poliastro/poliastro/blob/master/src/poliastro/neos.py), no hablaré demasiado sobre ello en esta entrada.

Para la parte de peticiones a internet, decidimos usar la librería [Requests](http://docs.python-requests.org/en/master/), bastante sencilla y además con su propio parser de JSON.

La función que creamos es muy simple:

1. Primero se envía una petición GET con un número SPK-ID como parámetro.

2. Si hay un error 4xx o 5xx, se produce una excepción.

3. Si no, se parsean los elementos orbitales, que se usan para

4. crear y devolver un objeto Orbit.

Con esta función fuimos capaces de crear este código tan bonito :P :

```python
from poliastro import neos
from poliastro.bodies import Earth
from poliastro.twobody.orbit import Orbit
from poliastro.plotting import OrbitPlotter

op = OrbitPlotter()

apophis_orbit = neos.orbit_from_spk_id('2099942') #Apophis SPK-ID
earth_orbit =  Orbit.from_body_ephem(Earth)

op.plot(earth_orbit, label='Earth')
op.plot(apophis_orbit, label='Apophis')
```

que produce:

![Apophis Orbit]({filename}/images/apophis.png "Apophis Orbit")

La función hacía su trabajo, pero aún había algunos problemas.

Como dije en la anterior entrada, `NeoWs` tiene ventajas (por eso decidimos usarla), pero también algunas desventajas, y una de ellas es que sólo permite buscar por número SPK-ID.

## SPK-ID y orbit_from_name()

El SPK-ID (con confundir con el número IAU) es un número que el [JPL](https://www.jpl.nasa.gov/) utiliza para catalogar los cuerpos menores en su base de datos, y por eso no es fácil de encontrar a no ser que busques en la [base de datos de cuerpos menores del JPL](https://ssd.jpl.nasa.gov/sbdb.cgi).

Tener que usar internet para encontrar cada SPK-ID sería bastante aburrido, así que el paso más lógico para nosotros era escribir una función que, dado un nombre, encontrase el correspondiente SPK-ID. Combinando esta función y la escrita anteriormente, la siguiente función `orbit_from_name` sería trivial.

Como ya he dicho, la única manera de encontrar el SPK-ID de un cuerpo es usar la base de datos del JPL, pero desgraciadamente no proporciona datos en formato máquina (la interfaz web tampoco es demsiado moderna, como se puede ver) así que necesitabamos un parser HTML.

![SBDB interface]({filename}/images/sbdb_interface.png "SBDB interface")

Escribimos una función `name_from_spk_id()` que básicamente hace una petición GET a la página con una cadena (nombre) como parámetro. Tras eso, pueden pasar tres cosas:

* Si hay un objeto con ese nombre, se parsea y se devuelve el SPK-ID.

* Si hay varios objetos con ese nombre, se produce una excepción con la lista de objetos, y se devuelve `None` en la función.

* Si no se encuentra ningún objeto, se produce una excepción y la función devuelve `None`.

El código también está disponible en [Github](https://github.com/poliastro/poliastro/blob/master/src/poliastro/neos.py).

Las funciones que parsean HTML suelen ser feas, y ésta no es una excepción, pero funciona, así que ahora mismo puedes conseguir la órbita de un NEO (en realidad sólo de NEAs de momento, pero sigue estando bien) por nombre o número IAU.

En los próximos días probablemente analizaremos en profundidad algunas bases de datos offline del JPL que encontramos ayer, así que no sabemos si continuaremos programando en esta línea o cambiaremos radicalmente. Eso significa que el tema de la entrada de la semana que viene será un misterio hasta entonces ;) Nos vemos!