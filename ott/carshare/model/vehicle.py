import logging
log = logging.getLogger(__file__)

import abc
import datetime
from sqlalchemy import Column, Index, Integer, Numeric, String, DateTime
from sqlalchemy.sql import func, and_

from ott.carshare.model.base import Base
from ott.carshare.model.position import Position

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


    def update_position(self, session, lat, lon, address=None, city=None, state=None, zipcode=None, time_span=144):
        ''' query the db for a position for this vehicle ... if the vehicle appears to be parked in the
            same place as an earlier update, update the 
            NOTE: the position add/update needs to be committed to the db by the caller of this method 
        '''

        # step 0: cast some variables
        pid = str(self.id)
        lat = round(lat, 6)
        lon = round(lon, 6)


        # step 1: get position object from db ...criteria is to find last position 
        #          update within an hour, and the car hasn't moved lat,lon
        hours_ago = datetime.datetime.now() - datetime.timedelta(hours=time_span)
        p = None
        try:
            q = session.query(Position).filter(
                       and_(
                            Position.vehicle_id == pid,
                            Position.updated >= hours_ago,
                            Position.lat == lat,
                            Position.lon == lon,
                        ) 
                    )
            p = q.first()
            #import pdb; pdb.set_trace()
        except Exception, err:
            log.exception('Exception: {0}'.format(err))

        # step 2: we didn't find an existing position in the Position history table, so add a new one
        try: 
            if p is None:
                p = Position()
                p.vehicle_id  = pid
                p.carshare_co = str(self.carshare_company)
                p.set_position(lat, lon, address, city, state, zipcode)
                session.add(p)
            else:
                # step 3: update the position record if need be
                p.set_position(lat, lon, address, city, state, zipcode)
        except Exception, err:
            log.exception('Exception: {0}, committing position to db for vehicle id={1}, lat={2}, lon={3}'.format(err, p.vehicle_id, lat, lon))
            session.rollback()
        finally:
            try:
                session.commit()
                session.flush()
            except:
                session.rollback()

        return p



def main():
    p = Position()

if __name__ == '__main__':
    main()
