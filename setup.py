# encoding: utf-8
# Copyright 2009–2012 California Institute of Technology. ALL RIGHTS
# RESERVED. U.S. Government Sponsorship acknowledged.

from setuptools import setup, find_packages
import os.path

# Package data
# ------------

_name        = 'edrnsite.portlets'
_version     = '1.1.5'
_description = 'Portlets for the EDRN Public Portal'
_url         = 'http://cancer.jpl.nasa.gov/products/edrnsite-portlets'
_downloadURL = 'http://oodt.jpl.nasa.gov/dist/edrnsite'
_author      = 'Sean Kelly'
_authorEmail = 'sean.kelly@jpl.nasa.gov'
_license     = 'Proprietary'
_namespaces  = ['edrnsite']
_entryPoints = {}
_extras = {
    'test': ['plone.app.testing'],
}
_zipSafe     = False
_keywords    = 'web zope plone edrn cancer biomarkers portlet'
_requirements = [
    'setuptools',
    'feedparser',
    'Products.CMFPlone',
]
_classifiers = [
    'Development Status :: 4 - Beta',
    'Environment :: Web Environment',
    'Framework :: Plone',
    'Intended Audience :: Healthcare Industry',
    'Intended Audience :: Science/Research',
    'License :: Other/Proprietary License',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Topic :: Internet :: WWW/HTTP',
    'Topic :: Scientific/Engineering :: Bio-Informatics',
    'Topic :: Software Development :: Libraries :: Python Modules',
]

# Setup Metadata
# --------------

def _read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

_header = '*' * len(_name) + '\n' + _name + '\n' + '*' * len(_name)
_longDescription = _header + '\n\n' + _read('README.txt') + '\n\n' + _read('docs', 'INSTALL.txt') + '\n\n' \
    + _read('docs', 'HISTORY.txt') + '\n\n' + _read('docs', 'LICENSE.txt')
open('doc.txt', 'w').write(_longDescription)

setup(
    author=_author,
    author_email=_authorEmail,
    classifiers=_classifiers,
    description=_description,
    download_url=_downloadURL,
    entry_points=_entryPoints,
    extras_require=_extras,
    include_package_data=True,
    install_requires=_requirements,
    keywords=_keywords,
    license=_license,
    long_description=_longDescription,
    name=_name,
    namespace_packages=_namespaces,
    packages=find_packages(exclude=['ez_setup']),
    url=_url,
    version=_version,
    zip_safe=_zipSafe,
)
