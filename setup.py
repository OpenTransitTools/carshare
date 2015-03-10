import os
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.md')).read()
CHANGES = open(os.path.join(here, 'CHANGES.txt')).read()

requires = [
    'ott.utils',
    'argparse',
    'waitress',
    'pyramid',
    'pyramid_mako',
    'mako',
    'pillow',
    'simplejson',
    'geojson',
    'sqlalchemy == 0.8.6', 
    'geoalchemy >= 0.7.2',
    'pyramid_swagger',
]

extras_require = dict(
    dev=[],
)

#
# eggs you need for development, but not production
#
if sys.version_info[:2] < (2, 7):
    requires.extend(['argparse>=1.2.1', 'unittest2>=0.5.1'])


setup(
    name='ott.carshare',
    version='0.1.0',
    description='Open Transit Tools - Carshare db loader and json web services',
    long_description=README + '\n\n' + CHANGES,
    classifiers=[
        "Programming Language :: Python",
        "Framework :: Pyramid",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
    ],
    author="Open Transit Tools",
    author_email="info@opentransittools.org",
    dependency_links=[
        'git+https://github.com/OpenTransitTools/utils.git#egg=ott.utils-0.1.0',
    ],
    license="Mozilla-derived (http://opentransittools.com)",
    url='http://opentransittools.com',
    keywords='ott, otp, gtfs, gtfsdb, data, database, services, transit',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=requires,
    extras_require=extras_require,
    tests_require=requires,
    test_suite="ott.carshare.tests",
    entry_points="""\
        [paste.app_factory]
        main = ott.carshare.pyramid.app:main

        [console_scripts]
        loader = ott.carshare.loader:main
    """,
)
