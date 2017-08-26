# Source for http://poliastro.github.io

This repository contains the source for http://poliastro.github.io/.

_Based on the wonderful job by Jake Vanderplas https://github.com/jakevdp/jakevdp.github.io-source (MIT License)_

## Building the Blog

Clone the repository & make sure submodules are included

```
$ git clone https://github.com/poliastro/poliastro.github.io-source.git
$ git submodule update --init --recursive
```

Install the required packages:

```
$ conda env create [ -f environment.yml ]
$ source activate poliastro36
(poliastro36) $ npm install -g less
```

To generate the main CSS:

```
(poliastro36) $ lessc main.less > main.css
```

Build the html and serve locally:

```
(poliastro36) $ make html
(poliastro36) $ make serve
(poliastro36) $ open http://localhost:8000
```

Deploy to github pages

```
(poliastro36) $ make publish-to-github
```

