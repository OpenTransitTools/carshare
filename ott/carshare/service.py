from ott.carshare.model.database import Database

import geojson
from ott.carshare.loader import init_parser

def main():
    args = init_parser()
    print args
    db = Database(args.url, args.schema)

    f1 = geojson.Feature(id=1, geometry=geojson.Point(coordinates=(53.04781795911469, -4.10888671875)))
    f2 = geojson.Feature(id=2, geometry=geojson.Point(coordinates=(53.04781795911469, -4.10888671875)))
    f  = [f1, f2]
    fc = geojson.FeatureCollection(f)
    json = geojson.dumps(fc, sort_keys=True)
    print json

if __name__ == '__main__':
    main()

