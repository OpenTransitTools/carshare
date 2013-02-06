import abc
import datetime
from sqlalchemy import Column, Index, Integer, Numeric, String, DateTime
from sqlalchemy.sql import func, and_

from ott.carshare.model.base import Base

class Vehicle(Base):
    __tablename__ = 'vehicles'

    id = Column(String, primary_key=True, nullable=False)
    carshare_company = Column(String, nullable=False)
    name = Column(String)
    created = Column(DateTime, default=datetime.datetime.now())
    updated = Column(DateTime, default=datetime.datetime.now())

    __mapper_args__ = {
            'polymorphic_on': carshare_company,
            'polymorphic_identity': __tablename__,
            'with_polymorphic':'*'
    }

    @abc.abstractmethod
    def set_attributes(self, dict):
        ''' copy known values from the dict into this object, then update the timestamp
        '''
        raise NotImplementedError("Please implement this method")


    def update_position(self, session, lat, lon, address=None, neighborhood=None, time_span=8):
        ''' query the db for a position for this vehicle ... if the vehicle appears to be parked in the
            same place as an earlier update, update the 
            NOTE: the position add/update needs to be committed to the db by the caller of this method 
        '''
        from ott.model.carshare.position import Position

        # step 1: get position object from db ...criteria is to find last position 
        #          update within an hour, and the car hasn't moved lat,lon
        hours_ago = datetime.datetime.now() - datetime.timedelta(hours=time_span)
        p = session.query(Position).filter(
                   and_(
                        Position.vehicle_id == self.id,
                        Position.updated >= hours_ago,
                        Position.lat == lat,
                        Position.lon == lon,
                    ) 
                ).first()

        # step 2: we didn't find an existing position in the Position history table, so add a new one 
        if p is None:
            p = Position()
            p.vehicle_id = self.id
            session.add(p)

        # step 3: update the position record
        p.set_position(lat, lon, address, neighborhood)

        return p


