import os
from setuptools import setup, find_packages


here = os.path.abspath(os.path.dirname(__file__))

README = open(os.path.join(here, 'README.rst')).read()
CHANGES = open(os.path.join(here, 'CHANGES.txt')).read()

requires = [
    'ott.utils',
    'argparse',
    'waitress',
    'pyramid',
    'pyramid_mako',
    'pyramid_swagger',
    'mako',
    'pillow',
    'simplejson',
    'geojson',
    'geoalchemy2',
    'sqlalchemy',
]

dev_extras = []
oracle_extras = ['cx_oracle>=5.1']
postgresql_extras = ['psycopg2>=2.4.2']

extras_require = dict(
    dev=dev_extras,
    postgresql=postgresql_extras,
)

setup(
    name='ott.carshare',
    version='0.1.0',
    description='Open Transit Tools - Carshare db loader and json web services',
    long_description=README + '\n\n' + CHANGES,
    keywords='GTFS,GTFS-realtime,GTFSRT',
    url='http://opentransittools.com',
    license="Mozilla-derived (http://opentransittools.com)",
    author="Open Transit Tools",
    author_email="info@opentransittools.org",
    classifiers=[
        "Programming Language :: Python",
        "Framework :: Pyramid",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
    ],
    dependency_links=[
        'git+https://github.com/OpenTransitTools/utils.git#egg=ott.utils-0.1.0',
    ],
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
