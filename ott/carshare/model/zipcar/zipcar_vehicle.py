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

    make = Column(String)
    model = Column(String)



    def __init__(self, vehicle_id, pod_id):
        self.id  = vehicle_id
        self.pod = pod_id
        self.carshare_company = self.identity

    @classmethod
    def make_vehicles(cls, pod_id, pod_data):
        '''
            "coordinates": {
                "lat": 42.3673905200087,
                "lng": -71.0897461574591
            },

        '''
        ret_val = []

        import pdb; pdb.set_trace()
        vehicles = object_utils.dval_list(pod_data, 'vehicles')
        coords = object_utils.dval(pod_data, 'coordinates')
        for vdata in vehicles:
            vid = object_utils.dval(vdata, 'vehicle_id')
            zc = ZipcarVehicle(vid, pod_id, coords)
            zc.set_attributes(vdata)
            ret_val.append(zc)
        return ret_val

    def set_attributes(self, dict):
        ''' copy known values from the dict into this object, then update the timestamp
        {
          "vehicle_id": 1179454588,
          "vehicle_name": "Gadsen",
          "make_model": "Volkswagen Golf",
          "style": "5-door",
          "year": 2014,
          "hourly_rate": 10.5,
          "daily_rate": 78,
          "currency_code": "USD",
          "product_types": [
            {
              "type": "standard",
              "label": "Zipcars"
            }
          ],
          "images": {
            "thumb": "http://media.zipcar.com/images/model-image?model_id=980237689&mode=thumb",
            "mobile": "http://media.zipcar.com/images/model-image?model_id=980237689&mode=med",
            "desktop": "http://media.zipcar.com/images/model-image?model_id=980237689"
          },
          "actions": [
            {
              "type": "learn_more",
              "label": "Learn More",
              "url": "http://www.zipcar.com/?mobile_p=0&utm_source=partner&utm_medium=api&utm_campaign=partner_app&utm_content=version0"
            },
            {
              "type": "reserve",
              "label": "Reserve",
              "url": "https://members.zipcar.com/reservations?utm_source=partner&utm_medium=api&utm_campaign=partner_app&utm_content=version0"
            }
          ]
        }
        '''
        self.name  = self.get_attribute(dict, 'name')
        self.model = self.get_attribute(dict, 'make_model')
        self.style = self.get_attribute(dict, 'style')
        self.year  = self.get_attribute(dict, 'year')
        self.hourly  = self.get_attribute(dict, 'hourly_rate')
        self.daily   = self.get_attribute(dict, 'daily_rate')

        self.lat = self.get_attribute(dict, 'latitude')
        self.lon = self.get_attribute(dict, 'longitude')
        self.address = self.get_attribute(dict, 'location_description')
        n = self.get_attribute(dict, 'neighborhoods')
        if n is not None and len(n) > 0:
            self.neighborhood = n[0] 

        self.updated = datetime.datetime.now()

