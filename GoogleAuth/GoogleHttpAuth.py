from GoogleAuth.BaseGoogleAuth import BaseGoogleAuth

class GoogleHttpAuth(BaseGoogleAuth):
    """Accepts already authenticated http object. Suitable for use in GAE."""

    def __init__(self, http, scope=[]):
        super(GoogleHttpAuth, self).__init__(scope)

        self.http = http

    def authorize(self):
        pass

