import geojson

from ott.carshare.model.database import Database
import ott.carshare.services.queries as q

def latest_position_features(session):
    ''' return geojson
    '''
    features = []
    positions = q.latest_positions(session)
    for i, p in enumerate(positions):
        f = geojson.Feature(id=i, geometry=geojson.Point(coordinates=(p.lon, p.lat)))
        features.append(f)

    fc = geojson.FeatureCollection(features)
    json = geojson.dumps(fc, sort_keys=True)
    return json

def main():
    from ott.carshare.loader import init_parser
    args = init_parser()
    db = Database(args.url, args.schema)
    session = db.get_session()
    json = latest_position_features(session)
    print json

if __name__ == '__main__':
    main()

