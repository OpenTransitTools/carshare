import json
import urllib
import datetime
import traceback

from ott.carshare.model.position import Position
from ott.carshare.model.vehicle import Vehicle
from ott.carshare.model.zipcar.zipcar_vehicle import ZipcarPod
from ott.carshare.model.zipcar.zipcar_vehicle import ZipcarVehicle

# PODs: /api/2.0/locations.json?lat=45.5&long=-122.5&lat_delta=1.0&lng_delta=1.0
# VEHICLE LIST: /api/2.0/locations/89042307/vehicles.json
# VEHICLE DETAILS:/api/2.0/vehicles/513127255.json 

LOC_PARAM='lat=45.5&long=-122.5&lat_delta=1.0&lng_delta=1.0'
TEST_LOC_PARAM='lat=45.5&long=-122.5&lat_delta=0.05&lng_delta=0.09'


class ZipcarPodsAndVehicles():
    '''  TO LOAD Zipcar stuff is a 3-step process:
            1. svc to load pods
            2. svc to find vehicle ids at pods
            3. vehicle detail svc
    '''

    def __init__(self, db, key, zipcar_domain, loc=LOC_PARAM):
        # would like to be able to overwrite the folling via config file for testing o
        self.pod_url_template = "{0}/api/2.0/locations.json?{2}"
        self.vlist_url_template = "{0}/api/2.0/locations/{2}/vehicles.json"
        self.vehicle_url_template = "{0}/api/2.0/vehicles/{2}.json"
        self.min_num_vehicles = 2

        self.key = key

        pods = self.get_pods(key, zipcar_domain, loc)
        vehicles = self.get_vehicles(key, zipcar_domain, pods)
        if len(vehicles) > self.min_num_vehicles:
            self.update_zipcar_db(db, pods, vehicles)


    def update_zipcar_db(self, db, pods, vehicles):
        ''' NOTE: key parameter is being passed around, since that will eventually be needed for Zipcar
        '''
        session = db.get_session()

        # step 1: remove old stuff....
        session.query(ZipcarPod).delete()
        zlist = session.query(ZipcarVehicle).all()
        # note: looping through and calling session.delete(z) is the only way I could get SQLAlchemy to delete the FK relational entry to position table.
        for z in zlist:
            session.delete(z)
        session.flush()
        session.commit()

        # step 2: add pods
        for p in pods:
            session.add(p)

        # step 3: add vehicles
        for v in vehicles:
            session.add(v)
            v.update_position(session, v.lat, v.lon, v.address, v.neighborhood)

        # step 3: commit stuff...
        session.flush()
        session.commit()


    def get_vehicles(self, key, zipcar_domain, pods):
        ''' NOTE: key parameter is being passed around, since that will eventually be needed for Zipcar
            query Zipcar webservice for list of vehicles...

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
        ret_val = []
        for pod in pods:
            # step 1: get the vehicle list at this pod location
            vlist = self.get_vehicles_at_pod(zipcar_domain, key, pod.id)

            # TODO log.debug(pod.description)

            # step 2: get vehicle details for each auto in the given pod
            for vehicle_id in vlist:
                try:
                    vehicle_url = self.vehicle_url_template.format(zipcar_domain, key, vehicle_id)
                    raw = urllib.urlopen(vehicle_url)
                    vjson = json.load(raw)
                    v = ZipcarVehicle(vehicle_id, pod.id)
                    v.set_attributes(vjson['vehicle'])
                    ret_val.append(v)
                    # TODO log.debug(v.name)
                except:
                    print 'Exception get_vehicles()'
                    print traceback.format_exc()

        return ret_val


    def get_vehicles_at_pod(self, zipcar_domain, key, pod):
        ''' NOTE: key parameter is being passed around, since that will eventually be needed for Zipcar
            vehicles: 
            [ {
                vehicle:
                {
                    vehicle_id: 902305814,
                    #useless info
                    name: "Calemine", model: "Civic", make: "Honda"
                    (note, still no lat/lon)
                }
              },
              {
                vehicle:
                {
                    vehicle_id: 717453456,
                }
              }
            ]
        '''
        ret_val = []
        try:
            vlist_url = self.vlist_url_template.format(zipcar_domain, key, pod)
            raw = urllib.urlopen(vlist_url)
            vehicle_list = json.load(raw)
            for v in vehicle_list['vehicles']:
                id = v['vehicle']['vehicle_id']
                ret_val.append(id)
        except:
            print 'Exception get_vehicles_at_pod()'
            print traceback.format_exc()

        return ret_val


    def get_pods(self, key, zipcar_domain, loc):
        '''
        {
            locations: 
            [
            {
                location:
                {
                    location_id: 68890170,
                    address_id: 68890167,
                    description: "SE 50th/Belmont",
                    directions: "<p class="Detail">This Zipcar is located in the first on-street parking space west of 50th Avenue on the south (eastbound) side of SE Belmont Street.</p>",
                    private_directions: "<p class="Detail">This Zipcar is located in the first on-street parking space west of 50th Avenue on the south (eastbound) side of SE Belmont Street.</p>",
                    public_transit_url: null,
                    public_transit_stop: "translation missing: en-US.68890170.public_transit_stop"
                }
            },
            ]
        }
        '''
        pod_url = self.pod_url_template.format(zipcar_domain, key, loc)
        raw = urllib.urlopen(pod_url)
        pod_list = json.load(raw)

        pods = []
        for p in pod_list['locations']:
            pod_data = p['location']
            if pod_data != None:
                id = pod_data['location_id']
                pod = ZipcarPod(id)
                pod.set_attributes(pod_data)
                pods.append(pod)

        return pods


