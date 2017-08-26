Title: Pelican, Github Pages and auto-deployment (SOCIS 2017)
Date: 2017-07-15 14:00
Category: SOCIS
Tags: SOCIS, ESA, poliastro
slug: 2017-07-15-pelican-github-pages-and-auto-deployment-socis
lang: en
Author: Antonio Hidalgo Galindo

After several weeks thinking that [SOCIS](http://sophia.estec.esa.int/socis/) would not launch this year, finally the long-awaited email arrived! I am really happy for being selected by `poliastro` and my mentor `@astrojuanlu`, with the aim of creating an API, relying on NASA Open APIs, in order to provide small-bodies orbital data ([my proposal can be seen here](https://github.com/poliastro/poliastro/wiki/SOCIS-2017-Antonio-Hidalgo)).

Our plan is to write a weekly blog entry, stating and documenting what have been done during that period. I think these posts will be a great way of reviewing what have been accomplished, and I also hope they will be interesting enough to anyone interested in Python, science, [NEOs](https://en.wikipedia.org/wiki/Near-Earth_object), or just reading random internet blogs.

This has been the first one of eight weeks (yeah, that’s not what my proposal timeline says, but it’s all we have 😊), and, surprisingly, the first task I was assigned was… setting up this blog!

So, without further ado, let’s start.


## Pelican, Github Pages and auto-deployment

Given that `poliastro` is a Python-based project, we decided to use [Pelican](https://blog.getpelican.com/), a static site generator which is written in Python, to create the blog. Regarding the hosting, our choice was Github Pages. My mentor had already participated in a repository with a Pelican blog, based on another [repository from Jake Vanderplas](https://github.com/jakevdp/jakevdp.github.io-source), so that was my starting point.

I had to change all the pages and strings related to the previous project for `poliastro` ones. Besides that, we wanted to automatize the deployment process to Github Pages, a little harder task, and we decided to try with Travis CI, a Continuous Integration tool, very used in Github environment.

After googling a little bit, a few results appeared. Vladimir Starkov had researched in [this article](https://iamstarkov.com/deploy-gh-pages-from-travis/) about basically what I was trying to accomplish. The easiest way of authenticating on Github was using a Github Token, but it had to be encrypted so no one could login in my account using it.

After some further researching, I discovered that Travis encrypts variables using a RSA public key associated to every repository (you can use Travis API if you want to check it: ```https://api.travis-ci.org/repos/$(owner_name)/$(repo_name)/key```. As I have full permissions to edit `poliastro.github.io-source` and `poliastro.github.io repos` repos, I decided to request a Github Token, and I encrypted it with the public key associated to `poliastro.github.io-source` repository in Travis CI:

```bash
$ travis encrypt GH_TOKEN=$(My Github Token) -r /poliastro/poliastro.github.io-source
secure: "a-really-long-string”
```

Adding this encrypted key to .travis.yml file, I could use GH_TOKEN variable in it, and upload it to Github without exposing my private token.

The deployment was coded in a `makefile`, using the [ghp-import tool](https://github.com/davisp/ghp-import), which creates a branch containing only documentation. This branch is later pushed to Github Pages repository, `poliastro.github.io` in our code:

```makefile
GITHUB_PAGES_REMOTE=https://${GH_TOKEN}@github.com/poliastro/poliastro.github.io.git
GITHUB_PAGES_BRANCH=master

.......

publish-to-github-force: publish
    ghp-import -n -m "publish-to-github-force from $(GIT_COMMIT_HASH)" -b blog-build $(OUTPUTDIR)
	git push -f $(GITHUB_PAGES_REMOTE) blog-build:$(GITHUB_PAGES_BRANCH)
```

So, whenever Travis CI executes a build in [poliastro.github.io-source](https://travis-ci.org/poliastro/poliastro.github.io-source), the variable gets automatically decrypted using the repository private key (except for builds caused by a Pull Request, as stated [here](https://docs.travis-ci.com/user/encryption-keys/), fact that turned to be a big headache for us :P), and the token is used to push to `poliastro.github.io` repo.

![Travis log with decrypted GH_TOKEN]({filename}/images/travis_decryption_log.jpg "Travis log with decrypted GH_TOKEN")

That was my work in the last week. If you would like to check the code, is available on [Github](https://github.com/poliastro/poliastro.github.io-source).

Next week we will probably start with Python, NASA APIs and more interesting stuff!
