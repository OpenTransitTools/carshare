import datetime
from sqlalchemy import Column, Index, Integer, Numeric, String, DateTime, ForeignKey

from ott.utils import object_utils
from ott.utils import geo_utils

from ott.carshare.model.vehicle import Vehicle

class ZipcarVehicle(Vehicle):
    '''
    '''
    identity = 'zipcar'
    __tablename__ = 'zipcar_vehicles'
    __mapper_args__ = {'polymorphic_identity': identity}

    id = Column(String, ForeignKey('vehicles.id', ondelete='CASCADE'), primary_key=True)
    pod = Column(String, ForeignKey('zipcar_pods.id'), nullable=True)

    model = Column(String)
    style = Column(String)
    year  = Column(String)
    hourly = Column(String)
    daily  = Column(String)

    img_thumb = Column(String)
    img_small = Column(String)
    img_large = Column(String)

    url_info = Column(String)
    url_reserve = Column(String)

    street = city = state = zip = None
    lat = lon = None

    def __init__(self, vehicle_id, pod_id):
        self.id  = str(vehicle_id)
        self.pod = str(pod_id)
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

        vehicles = object_utils.dval_list(pod_data, 'vehicles')
        for vehicle_data in vehicles:
            vid = object_utils.dval(vehicle_data, 'vehicle_id')
            zc = ZipcarVehicle(vid, pod_id)
            zc.set_attributes(pod_data, vehicle_data)
            ret_val.append(zc)
        return ret_val

    def set_attributes(self, pod_data, vehicle_data):
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
        self.name   = object_utils.dval(vehicle_data, 'vehicle_name')
        self.model  = object_utils.dval(vehicle_data, 'make_model')
        self.style  = object_utils.dval(vehicle_data, 'style')
        self.year   = object_utils.dval(vehicle_data, 'year')
        self.hourly = object_utils.dval(vehicle_data, 'hourly_rate')
        self.daily  = object_utils.dval(vehicle_data, 'daily_rate')

        images = object_utils.dval(vehicle_data, 'images')
        self.img_thumb = object_utils.dval(images, 'thumb')
        self.img_small = object_utils.dval(images, 'mobile')
        self.img_large = object_utils.dval(images, 'desktop')

        urls = object_utils.dval_list(vehicle_data, 'actions')
        for u in urls:
            type = object_utils.dval(u, 'type')
            if type == 'reserve':
                self.url_reserve = object_utils.dval(u, 'url')
            if type == 'learn_more':
                self.url_info = object_utils.dval(u, 'url')

        coord = object_utils.dval(pod_data, 'coordinates')
        address = object_utils.dval(pod_data, 'address')
        self.lat, self.lon  = geo_utils.get_coord_from_dict(coord)
        self.street, self.city, self.state, self.zip = geo_utils.get_address_from_dict(address)
        self.updated = datetime.datetime.now()

