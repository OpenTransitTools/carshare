import datetime
from sqlalchemy.ext.declarative import declarative_base

class _Base(object):

    @classmethod
    def get_attribute(cls, dict, id):
        ''' safely get an attribute from a dict, returning None if that attribute is not in the dict
        '''
        ret_val = None
        try:
            ret_val = dict[id]
        except:
            #try:
            #    ret_val = dict id
            pass
        return ret_val

    @classmethod
    def from_dict(cls, attrs):
        clean_dict = cls.make_record(attrs)
        c = cls(**clean_dict)
        return c


    def to_dict(self):
        ''' convert a SQLAlchemy object into a dict that is serializable to JSON
        ''' 
        ret_val = self.__dict__.copy()

        # the __dict__ on a SQLAlchemy object contains hidden crap that we delete from the class dict
        # (not crazy about this hack, but ...) 
        if set(['_sa_instance_state']).issubset(ret_val):
            del ret_val['_sa_instance_state']

        # convert time, date & datetime, etc... objects to iso formats
        for k in ret_val.keys():
            v = ret_val[k] 
            if hasattr(v,"isoformat"):
                ret_val[k] = v.isoformat()

        return ret_val


    @classmethod
    def to_dict_list(cls, list):
        ''' apply to_dict() to all elements in list, and return new / resulting list...
        '''
        ret_val = []
        for l in list:
            if hasattr(l,"to_dict"):
                l = l.to_dict()
            ret_val.append(l)
        return ret_val

    @classmethod
    def bulk_load(cls, engine, records, remove_old=True):
        ''' load a bunch of records at once from a list (first clearing out the table).
            note that the records array has to be dict structures, ala
            http://docs.sqlalchemy.org/en/latest/core/connections.html#sqlalchemy.engine.Connection.execute
        '''
        table = cls.__table__
        if remove_old:
            engine.execute(table.delete())
        engine.execute(table.insert(), records)


    @classmethod
    def set_schema(cls, schema):
        # if this is a database table, set the schema
        if hasattr(cls, '__table__'):
            cls.__table__.schema = schema

        # bit of recursion to hit sub classes
        for c in cls.__subclasses__():
            c.set_schema(schema)




def get_session(self):
        Session = sessionmaker(bind=self.db)
        session = Session()
        return session


Base = declarative_base(cls=_Base)
