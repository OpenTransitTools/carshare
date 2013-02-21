carshare
========

* Command-line program that reads carshare vehicles locations, and loads them into a database fronted by SQLAlchemy.
* Controller code that exposes car position data in a geojson format.
* Pyramid service that exposes the geojson data returned from the controller code as a webservice.
* Simple OpenLayers app that shows current vehicle locations.
* To get started:
 - PRE: Register with car2go for a developer id at http://code.google.com/p/car2go/wiki/oauth#Registration_as_consumer
 - cd carshare
 - buildout
 - bin/python ott/carshare/loader.py -k __ your car2go key __ -u sqlite:///carshare.db -c
 - bin/pserve development.ini
 - http://localhost:31113/static/test.html