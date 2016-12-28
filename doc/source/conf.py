#!/usr/bin/env python3

project = 'twittback'
author = 'Dimitri Merejkowsky'
version = '0.1'
language = 'en'

source_suffix = '.rst'
master_doc = 'index'

templates_path = ['_templates']

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.todo',
    'sphinxcontrib.spelling',
]

spelling_word_list_filename = '../../wordlist.txt'

pygments_style = 'sphinx'

todo_include_todos = True

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
html_show_sourcelink = True
