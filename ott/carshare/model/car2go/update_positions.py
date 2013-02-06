import json
import urllib
import datetime

from ott.carshare.model.vehicle import Vehicle
from ott.carshare.model.car2go.car2go_vehicle import Car2GoVehicle
from ott.carshare.model.position import Position


# car2go API: https://code.google.com/p/car2go/wiki/index_v2_1
# 
# https://www.car2go.com/api/v2.1/locations?oauth_consumer_key=<key>&format=json
# https://www.car2go.com/api/v2.1/vehicles?oauth_consumer_key=<key>&format=json&loc=Portland
# https://www.car2go.com/api/v2.1/gasstations?oauth_consumer_key=<key>&format=json&loc=Portland

VEHICLES_URL="https://www.car2go.com/api/v2.1/vehicles"

class UpdatePositions():

    def __init__(self, db, key, svc=VEHICLES_URL, loc='Portland', format='json'):
        self.pos = []
        self.url = "{0}?oauth_consumer_key={1}&format={2}&loc={3}".format(svc, key, format, loc)
        print self.url

        raw = urllib.urlopen(self.url)
        car2go_data = json.load(raw)
        session = db.get_session()
        for v in car2go_data['placemarks']:
            self.append_pos(session, v)
        session.flush()
        session.commit()


    def append_pos(self, session, vehicle):
        ''' get vehicle from db, then update its position (or update timestamp if vehicle is parked)
        '''
        v = self.get_vehicle(session, vehicle)
        if v is not None:
            address = vehicle['address']
            lat, lon = self.get_coord(vehicle)
            v.update_position(session, lat, lon, address)


    def get_coord(self, vehicle):
        lat = None
        lon = None
        try:
            ll = vehicle['coordinates']
            lon = ll[0]
            lat = ll[1]
        except:
            print "Exception"
        return lat,lon


    def get_vehicle(self, session, vehicle):
        ''' record from car2go service
            {
              "address":"Nw 9th Ave 1155, 97209 Multnomah",
              "coordinates":[-122.68043,45.53125,0],
              "name":"386FRH",
              "vin":"WMEEJ3BAXCK561214",
              "engineType":"CE",
              "fuel":57,
              "exterior":"GOOD",
              "interior":"GOOD"
            }
        '''
        v=None
        try:
            # step 1: find vehicle in db
            id = vehicle['vin']
            v = session.query(Car2GoVehicle).get(id)

            # step 2: create new vehicle and add to db
            if v is None:
                v = Car2GoVehicle(id)
                session.add(v)

            v.set_attributes(vehicle)
        except Exception, err:
            print 'Exception: {0}'.format(err)
            pass

        return v

