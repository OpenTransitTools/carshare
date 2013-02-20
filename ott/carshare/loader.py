import argparse
import os

from ott.carshare.model.database import Database
from ott.carshare.model.position import Position
from ott.carshare.model.car2go.car2go_vehicle   import Car2GoVehicle
from ott.carshare.model.car2go.update_positions import UpdatePositions
from ott.carshare.model.zipcar.update_positions import ZipcarPodsAndVehicles

from ott.carshare.model.zipcar.zipcar_vehicle import ZipcarPod
from ott.carshare.model.zipcar.zipcar_vehicle import ZipcarVehicle


import logging
logging.basicConfig()
log = logging.getLogger(__file__)
log.setLevel(logging.INFO)

def init_parser():
    parser = argparse.ArgumentParser(
        prog='controller',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument(
        '--key', 
        '-key',
        '-k',
        required='true',
        help="car2go consumer key (id)"
    )
    parser.add_argument(
        '--secret', 
        '-secret',
        '-ss',
        help="car2go 'shared secret' code"
    )
    parser.add_argument(
        '--url', 
        '-url',
        '-u',
        required='true',
        help="(geo) database url ala dialect+driver://user:password@host/dbname[?key=value..] ... or simply"
    )
    parser.add_argument(
        '--schema', 
        '-schema',
        '-s',
        help="database schema"
    )
    parser.add_argument(
        '--create', 
        '-create',
        '-c',
        action="store_true",
        help="drop / create database tables for vehicles"
    )
    parser.add_argument(
        '--zipcar', 
        '-zipcar',
        '-z',
        help="zipcar domain"
    )
    args = parser.parse_args()
    return args


def main():
    args = init_parser()
    print args
    db = Database(args.url, args.schema)
    if args.create:
        db.create()
    u = UpdatePositions(db, args.key)
    if args.zipcar is not None:
        z = ZipcarPodsAndVehicles(db, args.key, args.zipcar)

if __name__ == '__main__':
    main()

