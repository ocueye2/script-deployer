import cherrypy

class HelloWorld(object):
    @cherrypy.expose
    def index(self):
        return "Hello World!"

if __name__ == '__main__':
    # Set up the server configuration to listen on port 1111
    cherrypy.config.update({
        'server.socket_port': 1234,
        'log.screen': True  # Disable console logging
    })
    cherrypy.quickstart(HelloWorld())