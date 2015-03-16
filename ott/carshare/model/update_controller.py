''' base class for calling update objects
    step 1: in all objects that you want to blindly call an update on should inherit from this class
    step 2: put the import to that class file in the method update_children() below
'''

from ott.carshare.model.base import Base

class UpdateController(object):
    def __init__(self):
        pass

    @classmethod
    def update(cls, db, args):
        pass

    @classmethod
    def update_children(cls, db, args):
        ''' update children
        '''
        from ott.carshare.model.update_controller import UpdateController
        import ott.carshare.model.zipcar.update_positions
        import ott.carshare.model.car2go.update_positions

        for child in UpdateController.__subclasses__():
            child.update(db, args)

def main():
    UpdateController.update_children()

if __name__ == '__main__':
    main()
