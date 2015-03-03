import json
import re
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
        ''' call the car2go service, retrieve new positions, and update car position database
        '''

        # step 0: setup
        self.house_num_and_zip_re = re.compile('[0-9]*, 9[0-9]+')

        # step 1: new car2go data
        self.pos = []
        self.url = "{0}?oauth_consumer_key={1}&format={2}&loc={3}".format(svc, key, format, loc)
        print self.url
        raw = urllib.urlopen(self.url)
        car2go_data = json.load(raw)

        # step 2: if we have valid data, update the database
        if car2go_data and len(car2go_data['placemarks']) > 0:
            session = db.get_session()

            # step 2a: clear out the 'latest' flag from the position table (so we know the new service data is the 'latest' positions)
            Position.clear_latest_column(session, Car2GoVehicle.identity)

            # step 2b: update the positions 
            for v in car2go_data['placemarks']:
                self.append_pos(session, v)
                continue

            # step 2c: commit the new positions
            session.flush()
            session.commit()


    def append_pos(self, session, vehicle):
        ''' get vehicle from db, then update its position (or update timestamp if vehicle is parked)
        '''
        v = self.get_vehicle(session, vehicle)
        if v is not None:
            lat, lon = self.get_coord(vehicle)
            address, city, zip = self.get_address(vehicle)
            v.update_position(session, lat, lon, address, city, zip)


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

    def get_address(self, vehicle):
        ''' parse car2go's funky address string SE Lambert St 1683, 97202 Portland or Veterans Memorial Hwy, 97266 Portland
        '''
        address = None
        city = None
        zipcode = None
        try:
            # step 1: get address and assign it to address in case anything goes wrong
            address = vehicle['address']

            # step 2: parse "SE Lambert St 1683, 97202 Portland" or "Veterans Memorial Hwy, 97266 Portland" into address, zip and city
            street_n_city = re.split(self.house_num_and_zip_re, address)
            house_num_n_zip = re.findall(self.house_num_and_zip_re, address)
            house_num_n_zip = house_num_n_zip[0].split(',')
            street = street_n_city[0].strip()
            city = street_n_city[1].strip()
            zipcode = house_num_n_zip[1].strip()
            house_num = house_num_n_zip[0].strip()
            if house_num:
                address = "{0} {1}".format(house_num, street)
            else:
                address = street
        except Exception, err:
            print 'Exception: {0}'.format(err)
        return address,city,zipcode


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

