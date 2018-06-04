import argparse
import os
import logging
log = logging.getLogger(__file__)

from ott.carshare.model.database import Database
from ott.carshare.model.update_controller import UpdateController


def init_parser():
    parser = argparse.ArgumentParser(
        prog='controller',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument(
        '--car2go_key',
        '--ckey',
        '-ckey',
        '-ck',
        help="car2go api key"
    )
    parser.add_argument(
        '--zipcar_key',
        '--zkey',
        '-zkey',
        '-zk',
        help="ZipCar api key"
    )
    parser.add_argument(
        '--car2go_region',
        '--cregion',
        '-cregion',
        '-cr',
        default='portland',
        help="car2go region id"
    )
    parser.add_argument(
        '--zipcar_region',
        '--zregion',
        '-zregion',
        '-zr',
        default='portland',
        help="car2go region id"
    )
    parser.add_argument(
        '--database_url',
        '-url',
        '-u',
        '-d',
        required='true',
        help="(geo) database url ala dialect+driver://user:password@host/dbname[?key=value..]"
    )
    parser.add_argument(
        '--schema',
        '-schema',
        '-s',
        help="database schema"
    )
    parser.add_argument(
        '--geo',
        '-geo',
        '-g',
        action="store_true",
        help="add geometry columns"
    )
    parser.add_argument(
        '--create',
        '-create',
        '-c',
        action="store_true",
        help="drop / create database tables for vehicles"
    )
    args = parser.parse_args()
    return args


def main():
    #import pdb; pdb.set_trace()
    args = init_parser()
    print args
    return 1111111

    db = Database(args.database_url, args.schema, args.geo)
    if args.create:
        db.create()
    UpdateController().update_children(db, args)


if __name__ == '__main__':
    main()

