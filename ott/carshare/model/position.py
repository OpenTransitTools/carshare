import datetime

from geoalchemy import GeometryColumn, GeometryDDL, Point, WKTSpatialElement
from sqlalchemy import Column, Index, Integer, Numeric, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relation, backref

from ott.carshare.model.base import Base
from ott.carshare.model.vehicle import Vehicle

class Position(Base):
    ''' holds a history of the coordinates of a vehicle...

        IMPORTANT: datetime.datetime.now() is the datestamp used, which is local to where the server is hosted...
                   this could be problematic for a system that's hosted in a place not in the same timezone as the app.
                   If you ever host this app, and want to host in another locale, you should refactor datetime.datetime.now()
                   so that date is UTC based, etc...
    '''
    __tablename__ = 'positions'

    id = Column(Integer, primary_key=True, nullable=False)
    address = Column(String)
    neighborhood = Column(String)
    lat = Column(Numeric(12,9), nullable=False)
    lon = Column(Numeric(12,9), nullable=False)
    created = Column(DateTime, default=datetime.datetime.now())
    updated = Column(DateTime, default=datetime.datetime.now())

    vehicle_id = Column(
        String,
        ForeignKey(Vehicle.id, ondelete='CASCADE'),
        nullable=False
    )
    vehicle = relation(Vehicle, backref=backref('vehicles', order_by=id, cascade="all, delete-orphan"))


    def set_position(self, lat, lon, address=None, neighborhood=None):
        ''' set the lat / lon of this object, and update the timestamp
        '''
        self.lat = lat
        self.lon = lon
        if hasattr(self, 'geom'):
            print "implement geom setting..."
            pass

        self.address = address
        self.neighborhood = neighborhood
        self.updated = datetime.datetime.now()


    @classmethod
    def add_geometry_column(cls):
        cls.geom = GeometryColumn(Point(2))
        GeometryDDL(cls.__table__)


    @classmethod
    def add_geom_to_dict(cls, row):
        wkt = 'SRID=%s;POINT(%s %s)' %(
            SRID,
            row['stop_lon'],
            row['stop_lat']
        )
        row['geom'] = WKTSpatialElement(wkt)

