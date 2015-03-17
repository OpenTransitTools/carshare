import datetime
from sqlalchemy import Column, Index, Integer, Numeric, String, DateTime, ForeignKey

from ott.utils import object_utils

from ott.carshare.model.base import Base
from ott.carshare.model.vehicle import Vehicle
from ott.carshare.model.position import Position
from ott.carshare.model.zipcar.zipcar_pod import ZipcarPod

class ZipcarVehicle(Vehicle):
    '''
    '''
    identity = 'zipcar'
    __tablename__ = 'zipcar_vehicles'
    __mapper_args__ = {'polymorphic_identity': identity}

    id = Column(String, ForeignKey('vehicles.id', ondelete='CASCADE'), primary_key=True)
    pod = Column(String, ForeignKey('zipcar_pods.id'), nullable=True)

    model_id = Column(String)
    img_url = Column(String)
    type = Column(String)
    make = Column(String)
    model = Column(String)
    transmission = Column(String)
    good_to_know  = Column(String)

    def __init__(self, vehicle_id, pod_id):
        self.id  = vehicle_id
        self.pod = pod_id
        self.carshare_company = self.identity

    @classmethod
    def make_vehicles(cls, pod_data):
        '''
        '''
        ret_val = []

        vehicles = object_utils.dval_list(pod_data, 'vehicles')
        for v in vehicles:
            nv = Vehicle()
            ret_val.append(nv)
        return ret_val

    def set_attributes(self, dict):
        ''' copy known values from the dict into this object, then update the timestamp
            zipcar dict: 
            "vehicle": {
                "location_id": 89042307,
                "name": "Mill Creek",
                "model_id": 6869299,  /* Picture of Car: https://media.zipcar.com/images/model-image?model_id=94567 */
                "pretty_type": "Sedan 4 Door, 5 Seatbelts",
                "model": "3",
                "make": "Mazda",
                "pretty_transmission_type": "Automatic transmission",
                "good_to_know": "medium capacity-bike with wheel off, 6-8 standard file boxes",
        
                /* POSITION */
                "latitude": "45.54369687442603",
                "longitude": "-122.66794994473457"
                "location_description": "N Vancouver/Stanton",
                "neighborhoods": [
                    "North/Northeast Portland: Albina"
                ],
        
                /* misc stuff not captured  right now */
                /* fee table */
                "weekday_hourly": 10.25, "weekday_daily": 72, "weekend_hourly": 10.25, "weekend_daily": 72, "distance_included": 180, "7to7_daily": 72,
                "about_me": "Don't ask us why it's called the Mazda 3. Because when it comes to performance and handling, we give it a ten. Yup, it's got \"zoom zoom.\"",
                "little_known_fact": "Mazda has been using the phrase &quot;Zoom Zoom&quot; since the year 2000.",
                "address_id": 89042296,
            }
        '''
        self.name = self.get_attribute(dict, 'name')
        self.model_id = self.get_attribute(dict, 'model_id') 
        self.img_url = "http://media.zipcar.com/images/model-image?model_id={0}".format(self.model_id)
        self.type = self.get_attribute(dict, 'pretty_type')
        self.model = self.get_attribute(dict, 'model')
        self.make = self.get_attribute(dict, 'make')
        self.transmission = self.get_attribute(dict, 'pretty_transmission_type')
        self.good_to_know = self.get_attribute(dict, 'good_to_know')

        self.lat = self.get_attribute(dict, 'latitude')
        self.lon = self.get_attribute(dict, 'longitude')
        self.address = self.get_attribute(dict, 'location_description')
        n = self.get_attribute(dict, 'neighborhoods')
        if n is not None and len(n) > 0:
            self.neighborhood = n[0] 

        self.updated = datetime.datetime.now()

