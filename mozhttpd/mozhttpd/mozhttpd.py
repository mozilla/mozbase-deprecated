#!/usr/bin/env python

# ***** BEGIN LICENSE BLOCK *****
# Version: MPL 1.1/GPL 2.0/LGPL 2.1
#
# The contents of this file are subject to the Mozilla Public License Version
# 1.1 (the "License"); you may not use this file except in compliance with
# the License. You may obtain a copy of the License at
# http://www.mozilla.org/MPL/
#
# Software distributed under the License is distributed on an "AS IS" basis,
# WITHOUT WARRANTY OF ANY KIND, either express or implied. See the License
# for the specific language governing rights and limitations under the
# License.
#
# The Original Code is mozilla.org code.
#
# The Initial Developer of the Original Code is
# the Mozilla Foundation.
# Portions created by the Initial Developer are Copyright (C) 2011
# the Initial Developer. All Rights Reserved.
#
# Contributor(s):
#   Joel Maher <joel.maher@gmail.com>
#
# Alternatively, the contents of this file may be used under the terms of
# either the GNU General Public License Version 2 or later (the "GPL"), or
# the GNU Lesser General Public License Version 2.1 or later (the "LGPL"),
# in which case the provisions of the GPL or the LGPL are applicable instead
# of those above. If you wish to allow use of your version of this file only
# under the terms of either the GPL or the LGPL, and not to allow others to
# use your version of this file under the terms of the MPL, indicate your
# decision by deleting the provisions above and replace them with the notice
# and other provisions required by the GPL or the LGPL. If you do not delete
# the provisions above, a recipient may use your version of this file under
# the terms of any one of the MPL, the GPL or the LGPL.
#
# ***** END LICENSE BLOCK *****

import BaseHTTPServer
import SimpleHTTPServer
import errno
import logging
import threading
import socket
import sys
import os
import urllib
import re
from SocketServer import ThreadingMixIn

class EasyServer(ThreadingMixIn, BaseHTTPServer.HTTPServer):
    allow_reuse_address = True
    acceptable_errors = (errno.EPIPE,) # errno.WSAECONNABORTED) see https://bugzilla.mozilla.org/show_bug.cgi?id=709349#c20

    def handle_error(self, request, client_address):
        error = sys.exc_value

        if isinstance(error, socket.error) and\
           isinstance(error.args, tuple) and\
           error.args[0] in self.acceptable_errors:
            pass  # remote hang up before the result is sent
        else:
            logging.error(error)


class MozRequestHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
    docroot = os.getcwd() # current working directory at time of import

    def _get_handler(self, method):

        return None

    def _try_handler(self, method, postfile=None):
        handlers = [handler for handler in self.urlhandlers if handler['method'] == method]
        for handler in handlers:
            m = re.match(handler['path'], self.path)
            if m:
                if postfile:
                    postdata = postfile.read(int(self.headers.get('Content-length')))
                    (response_code, headerdict, data) = handler['function'](*m.groups(),
                                                                             query=self.query,
                                                                             postdata=postdata)
                else:
                    (response_code, headerdict, data) = handler['function'](*m.groups(),
                                                                             query=self.query)

                self.send_response(response_code)
                for (keyword, value) in headerdict.iteritems():
                    self.send_header(keyword, value)
                self.end_headers()
                self.wfile.write(data)

                return True

        return False


    def do_GET(self):
        if not self._try_handler('GET'):
            if self.docroot:
                SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self)
            else:
                self.send_response(404)
                self.end_headers()
                self.wfile.write('')

    def do_POST(self):
        if not self._try_handler('POST', postfile=self.rfile):
            if self.docroot:
                SimpleHTTPServer.SimpleHTTPRequestHandler.do_POST(self)
            else:
                self.send_response(404)
                self.end_headers()
                self.wfile.write('')

    def do_DEL(self):
        if not self._try_handler('DEL'):
            if self.docroot:
                SimpleHTTPServer.SimpleHTTPRequestHandler.do_DEL(self)
            else:
                self.send_response(404)
                self.end_headers()
                self.wfile.write('')

    def parse_request(self):
        retval = SimpleHTTPServer.SimpleHTTPRequestHandler.parse_request(self)
        if '?' in self.path:
            # we split off the query string, otherwise SimpleHTTPRequestHandler
            # will treat it as PATH_INFO for `translate_path`
            (self.path, self.query) = self.path.split('?', 1)
        else:
            self.query = None

        return retval

    def translate_path(self, path):
        path = path.strip('/').split()
        if path == ['']:
            path = []
        path.insert(0, self.docroot)
        return os.path.join(*path)

    # I found on my local network that calls to this were timing out
    # I believe all of these calls are from log_message
    def address_string(self):
        return "a.b.c.d"

    # This produces a LOT of noise
    def log_message(self, format, *args):
        pass

class MozHttpd(object):
    """
    Very basic HTTP server class. Takes a docroot (path on the filesystem)
    and a set of urlhandler dictionaries of the form:

    {
      'method': HTTP method (string): GET, POST, or DEL,
      'path': PATH_INFO (string),
      'function': function of form fn(arg1, arg2, arg3, ..., querystr) OR
      `           fn(arg1, arg2, arg3, ..., querystr, postdata) if method is
                  'POST'
    }

    and serves HTTP. For each request, MozHttpd will either return a file
    off the docroot, or dispatch to a handler function (if both path and
    method match).

    Note that one of docroot or urlhandlers may be None (in which case no
    local files or handlers, respectively, will be used). If both docroot or
    urlhandlers are None then MozHttpd will default to serving just the local
    directory.
    """

    def __init__(self, host="127.0.0.1", port=8888, docroot=None, urlhandlers=None):
        self.host = host
        self.port = int(port)
        self.docroot = docroot
        if not urlhandlers and not docroot:
            self.docroot = os.getcwd()
        self.httpd = None
        self.urlhandlers = urlhandlers or []

        class MozRequestHandlerInstance(MozRequestHandler):
            docroot = self.docroot
            urlhandlers = self.urlhandlers

        self.handler_class = MozRequestHandlerInstance

    def start(self, block=False):
        """
        Start the server.  If block is True, the call will not return.
        If block is False, the server will be started on a separate thread that
        can be terminated by a call to .stop()
        """
        self.httpd = EasyServer((self.host, self.port), self.handler_class)
        if block:
            self.httpd.serve_forever()
        else:
            self.server = threading.Thread(target=self.httpd.serve_forever)
            self.server.setDaemon(True) # don't hang on exit
            self.server.start()

    def stop(self):
        if self.httpd:
            self.httpd.shutdown()
        self.httpd = None

    __del__ = stop


def main(args=sys.argv[1:]):
    
    # parse command line options
    from optparse import OptionParser
    parser = OptionParser()
    parser.add_option('-p', '--port', dest='port', 
                      type="int", default=8888,
                      help="port to run the server on [DEFAULT: %default]")
    parser.add_option('-H', '--host', dest='host',
                      default='127.0.0.1',
                      help="host [DEFAULT: %default]")
    parser.add_option('-d', '--docroot', dest='docroot',
                      default=os.getcwd(),
                      help="directory to serve files from [DEFAULT: %default]")
    options, args = parser.parse_args(args)
    if args:
        parser.print_help()
        parser.exit()

    # create the server
    kwargs = options.__dict__.copy()
    server = MozHttpd(**kwargs)

    print "Serving '%s' at %s:%s" % (server.docroot, server.host, server.port)
    server.start(block=True)

if __name__ == '__main__':
    main()
