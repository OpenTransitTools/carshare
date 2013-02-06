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

        ''' not crazy about this hack, but ... 
            the __dict__ on a SQLAlchemy object contains hidden crap that we delete from the class dict
        '''
        if set(['_sa_instance_state']).issubset(ret_val):
            del ret_val['_sa_instance_state']

        ''' we're using 'created' as the date parameter, so convert values to strings
            TODO: better would be to detect date & datetime objects, and convert those...
        '''
        if set(['created']).issubset(ret_val):
            ret_val['created'] = ret_val['created'].__str__();

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
        cls.__table__.schema = schema


    def get_session(self):
        Session = sessionmaker(bind=self.db)
        session = Session()
        return session



Base = declarative_base(cls=_Base)
