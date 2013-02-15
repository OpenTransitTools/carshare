import geojson

import ott.carshare.services.queries as q

def features_to_json(features):
    ''' convert list of geojson.Feature() object to a feature collection, stream dumped to a string
    '''
    fc = geojson.FeatureCollection(features)
    json_string = geojson.dumps(fc, sort_keys=True)
    return json_string


def latest_positions_geojson(session):
    ''' return geojson of latest vehicle positions 
    '''
    positions = q.latest_positions(session)
    features = []
    for i, p in enumerate(positions):
        properties = {
            'position_id': p.id,
            'vehicle_id' : p.vehicle.id,
            'company'    : p.vehicle.carshare_company
        }
        geo = geojson.Point(coordinates=(p.lon, p.lat))
        f = geojson.Feature(id=i+1, properties=properties, geometry=geo)
        features.append(f)

    json = features_to_json(features)
    return json


def vehicle_history_geojson(session, vid):
    ''' return geojson of latest positions
    
        SELECT vehicle_id, COUNT(vehicle_id) AS NumOccurrences
        FROM positions
        GROUP BY vehicle_id
        HAVING ( COUNT(vehicle_id) > 1 )
        order by 2 desc
    '''
    positions = q.latest_positions(session)
    features = []
    for i, p in enumerate(positions):
        properties = {
            'position_id': p.id,
            'vehicle_id' : p.vehicle.id,
            'company'    : p.vehicle.carshare_company
        }
        geo = geojson.Point(coordinates=(p.lon, p.lat))
        f = geojson.Feature(id=i+1, properties=properties, geometry=geo)
        features.append(f)

    json = features_to_json(features)
    return json


def main():
    from ott.carshare.model.database import Database
    from ott.carshare.loader import init_parser
    args = init_parser()
    db = Database(args.url, args.schema)
    session = db.get_session()
    json = latest_positions_geojson(session)
    print json

if __name__ == '__main__':
    main()

