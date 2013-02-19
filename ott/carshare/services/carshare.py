import geojson
import simplejson as json

import ott.carshare.model.queries as q
from   ott.carshare.model.position import Position

def latest_positions_geojson(session):
    ''' return geojson of latest vehicle positions 
    '''
    positions = q.latest_positions(session)
    features = Position.to_geojson_features(positions)
    ret_val = features_to_json(features)
    return ret_val


def vehicle_information(session, id):
    ''' return vehicle data as json
    '''
    v = q.vehicle_information(session, id)
    v = v.to_dict()
    p = q.position_history(session, id)
    p = Position.to_dict_list(p)
    v['positions'] = p
    ret_val = json.dumps(v)
    return ret_val


def vehicle_position_history_geojson(session, id):
    ''' return geojson of latest positions
    '''
    positions = q.position_history(session, id)
    features = Position.to_geojson_features(positions)
    ret_val = features_to_json(features)
    return ret_val


def features_to_json(features):
    ''' convert list of geojson.Feature() object to a feature collection, stream dumped to a string
    '''
    fc = geojson.FeatureCollection(features)
    json_string = geojson.dumps(fc, sort_keys=True)
    return json_string


def main():
    from ott.carshare.model.database import Database
    from ott.carshare.loader import init_parser
    args = init_parser()
    db = Database(args.url, args.schema)
    session = db.get_session()
    p = latest_positions_geojson(session)
    print p

if __name__ == '__main__':
    main()

