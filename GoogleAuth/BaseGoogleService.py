from googleapiclient.discovery import build

from GoogleAuth.BaseGoogleAuth import BaseGoogleAuth


class BaseGoogleService(object):
    """Representing base class for Google services.
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
        self.google_auth.addScope(scope)

        self.service = None

    def enableReadOnly(self):
        raise NotImplementedError()

    def enableEdit(self):
        raise NotImplementedError()

    def getService(self):
        """Get a service that communicates to a Google API."""

        http = self.google_auth.getHttpObject()

        # Build the service object.
        self.service = build(self.api_name, self.api_version, http=http)

        return self.service
