import json
import urllib
import datetime
import traceback


from ott.utils import re_utils
from ott.utils import object_utils

from ott.carshare.model.position import Position
from ott.carshare.model.vehicle import Vehicle
from ott.carshare.model.base import Base
from ott.carshare.model.update_controller import UpdateController
from ott.carshare.model.zipcar.zipcar_vehicle import ZipcarPod
from ott.carshare.model.zipcar.zipcar_vehicle import ZipcarVehicle

class UpdatePositions(UpdateController):
    '''  TO LOAD Zipcar stuff is a 3-step process:
            1. svc to load pods
            2. svc to find vehicle ids at pods
            3. vehicle detail svc
    '''
    def __init__(self, db, key, zipcar_domain='', loc='Portland'):
        print "X"

    @classmethod
    def update(cls, db, args):
        ret_val = None
        if args.zipcar:
            print "updating:", __file__
            ret_val = UpdatePositions(db, args.zipcar)
        return ret_val

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
        ret_val = []
        for l in locations:
            id = object_utils.dval(l, 'location_id')
            if zip_filter:
                address = object_utils.dval(l, 'address')
                zip = object_utils.dval(address, 'postal_code')
                if not re_utils.contains(zip_filter, zip):
                    print "INFO: skipping record: {} not in Zipcar postal_code {}".format(zip_filter, zip)
                    continue
            pod = ZipcarPod(id, l)
            v = pod.make_vehicles(l)
            ret_val.append(pod)

        return ret_val

def main():
    from pprint import pprint
    json_data=open('/java/DEV/carshare/ott/carshare/model/zipcar/test/directory.json')
    data = json.load(json_data)
    #pprint(data)
    pods = UpdatePositions.parse_pods(object_utils.dval(data, 'locations'), "^9[78]*")
    print pods[0].__dict__

    json_data.close()

if __name__ == '__main__':
    main()
