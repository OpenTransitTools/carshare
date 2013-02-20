import math
import inspect

from sqlalchemy import create_engine, event
from sqlalchemy.pool import QueuePool
from sqlalchemy.orm import sessionmaker
#from sqalchemy.func import cos, acos

from ott.carshare.model.base import Base

import logging
logging.basicConfig()
log = logging.getLogger(__file__)
log.setLevel(logging.INFO)

class Database(object):
    '''
    '''

    def __init__(self, url='sqlite:///carshare.db', schema=None, is_geospatial=False, pool_size=20):
        self.url = url
        self.schema = schema
        self.is_geospatial = is_geospatial
        for cls in Base.__subclasses__():
            log.info("db ${0} sees class ${1} in schema ${2}".format(url, cls, schema))
            cls.set_schema(schema)
            if is_geospatial and hasattr(cls, 'add_geometry_column'):
                cls.add_geometry_column()

        self.engine = create_engine(url, poolclass=QueuePool, pool_size=pool_size)
        event.listen(self.engine, 'connect', Database.connection)

    def create(self):
        Base.metadata.drop_all(bind=self.engine)
        Base.metadata.create_all(bind=self.engine)


    def get_session(self):
        Session = sessionmaker(bind=self.engine)
        session = Session()
        return session

    @classmethod
    def make_database_pool(cls):
        log.info("create the db pool")
        return Database()

    tcnt=1
    @classmethod
    def radians(cls, x):
        ''' used for testing...see 'connection' method below
            raw_con.create_function("radians", 1, Database.radians)
        '''
        Database.tcnt = Database.tcnt + 1
        print Database.tcnt
        v = math.radians(x)
        return v

    @classmethod
    def connection(cls, raw_con, connection_record):
        ''' This method is called for each new SQLAlchemy database connection. I'm using it as a connection decorator to
            add math routines to a sqllite database

            @note: check out the call to (above): event.listen(self.engine, 'connect', Database.connection)
            @see:  http://docs.sqlalchemy.org/en/rel_0_8/core/events.html#sqlalchemy.events.PoolEvents
        '''
        if 'sqlite' in type(raw_con).__module__:
            raw_con.create_function("sin",     1, math.sin)
            raw_con.create_function("cos",     1, math.cos)
            raw_con.create_function("acos",    1, math.acos)
            raw_con.create_function("sqrt",    1, math.sqrt)
            raw_con.create_function("pow",     2, math.pow)
            raw_con.create_function("radians", 1, math.radians)
