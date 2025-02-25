# -*- coding: utf-8 -*-

import sys
import os
import re

# If we are building locally, or the build on Read the Docs looks like a PR
# build, prefer to use the version of the theme in this repo, not the installed
# version of the theme.
def is_development_build():
    # PR builds have an interger version
    re_version = re.compile(r'^[\d]+$')
    if 'READTHEDOCS' in os.environ:
        version = os.environ.get('READTHEDOCS_VERSION', '')
        if re_version.match(version):
            return True
        return False
    return True

if is_development_build():
    sys.path.insert(0, os.path.abspath('..'))
sys.path.append(os.path.abspath('./demo/'))

import revitron_sphinx_theme
from sphinx.locale import _

project = u'Revitron'
slug = re.sub(r'\W+', '-', project.lower())
version = '0.7.2'
release = '0.7.2'
author = 'Marc Anton Dahmen'
copyright = '<a href="https://marcdahmen.de">Marc Anton Dahmen</a>'
language = 'en'

extensions = [
    'sphinx.ext.intersphinx',
    'sphinx.ext.autodoc',
    'sphinx.ext.mathjax',
    'sphinx.ext.viewcode',
    'sphinxcontrib.httpdomain',
    'revitron_sphinx_theme',
    'autodocsumm'
]

autodoc_default_options = {
    'autosummary': True 
}

templates_path = ['_templates']
source_suffix = '.rst'
exclude_patterns = []
locale_dirs = ['locale/']
gettext_compact = False

master_doc = 'index'
suppress_warnings = ['image.nonlocal_uri']

intersphinx_mapping = {
    'rtd': ('https://docs.readthedocs.io/en/latest/', None),
    'sphinx': ('http://www.sphinx-doc.org/en/stable/', None),
}

html_theme = 'revitron_sphinx_theme'

html_theme_options = {
    'navigation_depth': 5,
    'logo_mobile': 'revitron-ui-mobile.svg',
    'github_url': 'https://github.com/revitron/revitron',
	'color_scheme': 'dark'
}

html_context = {
	'landing_page': {
		'menu': [
			{'title': 'Docs', 'url': 'installing.html'},
			{'title': 'GitHub', 'url': 'https://github.com'}
		]
	} 
}

if not 'READTHEDOCS' in os.environ:
    html_static_path = ['_static/']
    html_js_files = ['debug.js']

    # Add fake versions for local QA of the menu
    html_context['test_versions'] = list(map(
        lambda x: str(x / 10),
        range(1, 100)
    ))

html_logo = 'demo/static/revitron.svg'
html_title = 'Revitron'
html_show_sourcelink = True

htmlhelp_basename = slug


latex_documents = [
  ('index', '{0}.tex'.format(slug), project, author, 'manual'),
]

man_pages = [
    ('index', slug, project, [author], 1)
]

texinfo_documents = [
  ('index', slug, project, author, slug, project, 'Miscellaneous'),
]


# Extensions to theme docs
def setup(app):
    from sphinx.domains.python import PyField
    from sphinx.util.docfields import Field

    app.add_object_type(
        'confval',
        'confval',
        objname='configuration value',
        indextemplate='pair: %s; configuration value',
        doc_field_types=[
            PyField(
                'type',
                label=_('Type'),
                has_arg=False,
                names=('type',),
                bodyrolename='class'
            ),
            Field(
                'default',
                label=_('Default'),
                has_arg=False,
                names=('default',),
            ),
        ]
    )
