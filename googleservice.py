from googleapiclient.discovery import build
from services.googleauth import BaseGoogleAuth

class GoogleService(object):
    """
    Representing base class for Google services.
    """

    def __init__(self, api_name, api_version, google_auth, scope=[]):
        """Constructor takes:
           api_name: string The name of the api to connect to.
	       api_version: string The api version to connect to.
           scope: A list of strings representing the auth scopes to authorize for the connection.
	       googleAuth: google auth object.
        """
        assert isinstance(google_auth, BaseGoogleAuth)

        self.api_name = api_name
        self.api_version = api_version
        self.google_auth = google_auth
        self.google_auth.add_scope(scope)

        self.service = None

    def get_service(self):
        """Get a service that communicates to a Google API."""

        http = self.google_auth.get_http_object()

        # Build the service object.
        self.service = build(self.api_name, self.api_version, http=http)

        return self.service

    def get_service_with_credentials(self):
        self.service = build(self.api_name, self.api_version, credentials=self.google_auth.credentials)

        return self.service

    def refresh_auth(self):
        self.google_auth.authorize()