Title: NeoWs, SPK-ID and parsing (SOCIS 2017)
Date: 2017-07-31 22:30
Category: SOCIS
Tags: SOCIS, poliastro, NASA, NeoWs, APIs, HTML, parsing
slug: 2017-07-31-neows-spk-id-and-parsing-socis
lang: en
Author: Antonio Hidalgo Galindo

In the previous entry, several different APIs related to NEOs were studied, and finally [NeoWs](https://api.nasa.gov/neo/?api_key=DEMO_KEY) was chosen to start working with.

This week, we aimed to start with coding itself, adding an `orbit_from_spk_id` function to newly created `poliastro.neos module`.

In order to achieve this, the first step was researching how NeoWs API exactly works.

## NeoWs operation
As stated in the prevoius article of this "series", this API provides several different functionalities, but, for the moment, we were only interested in the lookup service.

It also counts with web documentation, which was a really good start point, as you can see:

![NeoWs Documentation]({filename}/images/neows_lookup.png "NeoWs Documentation")

When using the lookup service (and any NASA API) you need an `API key`, but we used `DEMO_KEY`, which only limits your queries to 40 per hour. Having that in mind, all you need to do is a query with a body SPK-ID (we will explain this number later), and, if all goes well, the API will answer your query with a JSON response, containing the following data:

* Body information

    * Name, ID, hazard, ...

    * Orbital data

* Next close approachs


Of course, we were mainly interested in orbital data. But, what would mean "orbital data"? A simple query using [Eros asteroid](https://en.wikipedia.org/wiki/433_Eros) SPK-ID, gave us the following:

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
Not bad at all!

If you are familiar with astrophysics, you will probably know about classical orbital elements. If you are more a computer scientist than an astrophysicist, [classical orbital elements](https://en.wikipedia.org/wiki/Orbital_elements#Keplerian_elements) are just six parameters which determine orbit and body position in that orbit at a given time.

There are several ways to create an [Orbit](https://poliastro.readthedocs.io/en/latest/api.html#module-poliastro.twobody.orbit.Orbit) object in poliastro, but it seemed that we had all the necessary parameters to create one with [from_classical() function](https://poliastro.readthedocs.io/en/latest/api.html#module-poliastro.twobody.orbit.Orbit.from_classical).

So, after retrieving API information, we were ready to start coding :)

## orbit_from_spk_id()

Since you can see the `neos module` code on [Github](https://github.com/poliastro/poliastro/blob/master/src/poliastro/neos.py), I won't write much about it here.

We decided to use [Requests library](http://docs.python-requests.org/en/master/), which is really easy and has its own JSON parser.

The function created is really simple:

1. First, a GET request is send with SPK-ID as a parameter.

2. If there is a 4xx or 5xx error, it raises an exception.

3. Else, it parses classical orbital elements, which are used then to

4. create and return an Orbit object.

After that, we were able to create such a beautiful code :P :

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

which produces:

![Apophis Orbit]({filename}/images/apophis.png "Apophis Orbit")

The function was coded and it worked, but there were still some problems.

As I said in the previous entry, `NeoWs` has pros (that's why we decided to use it), but also has some cons, and one of them is that it only allows to browse by SPK-ID number.

## SPK-ID and orbit_from_name()

SPK-ID (do not confuse with IAU number) is a number that [JPL](https://www.jpl.nasa.gov/) uses to catalog small-bodies in their database, so it isn't easy to find unless you search in [JPL Small-bodies Database](https://ssd.jpl.nasa.gov/sbdb.cgi).

Having to use internet in order to find every SPK-ID would be really boring, so the next logical step was coding a function that, given a name, searched the corresponding SPK-ID. Combining this function with the previously written, `orbit_from_name` function would be trivial.

As I said, the only way that we had to find SPK-IDs was using JPL Small-bodies Database, but it doesn't provide machine-readable data (web interface isn't really modern either, as you can see), so a HTML parser was needed.

![SBDB interface]({filename}/images/sbdb_interface.png "SBDB interface")

We wrote an `name_from_spk_id()` function that basically makes a GET request to SBDB with a string. After that, there are three options:

* If an object exists with that name, SPK-ID is parsed and returned.

* If there are several objects that matches the query, an exception is raised with the list of those objects, and function return `None`.

* If no objects were found, an exception is raised and function return `None`.

Again, code is available on [Github](https://github.com/poliastro/poliastro/blob/master/src/poliastro/neos.py).

Modules with HTML parsing in them are usually ugly, and this one is no exception, but it works, so currently you can get a NEO orbit (only NEAs at the moment, but it's equally great) by name or IAU number.

Next days, we will probably take a close look at some JPL offline databases we found yesterday, so we don't know if we'll continue with the same code or we'll change radically. That means that next week entry topic will be completly unknown until then ;) See you!