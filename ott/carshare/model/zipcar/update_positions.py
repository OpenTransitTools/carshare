import logging
log = logging.getLogger(__file__)

import json
import urllib

from ott.utils import re_utils
from ott.utils import object_utils

from ott.carshare.model.update_controller import UpdateController
from ott.carshare.model.position import Position
from ott.carshare.model.zipcar.zipcar_pod import ZipcarPod
from ott.carshare.model.zipcar.zipcar_vehicle import ZipcarVehicle

# TODO add these to .config file
DIRECTORY_URL  = "https://api.zipcar.com/v0/directory?country=US&embed=vehicles"
ZIPCODE_FILTER = "(^|\s)(97|98660)"
LOCATION="Portland"

class UpdatePositions(UpdateController):
    '''  TO LOAD Zipcar stuff is a 3-step process:
            1. svc to load pods
            2. svc to find vehicle ids at pods
            3. vehicle detail svc
    '''

    def __init__(self, db, zipcode_filter=ZIPCODE_FILTER, loc=LOCATION):
        self.db = db
        self.pods = None
        self.vehicles = None
        self.zipcode_filter = zipcode_filter

        self.load_zipcar_data()
        self.update_zipcar_db(self.db, self.pods, self.vehicles)

    @classmethod
    def update(cls, db, args):
        ret_val = None
        if args.zipcar:
            print "updating:", __file__
            ret_val = UpdatePositions(db)
        return ret_val

    def load_zipcar_data(self):
        try:
            data = self.get_data()
            data = object_utils.dval(data, 'locations')
            if data:
                self.pods, self.vehicles = UpdatePositions.parse_pods(data, self.zipcode_filter)
            else:
                raise Exception('could not load any Zipcode data {0}'.format(data))
        except Exception, err:
            log.exception('Exception: {0}'.format(err))

    def get_data(self):
        '''
        '''
        #return self.get_test_data()
        url = DIRECTORY_URL
        raw = urllib.urlopen(url)
        json_data = json.load(raw)
        return json_data

    def get_test_data(self):
        json_data=open('/java/DEV/carshare/ott/carshare/model/zipcar/test/directory_old.json')
        data = json.load(json_data)
        json_data.close()
        return data

    @classmethod
    def parse_pods(cls, locations, zip_filter=None):
        '''
          "locations": [
          {
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
          }]
        '''
        pods = []
        vehicles = []
        for l in locations:
            id = object_utils.dval(l, 'location_id')

            # optionally filter by zipcode
            if zip_filter:
                address = object_utils.dval(l, 'address')
                zip = object_utils.dval(address, 'postal_code')
                if not re_utils.contains(zip_filter, zip):
                    log.debug("skipping record: {} not in Zipcar postal_code {}".format(zip_filter, zip))
                    continue

            # make pod
            pod = ZipcarPod(id, l)
            pods.append(pod)


            # make vehicles
            #import pdb; pdb.set_trace()
            v = ZipcarVehicle.make_vehicles(id, l)
            if v:
                vehicles.extend(v)

        return pods, vehicles


    @classmethod
    def update_zipcar_db(cls, db, pods, vehicles):
        ''' NOTE: key parameter is being passed around, since that will eventually be needed for Zipcar
        '''
        session = None
        try:
            session = db.get_session()

            # step 1: remove old stuff....
            zlist = session.query(ZipcarVehicle).all()
            # note: looping through and calling session.delete(z) is the only way I could get SQLAlchemy to delete the
            #       FK relational entry to position table.
            for z in zlist:
                session.delete(z)

            session.query(ZipcarPod).delete()

            session.commit()
            session.flush()

            # step 2: add pods
            for p in pods:
                session.add(p)

            session.commit()
            session.flush()

            # step 3: add vehicles
            for v in vehicles:
                session.add(v)

            session.commit()
            session.flush()

            # step 4: add position data to each vehicle
            Position.clear_latest_column(session, ZipcarVehicle.identity)
            for v in vehicles:
                v.update_position(session, v.lat, v.lon, v.street, v.city, v.state, v.zip, 1)

        except Exception, err:
            log.exception('Exception: {0}'.format(err))
            pass
        finally:
            if session:
                # step 3: commit stuff...
                session.commit()
                session.flush()




def main():
    from pprint import pprint
    u = UpdatePositions(None)

    print u.pods[0].__dict__
    print u.vehicles[0].__dict__


if __name__ == '__main__':
    main()
