# Standard library imports...
from http.server import BaseHTTPRequestHandler, HTTPServer
import socket
from threading import Thread


class MockHttpServer(object):

    @property
    def port(self):
        return self._port

    @property
    def url(self):
        return "http://localhost:"+str(self._port)
    
    def __init__(
            self, 
            port=None, 
            handler=None 
        ):
        self._port = port #type: int
        self._handler = handler #type: BaseHTTPRequestHandler
        self._server = None # type: HTTPServer
        self._thread = None # type: Thread

        if not self._handler:
            self._handler = BaseHTTPRequestHandler
        
        if not self._port:
            self._port = self._get_free_port() 


    def _get_free_port(self):
        s = socket.socket(socket.AF_INET, type=socket.SOCK_STREAM)
        s.bind(('localhost', 0))
        #pylint: disable=unused-variable
        address, port = s.getsockname()
        s.close()
        return port


    def start(self):
        self._server = HTTPServer(('localhost', self._port), self._handler)
        self._thread = Thread(target=self._server.serve_forever)
        self._thread.setDaemon(True)
        self._thread.start()

    def stop(self):
        if self._thread:
            self._thread._stop()
