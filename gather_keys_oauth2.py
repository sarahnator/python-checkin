#!/usr/bin/env python
import cherrypy
import os
import sys
import threading
import traceback
import webbrowser

import urllib.request
import requests_oauthlib
from urllib.parse import urlparse
from base64 import b64encode
from fitbit.api import Fitbit
from oauthlib.oauth2.rfc6749.errors import MismatchingStateError, MissingTokenError


class OAuth2Server:
    def __init__(self, client_id, client_secret,
                 redirect_uri='http://127.0.0.1:8080/'):
        """ Initialize the FitbitOauth2Client """
        self.success_html = """
            <h1>You are now authorized to access the Fitbit API!</h1>
            <br/><h3>You can close this window</h3>"""
        self.failure_html = """
            <h1>ERROR: %s</h1><br/><h3>You can close this window</h3>%s"""

        self.fitbit = Fitbit(
            client_id,
            client_secret,
            redirect_uri=redirect_uri,
            # timeout=10,
        )

        self.redirect_uri = redirect_uri
    def emptyFunc(self):
            pass
    def browser_authorize(self):
        """
        Open a browser to the authorization url and spool up a CherryPy
        server to accept the response
        """
        url, _ = self.fitbit.client.authorize_token_url()
        # Open the web browser in a new thread for command-line browser support

        threading.Timer(1, webbrowser.open, args=(url,)).start()
        # eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIyMkJMRkMiLCJzdWIiOiI4SjM4SjMiLCJpc3MiOiJGaXRiaXQiLCJ0eXAiOiJhY2Nlc3NfdG9rZW4iLCJzY29wZXMiOiJyc29jIHJhY3QgcnNldCBybG9jIHJ3ZWkgcmhyIHJudXQgcnBybyByc2xlIiwiZXhwIjoxNjIyMDg0NzcxLCJpYXQiOjE1OTA1NDg4Nzl9.G0iELADLB5ugwQHDFjruaWJliAYyEnpHBJwR_nG1koo
        
        # #fix 403 error
        # headers = {
        #     'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36',
        #     'From': 'almundbutter@gmail.com'
        # }
        # response = requests.get(url, headers=headers)

        # response = urllib.request.urlopen(url)
        # html = response.read()

        # request = urllib.request.Request(url, headers='')
        # opener = urllib.request.build_opener()
        # response = opener.open(request)

        # 127.0.0.1 - "GET /?code=d841e15f7fdb5069affa89fc8a118ef6cab6fc34&state=10SOQorAqsTwrt9p93Kh14gkWyZxfA HTTP/1.1" 200 122 "" "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36"
        # http://127.0.0.1:8080

        # Same with redirect_uri hostname and port.
        urlparams = urlparse(self.redirect_uri)

        cherrypy.config.update({'server.socket_host': urlparams.hostname,
                                'server.socket_port': urlparams.port,
                                'checker.on': False,
                                'log.screen': False,
                                'log.access_file': '',
                                'log.error_file': ''})
        
        cherrypy.quickstart(self)

    @cherrypy.expose
    def index(self, state, code=None, error=None):
        """
        Receive a Fitbit response containing a verification code. Use the code
        to fetch the access_token.
        """
        error = None
        if code:
            try:
                self.fitbit.client.fetch_access_token(code)
            except MissingTokenError:
                error = self._fmt_failure(
                    'Missing access token parameter.</br>Please check that '
                    'you are using the correct client_secret')
            except MismatchingStateError:
                error = self._fmt_failure('CSRF Warning! Mismatching state')
        else:
            error = self._fmt_failure('Unknown error while authenticating')
        # Use a thread to shutdown cherrypy so we can return HTML first
        self._shutdown_cherrypy()
        return error if error else self.success_html

    def _fmt_failure(self, message):
        tb = traceback.format_tb(sys.exc_info()[2])
        tb_html = '<pre>%s</pre>' % ('\n'.join(tb)) if tb else ''
        return self.failure_html % (message, tb_html)

    def _shutdown_cherrypy(self):
        """ Shutdown cherrypy in one second, if it's running """
        if cherrypy.engine.state == cherrypy.engine.states.STARTED:
            threading.Timer(1, cherrypy.engine.exit).start()


if __name__ == '__main__':

    if not (len(sys.argv) == 3):
        print("Arguments: client_id and client_secret")
        sys.exit(1)

    server = OAuth2Server(*sys.argv[1:])
    server.browser_authorize()

    profile = server.fitbit.user_profile_get()
    print('You are authorized to access data for the user: {}'.format(
        profile['user']['fullName']))

    print('TOKEN\n=====\n')
    for key, value in server.fitbit.client.session.token.items():
        print('{} = {}'.format(key, value))
