from setuptools import setup, find_packages
import sys

required_eggs = [
    'pyramid',
    'simplejson',
    'geoalchemy',
    'setuptools',
]

# NOTE: also required is a db driver ... on windows, precompiled drivers are common.  
#       buildout.cfg allows psycopg2 and oracle drivers installed locally.
#       http://www.stickpeople.com/projects/python/win-psycopg/

#
# eggs that you need if you're running a version of python lower than 2.7
#
if sys.version_info[:2] < (2, 7):
    install_requires.extend(['argparse>=1.2.1', 'unittest2>=0.5.1'])

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
    url='https://github.com/OpenTransitTools/carshare',
    namespace_packages=('ott',),
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=required_eggs,
    extras_require=dict(dev=dev_extras)
)
