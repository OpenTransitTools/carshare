from sqlalchemy import create_engine
from sqlalchemy.pool import QueuePool
from sqlalchemy.orm import sessionmaker

from ott.carshare.model.base import Base

import logging
logging.basicConfig()
log = logging.getLogger(__file__)
log.setLevel(logging.INFO)

class Database(object):

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
