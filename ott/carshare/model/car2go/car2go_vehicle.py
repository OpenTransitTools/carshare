import datetime
from sqlalchemy import Column, Index, Integer, Numeric, Boolean, String, DateTime, ForeignKey

from ott.carshare.model.vehicle import Vehicle

class Car2GoVehicle(Vehicle):
    identity = 'car2go'
    __tablename__ = 'car2go_vehicles'
    __mapper_args__ = {'polymorphic_identity': identity}

    id = Column(String, ForeignKey('vehicles.id', ondelete='CASCADE'), primary_key=True)
    interior = Column(String)
    exterior = Column(String)
    fuel = Column(String)
    engineType = Column(String)
    hasBikeRack = Column(Boolean)


    def __init__(self, id, name=None):
        self.id = id
        self.name = name
        self.carshare_company = self.identity


    def set_attributes(self, dict):
        ''' copy known values from the dict into this object, then update the timestamp
            car2go v2.1 dict = {u'name': u'271FRH', u'vin': u'WMEEJ3BA3CK569302', u'coordinates': [-122.61106, 45.50267, 0], u'interior': u'GOOD', u'exterior': u'GOOD', u'address': u'Se 50th Ave 2787, 97206 Multnomah', u'fuel': 57, u'engineType': u'CE'}
        '''
        self.name = self.get_attribute(dict, 'name')
        self.interior = self.get_attribute(dict, 'interior')
        self.exterior = self.get_attribute(dict, 'exterior')
        self.fuel = self.get_attribute(dict, 'fuel')
        self.engineType = self.get_attribute(dict, 'engineType')
        self.updated = datetime.datetime.now()

        if "BIKE RACK" in self.name:
            self.hasBikeRack = True
            self.name = self.name.strip("BIKE RACK").strip()

