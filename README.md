carshare
========

* Command-line program that reads carshare vehicles locations, and loads them into a database fronted by SQLAlchemy.
* Controller code that exposes car position data in a json format.
* Pyramid that exposes the json data returned from the controller code as a webservice.
* Simple jQuery mobile / OpenLayers app that shows current vehicle locations.
