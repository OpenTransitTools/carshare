import datetime
from sqlalchemy import Column, Index, Integer, Numeric, String, DateTime, ForeignKey

from ott.utils import object_utils

from ott.carshare.model.base import Base
from ott.carshare.model.vehicle import Vehicle
from ott.carshare.model.position import Position

class ZipcarPod(Base):
    '''
    '''
    __tablename__ = 'zipcar_pods'

    id = Column(String, primary_key=True, nullable=False)
    description = Column(String)
    created = Column(DateTime, default=datetime.datetime.now())
    updated = Column(DateTime, default=datetime.datetime.now())

    def __init__(self, location_id, pod_data=None):
        self.id = location_id
        if pod_data:
            self.set_attributes(pod_data)

    def set_attributes(self, dict):
        '''
              "location_id": 95724,
              "display_name": "355 Binney St - Kendall Cinema",
              "address": {
                "street": "355 Binney St",
                "city": "Cambridge",
                "region_name": "Massachusetts",
                "postal_code": "02139",
                "country_code": "US"
              },
              "coordinates": {
                "lat": 42.3673905200087,
                "lng": -71.0897461574591
              },
              "num_vehicles": 8,
              "products": [
                {
                  "type": "standard",
                  "label": "Zipcars"
                }
              ],
              "vehicles": [ { ... }, {...}]
        '''
        self.description = self.get_attribute(dict, 'display_name')
        self.directions = self.get_attribute(dict, 'directions')
        self.transit_url = self.get_attribute(dict, 'public_transit_url')
        stop = self.get_attribute(dict, 'public_transit_stop')
        if stop is not None and not stop.startswith('translation missing'):
            self.transit_stop = stop
        self.updated = datetime.datetime.now()
