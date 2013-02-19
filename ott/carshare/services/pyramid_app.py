import os
import shutil
import simplejson as json

from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.response import Response
from pyramid.view import view_config
from pyramid.decorator import reify

from ott.carshare.model.database import Database
import ott.carshare.services.carshare as ws

db = Database.make_database_pool()

@view_config(route_name='default_index', renderer='index.html')
def index(request):
    return {'project': 'CarShare'}


@view_config(route_name='vehicle_ws', renderer='json')
def vehicle_information(request):
    ''' return the latest carshare positions as geojson
    '''
    id  = get_first_param(request, 'id')
    if id:
        ses = db.get_session()
        ret_val = ws.vehicle_information(ses, id)
    else:
        ret_val = json_message('You need to specify an "id" parameter as a request parameter')

    if ret_val is None:
        ret_val = json_message()

    ret_val = Response(ret_val)
    return ret_val


@view_config(route_name='history_ws', renderer='json')
def position_history(request):
    ''' return the latest carshare positions as geojson
    '''
    id  = get_first_param(request, 'id')
    if id:
        ses = db.get_session()
        ret_val = ws.vehicle_position_history_geojson(ses, id)
    else:
        ret_val = json_message('You need to specify an "id" parameter as a request parameter')

    if ret_val is None:
        ret_val = json_message()

    ret_val = Response(ret_val)
    return ret_val


@view_config(route_name='positions_ws', renderer='json')
def positions(request):
    ''' return the latest carshare positions as geojson
    '''
    ses = db.get_session()
    ret_val = ws.latest_positions_geojson(ses)
    return Response(ret_val)


@view_config(route_name='mock_positions_ws', renderer='json')
def mock_positions(request):
    ''' stream a mock .json file out in the response
    '''
    response = request.response
    response.app_iter = open(request.BASE_DIR + '/static/js/mock/collection.json', 'r')
    return response


def carshare_static_config(config):
    ''' config the static folders
    '''
    cache_age=3600
    config.add_static_view('static', 'static',          cache_max_age=cache_age)
    config.add_static_view('js',     'static/js',       cache_max_age=cache_age)
    config.add_static_view('css',    'static/css',      cache_max_age=cache_age)
    config.add_static_view('images', 'static/images',   cache_max_age=cache_age)

    # important ... allow .html extension on mako templates
    config.add_renderer(".html", "pyramid.mako_templating.renderer_factory")


def carshare_view_config(config):
    ''' config the different views...
    '''
    config.add_route('default_index',      '/')
    config.add_route('vehicle_ws',         '/vehicle')
    config.add_route('positions_ws',       '/positions')
    config.add_route('history_ws',         '/history')
    config.add_route('mock_positions_ws',  '/mock_positions')


def get_first_param(request, name, def_val=None):
    '''
        utility function

        @return the first value of the named http param (remember, http can have multiple values for the same param name), 
        or def_val if that param was not sent via HTTP
    '''
    ret_val=def_val
    try:
        ret_val = request.params.getone(name)
    except:
        pass

    return ret_val


def json_message(msg="Something's wrong...sorry!"):
    return {error:True, msg:msg}


if __name__ == '__main__':
    config = Configurator()
    carshare_view_config(config)
    app = config.make_wsgi_app()
    server = make_server('0.0.0.0', 8080, app)
    server.serve_forever()
