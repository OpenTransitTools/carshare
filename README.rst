========
carshare
========

.. image:: https://badges.gitter.im/Join%20Chat.svg
   :alt: Join the chat at https://gitter.im/OpenTransitTools/gtfsdb
   :target: https://gitter.im/OpenTransitTools/gtfsdb?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge


* Command-line program that reads carshare vehicles locations, and loads them into a database fronted by SQLAlchemy.
* Controller code that exposes car position data in a geojson format.
* Pyramid service that exposes the geojson data returned from the controller code as a webservice.
* Simple OpenLayers app that shows current vehicle locations.
* To get started:
 - PRE: Register with car2go for a developer id at http://code.google.com/p/car2go/wiki/oauth#Registration_as_consumer
 - cd carshare
 - buildout
 - git update-index --assume-unchanged .pydevproject .*/*.xml *.iml
 - bin/loader -k __ your car2go key __ -z -c -d sqlite:///carshare.db (or postgresql+psycopg2://postgres@localhost:5432/postgres -s carshare)
 - bin/pserve development.ini
 - http://localhost:31113/static/test.html
 
* Carshare in Portland, OR -- http://www.portlandoregon.gov/transportation/article/390417
 - car2go
 - Zipcar

