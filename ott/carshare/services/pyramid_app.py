import os
import shutil

from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.response import Response
from pyramid.view import view_config
from pyramid.decorator import reify

from ott.carshare.model.database import Database
import ott.carshare.services.carshare as ws

def get_database_pool():
    print "create the db pool"
    return Database()

db = get_database_pool()

@view_config(route_name='default_index', renderer='index.html')
def index(request):
    return {'project': 'CarShare'}


@view_config( route_name='positions_ws', renderer='json')
def positions(request):
    ''' return the latest carshare positions as geojson
    '''
    ses = db.get_session()
    json = ws.latest_positions_geojson(ses)
    return Response(json)


@view_config( route_name='positions_ws', renderer='json')
def positions(request):
    ''' return the latest carshare positions as geojson
    '''
    ses = db.get_session()
    json = ws.latest_positions_geojson(ses)
    return Response(json)


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
    config.add_route('default_index', '/')
    config.add_route('positions_ws',  '/positions')
    config.add_route('mock_positions_ws',  '/mock_positions')


if __name__ == '__main__':
    config = Configurator()
    carshare_view_config(config)
    app = config.make_wsgi_app()
    server = make_server('0.0.0.0', 8080, app)
    server.serve_forever()
