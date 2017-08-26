Title: Pelican, Github Pages y despliegue automático (SOCIS 2017)
Date: 2017-07-15 14:00
Category: SOCIS
Tags: SOCIS, ESA, poliastro
slug: 2017-07-15-pelican-github-pages-and-auto-deployment-socis
lang: es
Author: Antonio Hidalgo Galindo

Tras varias semanas creyendo que [SOCIS](http://sophia.estec.esa.int/socis/) no se realizaría este año, ¡por fin me ha llegado el email!  Estoy muy contento de haber sido elegido por `poliastro` y mi mentor `@astrojuanlu`, con el objetivo de crear una API, basada en las APIs abiertas de la NASA, para proporcionar datos orbitales de cuerpos menores ([mi propuesta completa está aquí](https://github.com/poliastro/poliastro/wiki/SOCIS-2017-Antonio-Hidalgo)).

Nuestra idea es escribir una entrada semanal en este blog, documentado el trabajo realizado durante esa semana. Creo que cada post será una buena manera de revisar lo que se va consiguiendo, y además espero que resulte interesante para cualquier interesado en Python, ciencia, [NEOs](https://es.wikipedia.org/wiki/Objeto_pr%C3%B3ximo_a_la_Tierra), o simplemente en leer blogs aleatorios por internet.

Esta ha sido la primera de ocho semanas (sí, sé que en mi propuesta pone otra cosa, pero es el tiempo que tenemos 😊), y, sorprendentemente, la primera tarea que se me ha encargado ha sido... ¡montar este blog!

Así qué, sin más dilación, empecemos.


## Pelican, Github Pages y despliegue automático

Ya que `poliastro` es un proyecto basado en Python, decidimos usar [Pelican](https://blog.getpelican.com/), un generador de páginas estáticas escrito en Python, para crear el blog. En cuanto al hosting, la elección fue Github Pages. Mi mentor ya había participado en un blog con Pelican, basado en [este repositorio de Jake Vanderplas](https://github.com/jakevdp/jakevdp.github.io-source), así que ese fue mi punto de partida.

Tuve que cambiar todas las páginas y cadenas relacionadas con el proyecto anterior por los correspondientes de `poliastro`.
Además de eso, también queríamos automatizar el proceso de despliegue del blog en Github Pages, una tarea algo más complicada, y decidimos usar Travis CI, una herramienta de Integración Continua muy usada en el entorno de Github.

Tras unas cuantas búsquedas en Google, aparecieron varios resultados. Vladimir Starkov había investigado en [este artículo](https://iamstarkov.com/deploy-gh-pages-from-travis/) sobre lo mismo que yo intentaba conseguir. La manera más fácil de autenticarnos en Github era usando un Github Token, pero tenía que estar cifrado de forma que nadie pudiese entrar en mi cuenta usándolo.

Después de investigar un poco, descubrí que Travis puede encriptar variables usando una clave publica RSA asociada a cada repositorio (se puede comprobar usando la API de Travis: ```https://api.travis-ci.org/repos/$(owner_name)/$(repo_name)/key```).
Ya que tengo permisos para editar `poliastro.github.io-source` y `poliastro.github.io repos`, decidí usar un Github Token de mi cuenta y cifrarlo con la clave pública asociada al repositorio `poliastro.github.io-source` en Travis CI:

```bash
$ travis encrypt GH_TOKEN=$(Github Token) -r /poliastro/poliastro.github.io-source
secure: "a-really-long-string”
```

Al añadir la clave cifrada al archivo .travis.yml, ya podía usar la variable GH_TOKEN en Travis, y subir el archivo a Github sin exponer mi token.

El despliegue fue escrito en un `makefile`, usando la [herramienta ghp-import](https://github.com/davisp/ghp-import), que crea una nueva rama que contiene únicamente la documentación. Después se realiza un push desde esa rama al repositorio de Github Pages, `poliastro.github.io` en nuestro caso:

```makefile
GITHUB_PAGES_REMOTE=https://${GH_TOKEN}@github.com/poliastro/poliastro.github.io.git
GITHUB_PAGES_BRANCH=master

.......

publish-to-github-force: publish
    ghp-import -n -m "publish-to-github-force from $(GIT_COMMIT_HASH)" -b blog-build $(OUTPUTDIR)
	git push -f $(GITHUB_PAGES_REMOTE) blog-build:$(GITHUB_PAGES_BRANCH)
```

Por tanto, cada vez que Travis CI se ejecuta en [poliastro.github.io-source](https://travis-ci.org/poliastro/poliastro.github.io-source), la variable se descifra automáticamente usando la clave privada del repositorio (excepto cuando se ejecuta por culpa de un Pull Request, como se desprende de [aquí](https://docs.travis-ci.com/user/encryption-keys/), hecho que provocó varios quebraderos de cabeza :P), y el token se usa para desplegar el código en el repositorio `poliastro.github.io`.

![Travis log with decrypted GH_TOKEN]({filename}/images/travis_decryption_log.jpg "Travis log with decrypted GH_TOKEN")

Este ha sido mi trabajo de la última semana. Si quieres ver el código completo, está disponible en [Github](https://github.com/poliastro/poliastro.github.io-source).

La próxima semana empezaremos con Python, las APIs de la NASA y muchas más cosas interesantes.