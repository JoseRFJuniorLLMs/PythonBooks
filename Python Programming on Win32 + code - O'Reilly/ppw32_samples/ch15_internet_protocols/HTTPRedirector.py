# HTTPRedirector.py

# A HTTP Server that redirects all requests to a named, remote server.

# BaseHTTPServer provides the basic HTTP Server functionality.
import BaseHTTPServer

# httplib is used to establish our connection to the remote server
import httplib

import socket # For the error!

# The server we are redirecting to.
g_RemoteServerName = "www.python.org"

class HTTPRedirector(BaseHTTPServer.BaseHTTPRequestHandler):
    # This function is called when a client makes a GET request
    # ie, it wants the headers, and the data.
    def do_GET(self):
        srcfile = self.send_headers("GET")
        if srcfile:
            # Copy the data from the remote server
            # back to the client.
            BLOCKSIZE = 8192
            while 1:
                # Read a block from the remote.
                data = srcfile.read(BLOCKSIZE)
                if not data: break
                self.wfile.write(data)

            srcfile.lose()

    # This function is called when a client makes a HEAD request
    # ie, it only wants the headers, not the data.
    def do_HEAD(self):
        srcfile = self.send_headers("HEAD")
        if srcfile:
            srcfile.close()
    
    # A private function which handles all the redirection logic.
    def send_headers(self, request):
        # Establish a remote connection
        try:
            http = httplib.HTTP(g_RemoteServerName)
        except socket.error, problem:
            print "Error - Cannot connect to %s: %s" \
                   % (g_RemoteServerName, problem)
            return
        # Re-send all the headers we retrieved in the request.
        http.putrequest(request, self.path)
        for header, val in self.headers.items():
            http.putheader(header, val)
        http.endheaders()
        # Now get the response from the remote server
        errcode, errmsg, headers = http.getreply()
        self.send_response(errcode, errmsg)
        # Send the headers back to the client.
        for header, val in headers.items():
            self.send_header(header, val)
        self.end_headers()
        if errcode==200:
            return http.getfile()

if __name__=='__main__':
    print "Redirecting HTTP requests to", g_RemoteServerName
    BaseHTTPServer.test(HTTPRedirector)
