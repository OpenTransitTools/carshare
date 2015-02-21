import datetime
from sqlalchemy import Column, Index, Integer, Numeric, String, DateTime, ForeignKey

from ott.carshare.model.base import Base
from ott.carshare.model.vehicle import Vehicle
from ott.carshare.model.position import Position

class ZipcarPod(Base):
    '''
          "location" : 
              {
                  "location_id": 95724,
                  "display_name": "355 Binney St - Kendall Cinema",
                  "address": {
                    "street": "355 Binney St",
                    "city": "Cambridge",
                    "region_name": "Massachusetts",
                    "postal_code": "9700",
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
                  "vehicles": [
              }

              NOTE to SELF - also see these urls in use:
                http://www.trimet.org/go/cgi-bin/cstops.pl?action=entry&resptype=U&lang=en&noCat=Landmark&Loc=11511
                http://www.trimet.org/go/cgi-bin/cstops.cgi?near=SW+Corbett+and+Meade,PO
                http://www.trimet.org/go/cgi-bin/plantrip.cgi?to=2828+S.W.+Corbett,PO
                http://www.trimet.org/schedule/r055.htm
    '''
    __tablename__ = 'zipcar_pods'

    id = Column(String, primary_key=True, nullable=False)
    description = Column(String)
    directions = Column(String)
    transit_url = Column(String)
    transit_stop = Column(String)
    created = Column(DateTime, default=datetime.datetime.now())
    updated = Column(DateTime, default=datetime.datetime.now())

    def __init__(self, location_id):
        self.id = location_id

    def set_attributes(self, dict):
        '''
            location:
            {
                location_id: 68890170,
                address_id: 68890167,
                description: "SE 50th/Belmont",
                directions: "<p class="Detail">This Zipcar is located in the first on-street parking space west of 50th Avenue on the south (eastbound) side of SE Belmont Street.</p>",
                private_directions: "<p class="Detail">This Zipcar is located in the first on-street parking space west of 50th Avenue on the south (eastbound) side of SE Belmont Street.</p>",
                public_transit_url: "http://www.trimet.org/go/cgi-bin/stop_info.pl?lang=en&Id=15966&acode1=PO&x1=45.516978&y1=-122.679601",
                public_transit_stop: "SW 6th and Salmon Stop ID 7789" or "translation missing: en-US.68890170.public_transit_stop"
            }
        '''
        self.description = self.get_attribute(dict, 'description')
        self.directions = self.get_attribute(dict, 'directions')
        self.transit_url = self.get_attribute(dict, 'public_transit_url')
        stop = self.get_attribute(dict, 'public_transit_stop')
        if stop is not None and not stop.startswith('translation missing'):
            self.transit_stop = stop
        self.updated = datetime.datetime.now()
