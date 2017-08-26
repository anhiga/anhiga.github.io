Title: Space APIs, JSON and REST (SOCIS 2017)
Date: 2017-07-25 14:00
Category: SOCIS
Tags: SOCIS, ESA, poliastro, NASA, APIs, open data
slug: 2017-07-25-space-apis-json-and-rest-socis
lang: en
Author: Antonio Hidalgo Galindo

After setting up the blog, it was time to start with the first week of my [timeline](https://github.com/poliastro/poliastro/wiki/SOCIS-2017-Antonio-Hidalgo#timeline). The task for this week was to research the available NASA Open APIs and other NEOs databases that could better fit for this project.

I had already studied some APIs, and taked a look at their capabilities, but further research was needed. As my [proposal](https://github.com/poliastro/poliastro/wiki/SOCIS-2017-Antonio-Hidalgo#proposal) was made of 3 different pages, I analyzed each one separately.

## CNEOS page
In the [CNEOS page](https://cneos.jpl.nasa.gov/orbits/) there is a list of tools, but it can be shorten to four different APIs/Databases:

* [JPL Small-Body Database Browser](https://ssd.jpl.nasa.gov/sbdb.cgi): allows to search any small-body (like NEOs) by entering the IAU number, name, or designation, and also supports wild-cards `*` and/or `?`. Available data include, quoting the page itself:
> * orbital elements
> * orbit diagrams
> * physical parameters
> * discovery circumstances
>
> Newly discovered objects and their orbits are added on a daily basis.

* [JPL Small-Body Database Search Engine](https://ssd.jpl.nasa.gov/sbdb_query.cgi): can be used to generate custom tables of orbital and/or physical parameters for all asteroids and comets or a specified sub-set. There is a huge amount of search contraints, for example:
![Figure 1]({filename}/images/sbdb_constraints.jpg "Figure 1")
And you can also select output fields, and choose between HTML and CSV output format.

* [Horizons](https://ssd.jpl.nasa.gov/?horizons): provides access to highly accurate ephemerides for solar system objects, not only small-body. Can be accessed using telnet, email and web-interface.

## NEOWS
Among NASA OPEN APIs, it is [NeoWs](https://api.nasa.gov/neo/?api_key=DEMO_KEY). It can be used to get lists of Near Earth Objects (within a date range, for today...), and to retrieve orbital elements and close aproaches data given a SPK-ID (integer code that [JPL](https://www.jpl.nasa.gov/) uses to identify objects). Despite his name, only works with NEAs (Near Earth Asteroids), and therefore there is no information about comets.

## JPL SSD/CNEOS API SERVICE
As stated on his web, [JPL SSD/CNEOS API SERVICE](https://ssd-api.jpl.nasa.gov/)
> provides an interface to machine-readable data (JSON-format) related to SSD and CNEOS.

The more relevant tools are:

* [Close-Approach Data (CAD)](https://ssd-api.jpl.nasa.gov/doc/cad.html): provides access to current close-approach data for all asteroids and comets in JPL Small-Body DataBase.

* [Accessible NEAs (NHATS)](https://cneos.jpl.nasa.gov/nhats/): is provided by Near-Earth Object Human Space Flight Accessible Targets Study ([NHATS](https://cneos.jpl.nasa.gov/nhats/intro.html)), and can be used to identify those NEAs that may be well-suited to future human space flight round trip rendezvous missions.

* [Scout](https://ssd-api.jpl.nasa.gov/doc/scout.html): Scout system provides trajectory analysis and hazard assessment for recently detected objects.

* [Sentry](https://cneos.jpl.nasa.gov/sentry/): Sentry is a highly automated collision monitoring system that continually scans the most current asteroid catalog for possibilities of future impact.

## Choosing the APIs
Once all the possibilities were studied, it was time to choose the APIs that seem more suitable for our purpose.

Given that `poliastro` core are [Orbit](https://poliastro.readthedocs.io/en/latest/api.html#poliastro.twobody.orbit.Orbit) objects, our main goal is to automatically create a NEO orbit, based on data from internet APIs. In order to achieve this, orbital elements or position and velocity vectors are needed, so this was the first requeriment that APIs had to comply with.

Therefore several APIs could be discarded because they do not provide needed data: `Accesible NEAs`, `Scout`, `Sentry` and `Close-Approach Data`.

Since we would rather not have to deal with intricate POST requests, another important requeriment for APIs was to provide a good interface (the "I" in API stands for interface, so...), and with luck something close to [RESTFul webservices](https://en.wikipedia.org/wiki/Representational_state_transfer).

`JPL Small-Body Database Search Engine` requires POST requests that are more than 150 lines long, so we automatically discarded it.

Finally, the third requeriment, considering that we are writing code in Python, was machine-readable data output, with JSON being the best format and awfully written HTML being the worst.

Both `JPL Small-Body Database Browser` and `Horizons` provide HTML output, which have to be parsed, with all the risks that imply, so they were discarded.

In order to clarify all of this data sequence, I made a table:


|                  API                  | Orbital elements? | REST-style? | Machine-readable? |            Other            |
|:-------------------------------------:|:-----------------:|:-----------:|:-----------------:|:---------------------------:|
|    JPL Small-Body Database Browser    |        Yes        |     Yes     |         No        |     Not limited to NEOs     |
| JPL Small-Body Database Search Engine |        Yes        |      No     |     Yes (CSV)     |     Not limited to NEOs     |
|                Horizons               |        Yes        |      No     |         No        | [existent Python interface] |
|                 NeoWs                 |        Yes        |     Yes     |     Yes (JSON)    |  Only for NEAs (asteroids)  |
|       Close-Approach Data (CAD)       |         No        |     Yes     |     Yes (JSON)    |                             |
|        Accessible NEAs (NHATS)        |         No        |     Yes     |     Yes (JSON)    |                             |
|                 Scout                 |         No        |     Yes     |     Yes (JSON)    |                             |
|                 Sentry                |         No        |     Yes     |     Yes (JSON)    |                             |
[existent Python interface]: https://github.com/mommermi/callhorizons



With all this requeriments in mind, the best option seemed to be `NeoWs`. Although it doesn't provides information about NECs (comets), they are only 0.7% of NEOs total, so they could be discarded (only for the moment :P). Another issue related to `NeoWs` is the fact that it only allows to browse by SPK-ID number (do not confuse with IAU number), which is unknown for most people, so before doing any query, SPK-ID number has to be found.

And that was all for this week. Next week, we will start with coding itself, adding an `orbit_from_spk_id` function to `poliastro`, that queries `NeoWs` API. See you!