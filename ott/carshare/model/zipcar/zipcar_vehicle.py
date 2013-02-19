import datetime
from sqlalchemy import Column, Index, Integer, Numeric, String, DateTime, ForeignKey

from ott.carshare.model.base import Base
from ott.carshare.model.vehicle import Vehicle
from ott.carshare.model.position import Position

class ZipcarPod(Base):
    '''
          "location" : 
              {
                  "location_id":68890170,
                  "directions":"<p class=\"Detail\">This Zipcar is located in the first on-street parking space west of 50th...</p>",
                  "public_transit_url":"http://www.trimet.org/go/cgi-bin/stop_info.pl?lang=en&Id=15966&acode1=PO&x1=45.516978&y1=-122.679601",
                  "public_transit_stop":""

                  "description":"SE 50th/Belmont", /* address / location ... part of vehicle too */
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

