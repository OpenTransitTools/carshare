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
        action="store_true",
        help="load/update zipcar data"
    )
    args = parser.parse_args()
    return args


def main():
    #import pdb; pdb.set_trace()
    args = init_parser()
    print args
    db = Database(args.url, args.schema)
    if args.create:
        db.create()
    UpdateController().update_children(db, args)

if __name__ == '__main__':
    main()

