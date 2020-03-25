#!/usr/bin/env python

AUTHOR = 'Antonio Hidalgo'
SITENAME = 'blog'
SITESUBTITLE = u"anhiga's blog"
SITEURL = 'blog.anhiga.me'
PATH = 'content'
TIMEZONE = 'Europe/Madrid'
DEFAULT_LANG = 'en'
LOCALE = 'en_US.UTF-8'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Set the article URL
ARTICLE_URL = '{date:%Y}/{date:%m}/{date:%d}/{slug}/'
ARTICLE_SAVE_AS = '{date:%Y}/{date:%m}/{date:%d}/{slug}/index.html'

DEFAULT_PAGINATION = 10

#SUMMARY_USE_FIRST_PARAGRAPH = True
SUMMARY_MAX_LENGTH = 140

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True

#MARKUP = ('md', 'ipynb')
#PLUGINS = ['ipynb.markup']

MARKUP = ['md']
PLUGIN_PATHS = ['./plugins', './plugins/pelican-plugins']
PLUGINS = [
    'summary',       # auto-summarizing articles
    'feed_summary',  # use summaries for RSS, not full articles
    'ipynb.liquid',  # for embedding notebooks
    'liquid_tags.img',  # embedding images
    'liquid_tags.video',  # embedding videos
    'liquid_tags.include_code',  # including code blocks
    'liquid_tags.literal',
    #'headerid',  # https://github.com/getpelican/pelican-plugins/tree/master/headerid
    #'gravatar',  # https://github.com/getpelican/pelican-plugins/tree/master/gravatar
    #'footer_insert',  # https://github.com/getpelican/pelican-plugins/tree/master/footer_insert
    #'autopages',  # https://github.com/getpelican/pelican-plugins/tree/master/autopages
    #'simple_footnotes', # https://github.com/getpelican/pelican-plugins/tree/master/simple_footnotes
    #'show_source',  # https://github.com/getpelican/pelican-plugins/tree/master/show_source
    #'series',  # https://github.com/getpelican/pelican-plugins/tree/master/series
    #'representative_image',  # https://github.com/getpelican/pelican-plugins/tree/master/representative_image
]
IGNORE_FILES = ['.ipynb_checkpoints']

# for liquid tags
CODE_DIR = 'downloads/code'
NOTEBOOK_DIR = 'downloads/notebooks'

# THEME SETTINGS
THEME = './theme/'

ABOUT_PAGE = None
#TWITTER_USERNAME = 'poliastro'
GITHUB_USERNAME = 'anhiga'
SHOW_ARCHIVES = True
SHOW_FEED = False  # Need to address large feeds

ISSO_HOST = 'localhost:1234'

ENABLE_MATHJAX = True

STATIC_PATHS = ['images', 'figures', 'videos', 'downloads']

# Footer info

LICENSE_URL = "https://github.com/anhiga/anhiga.github.io-source/blob/master/LICENSE"
LICENSE = "CC-BY for content and MIT for code"
