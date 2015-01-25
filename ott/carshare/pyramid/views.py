import logging
log = logging.getLogger(__file__)

import StringIO
import re

from pyramid.request import Request
from pyramid.response import Response
from pyramid.httpexceptions import HTTPFound

from pyramid.view import view_config
from pyramid.config import Configurator
from pyramid.session import UnencryptedCookieSessionFactoryConfig

from pyramid.events import NewRequest
from pyramid.events import ApplicationCreated
from pyramid.events import subscriber


def do_view_config(config):
    ''' adds the views (see below) and static directories to pyramid's config
    '''

    # routes setup
    config.add_route('index',                           '/')


@view_config(route_name='index', renderer='index.html')
def index_view(request):
    return {}


@subscriber(ApplicationCreated)
def application_created_subscriber(event):
    '''
       what do i do?

       1. I'm called at startup of the Pyramid app.  
       2. I could be used to make db connection (pools), etc...
    '''
    log.info('Starting pyramid server...')


@subscriber(NewRequest)
def new_request_subscriber(event):
    '''
       what do i do?

       1. entry point for a new server request
       2. configure the request context object (can insert new things like db connections or authorization to pass around in this given request context)
    '''
    log.debug("new request called -- request is 'started'")
    request = event.request
    request.model = get_model(request)
    settings = request.registry.settings
    request.add_finished_callback(cleanup)

@view_config(context='pyramid.exceptions.NotFound', renderer='notfound.mako')
def notfound_view(self):
    '''
        render the notfound.mako page anytime a request comes in that 
        the app does't have mapped to a page or method
    '''
    return {}


##
## view utils
##

def cleanup(request):
    '''
       what do i do?

       1. I was configured via the new_request_subscriber(event) method
       2. I'm called via a server event (when a request is 'finished')
       3. I could do random cleanup tasks like close database connections, etc... 
    '''
    log.debug("cleanup called -- request is 'finished'")


def forward_request(request, path, query_string=None, extra_params=None):
    # http://ride.trimet.org?mapit=I&submit&${plan['params']['map_planner']}
    # def map_url_params(self, fmt="from={frm}&to={to}&time={time}&maxHours={max_hours}&date={month}/{day}/{year}&mode={mode}&optimize={optimize}&maxWalkDistance={walk_meters:.0f}&arriveBy={arrive_depart}"):
    return HTTPFound(location=path)

def make_subrequest(request, path, query_string=None, extra_params=None):
    ''' create a subrequest to call another page in the app...
        http://docs.pylonsproject.org/projects/pyramid/en/latest/narr/subrequest.html
    '''
    # step 1: make a new request object...
    path = get_path(request, path)
    subreq = Request.blank(path)

    # step 2: default to request's querystring as default qs
    if query_string is None:
        query_string = request.query_string

     # step 3: pre-pend any extra stuff to our querytring
    if extra_params:
        newqs = extra_params
        if len(query_string) > 0:
            newqs = newqs + "&" + query_string
        query_string = newqs

    # step 4: finish the qs crap, and call this sucker...
    subreq.query_string = query_string
    ret_val = request.invoke_subrequest(subreq)
    return ret_val
