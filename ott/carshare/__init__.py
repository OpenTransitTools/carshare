__import__('pkg_resources').declare_namespace(__name__)

import os
from pyramid.config import Configurator
from pyramid.events import subscriber
from pyramid.events import ApplicationCreated
from pyramid.events import NewRequest

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)

    from ott.carshare.services.pyramid_app import carshare_static_config, carshare_view_config 
    carshare_static_config(config)
    carshare_view_config(config)

    config.scan()
    return config.make_wsgi_app()

@subscriber(ApplicationCreated)
def application_created_subscriber(event):
    ''' what do i do?

        I'm called at startup of the Pyramid app.  
    '''
    #log.info('Starting pyramid server -- visit me on http://localhost:8080')
    print event

@subscriber(NewRequest)
def new_request_subscriber(event):
    ''' what do i do?
       1. entry point for a new server request
       2. configure the request context object (can insert new things like db connections or authorization to pass around in this given request context)
    '''
    #log.debug("new request called -- request is 'started'")
    request = event.request
    request.BASE_DIR = os.path.dirname(os.path.realpath(__file__))


