from ott.carshare.model.database import Database

import geojson
from ott.carshare.loader import init_parser
from ott.carshare.model.position import Position

def main():
    args = init_parser()
    db = Database(args.url, args.schema)

    session = db.get_session()
    positions = session.query(Position).all()

    features = []
    for i, p in enumerate(positions):
        f = geojson.Feature(id=i, geometry=geojson.Point(coordinates=(p.lat, p.lon)))
        features.append(f)

    fc = geojson.FeatureCollection(features)
    json = geojson.dumps(fc, sort_keys=True)
    print json

if __name__ == '__main__':
    main()

