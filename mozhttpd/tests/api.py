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
# Portions created by the Initial Developer are Copyright (C) 2012
# the Initial Developer. All Rights Reserved.
#
# Contributor(s):
#   William Lachance <wlachance@mozilla.com>
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

import mozhttpd
import urllib2
import os
import unittest
import re
import json

here = os.path.dirname(os.path.abspath(__file__))

class ApiTest(unittest.TestCase):
    resource_get_called = 0
    resource_post_called = 0
    resource_del_called = 0

    @mozhttpd.handlers.json_response
    def resource_get(self, objid, query):
        self.resource_get_called += 1
        return (200, { 'called': self.resource_get_called,
                       'id': objid,
                       'query': query })

    @mozhttpd.handlers.json_response
    def resource_post(self, query, postdata=None):
        self.resource_post_called += 1
        return (201, { 'called': self.resource_post_called,
                       'data': json.loads(postdata),
                       'query': query })

    @mozhttpd.handlers.json_response
    def resource_del(self, objid, query):
        self.resource_del_called += 1
        return (200, { 'called': self.resource_del_called,
                       'id': objid,
                       'query': query })

    def get_url(self, path, server_port, querystr):
        url = "http://127.0.0.1:%s%s" % (server_port, path)
        if querystr:
            url += "?%s" % querystr
        return url

    def try_get(self, server_port, querystr):
        self.resource_get_called = 0

        f = urllib2.urlopen(self.get_url('/api/resource/1', server_port, querystr))
        self.assertEqual(f.getcode(), 200)
        self.assertEqual(json.loads(f.read()), { 'called': 1, 'id': str(1), 'query': querystr })
        self.assertEqual(self.resource_get_called, 1)

    def try_post(self, server_port, querystr):
        self.resource_post_called = 0

        postdata = { 'hamburgers': '1234' }
        f = urllib2.urlopen(self.get_url('/api/resource/', server_port, querystr),
                            data=json.dumps(postdata))
        self.assertEqual(f.getcode(), 201)
        self.assertEqual(json.loads(f.read()), { 'called': 1,
                                                 'data': postdata,
                                                 'query': querystr })
        self.assertEqual(self.resource_post_called, 1)

    def try_del(self, server_port, querystr):
        self.resource_del_called = 0

        opener = urllib2.build_opener(urllib2.HTTPHandler)
        request = urllib2.Request(self.get_url('/api/resource/1', server_port, querystr))
        request.get_method = lambda: 'DEL'
        f = opener.open(request)

        self.assertEqual(f.getcode(), 200)
        self.assertEqual(json.loads(f.read()), { 'called': 1, 'id': str(1), 'query': querystr })
        self.assertEqual(self.resource_del_called, 1)

    def test_api(self):
        httpd = mozhttpd.MozHttpd(port=0,
                                  urlhandlers = [ { 'method': 'GET',
                                                    'path': '/api/resource/([^/]+)/?',
                                                    'function': self.resource_get },
                                                  { 'method': 'POST',
                                                    'path': '/api/resource/?',
                                                    'function': self.resource_post },
                                                  { 'method': 'DEL',
                                                    'path': '/api/resource/([^/]+)/?',
                                                    'function': self.resource_del }
                                                  ])
        httpd.start(block=False)

        server_port = httpd.httpd.server_port

        # GET
        self.try_get(server_port, None)
        self.try_get(server_port, '?foo=bar')

        # POST
        self.try_post(server_port, None)
        self.try_post(server_port, '?foo=bar')

        # DEL
        self.try_del(server_port, None)
        self.try_del(server_port, '?foo=bar')

        # By default we don't serve any files if we just define an API
        f = None
        try:
            f = urllib2.urlopen(self.get_url('/', server_port, None))
        except urllib2.HTTPError, e:
            self.assertEqual(e.code, 404)

    def test_api_with_docroot(self):
        httpd = mozhttpd.MozHttpd(port=0, docroot=here,
                                  urlhandlers = [ { 'method': 'GET',
                                                    'path': '/api/resource/([^/]+)/?',
                                                    'function': self.resource_get } ])
        httpd.start(block=False)
        server_port = httpd.httpd.server_port

        # We defined a docroot, so we expect a directory listing
        f = urllib2.urlopen(self.get_url('/', server_port, None))
        self.assertEqual(f.getcode(), 200)
        self.assertTrue('Directory listing for' in f.read())

        # Make sure API methods still work
        self.try_get(server_port, None)
        self.try_get(server_port, '?foo=bar')


if __name__ == '__main__':
    unittest.main()
