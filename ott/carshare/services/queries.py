from sqlalchemy.orm import joinedload
from ott.carshare.model.database import Database
from ott.carshare.model.position import Position
from ott.carshare.model.vehicle  import Vehicle

def latest_positions(session):
    ''' return array of positions based on date after querying database
        note we'll include vehicle object  
    '''
    positions = session.query(Position).options(joinedload('vehicle')).all()
    return positions