import datetime
import geojson

from geoalchemy import GeometryColumn, GeometryDDL, Point, WKTSpatialElement
from sqlalchemy import Column, Index, Integer, Numeric, String, Boolean, DateTime, ForeignKey, ForeignKeyConstraint
from sqlalchemy.sql import func, and_
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
    latest  = Column(Boolean,  default=False)

    vehicle_id  = Column(String, nullable=False)
    carshare_co = Column(String, nullable=False)

    __table_args__ = (
        ForeignKeyConstraint(
              [vehicle_id, carshare_co],
              [Vehicle.id, Vehicle.carshare_company]),
              {}
    )

    vehicle = relation(Vehicle, backref=backref('vehicles', order_by=id, cascade="all, delete-orphan"))

    def set_position(self, lat, lon, address=None, neighborhood=None):
        ''' set the lat / lon of this object, and update the timestamp and 'latest' status (to True)
        '''
        self.lat = lat
        self.lon = lon
        if hasattr(self, 'geom'):
            print "implement geom setting..."
            pass

        self.address = address
        self.neighborhood = neighborhood
        self.updated = datetime.datetime.now()
        self.latest  = True


    @classmethod
    def clear_latest_column(cls, session, car_co='car2go'):
        ''' set all latest=True positions to false (for a give car company)
        '''
        session.query(Position).filter(and_(Position.latest == True, Position.carshare_co == car_co)
                              ).update({"latest":False}, synchronize_session=False)


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


    @classmethod
    def to_geojson_features(cls, positions):
        ''' loop through list of Position objects and turn them into geojson features
        '''
        ret_val = []
        for i, p in enumerate(positions):
            td = p.updated - p.created
            el = (td.microseconds + (td.seconds + td.days * 24 * 3600) * 10**6) / 10**6
            properties = {
                'position_id' : p.id,
                'vehicle_id'  : p.vehicle_id,
                'carshare_co' : p.carshare_co,
                'created'     : p.created.isoformat(),
                'updated'     : p.updated.isoformat(),
                'elapsed'     : el
            }
            geo = geojson.Point(coordinates=(p.lon, p.lat))
            f = geojson.Feature(id=i+1, properties=properties, geometry=geo)
            ret_val.append(f)
    
        return ret_val
