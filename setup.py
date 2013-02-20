import os
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.md')).read()
CHANGES = open(os.path.join(here, 'CHANGES.txt')).read()

requires = [
    'argparse',
    'pyramid',
    'pyramid_debugtoolbar',
    'waitress',
    'simplejson',
    'geojson',
    'geoalchemy',
    'setuptools',
]

#
# eggs you need for development, but not production
#
dev_extras = (
    'zc.buildout',
    'coverage>=3.5.2',
    'fabric>=1.4.3',
    'zest.releaser>=3.37',
)


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
    author='Frank Purcell',
    author_email='ott@frankpurcell.com',
    url='http://opentransittools.com',
    keywords='carshare',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=requires,
    tests_require=requires,
    test_suite="ott.carshare",
    extras_require=dict(dev=dev_extras),
    entry_points="""\
        [paste.app_factory]
        main = ott.carshare:main
    """,
)
