from sqlalchemy.orm import joinedload
from ott.carshare.model.database import Database
from ott.carshare.model.position import Position
from ott.carshare.model.vehicle  import Vehicle


def latest_positions(session):
    """ return array of positions based on date after querying database
        note we'll include vehicle object  
    """
    positions = session.query(Position).filter(Position.latest==True)
    return positions


def position_history(session, id, limit=1000):
    """ return array of positions for a given vehicle 
    
        SELECT vehicle_id, COUNT(vehicle_id) AS NumOccurrences
        FROM positions
        GROUP BY vehicle_id
        HAVING ( COUNT(vehicle_id) > 1 )
        order by 2 desc
    """
    positions = session.query(Position).filter(Position.vehicle_id==id).limit(limit)
    return positions


def vehicle_information(session, id):
    """ return vehicle info  
    """
    v = session.query(Vehicle).filter(Vehicle.id==id).first()
    return v


def nearest_vehicles(session, lon, lat, dist):
    """ from the 'latest' positions, find 
    """
    v = session.query(Position).\
                filter(Position.latest == True).\
                filter(Position.calc_distance(Position.lon, Position.lat, (lon, lat)) < dist)
    return v


def nearest_positions(session, lon, lat, dist, limit=1000):
    """ from ALL positions (latest and historical), find points 
    """
    p = session.query(Position).filter(Position.calc_distance(Position.lon, Position.lat, (lon, lat)) < dist).limit(limit)
    return p

