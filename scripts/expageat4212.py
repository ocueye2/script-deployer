import cherrypy

class HelloWorld(object):
    @cherrypy.expose
    def index(self):
        return "test"
cherrypy.config.update({
        'server.socket_port': 4212,
        'log.screen': True  # Disable console logging
    })
cherrypy.quickstart(HelloWorld())