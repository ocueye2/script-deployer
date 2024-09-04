import cherrypy

class HelloWorld(object):
    @cherrypy.expose
    def index(self):
        return "This is an exampe service running at 4212"
cherrypy.config.update({
        'server.socket_port': 4212,
        'log.screen': True  # Disable console logging
    })
cherrypy.quickstart(HelloWorld())