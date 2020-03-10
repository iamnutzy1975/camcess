import httplib2
from oauth2client.service_account import ServiceAccountCredentials

class BaseGoogleAuth(object):
    """Represents base class for all the different ways Google authentication works"""

    def __init__(self, scope = [], timeout = 60):
        assert isinstance(scope, list)

        self.scope = scope
        self.timeout = timeout
        self.credentials = None
        self.http = None

    def add_scope(self, scope):
        """Adds scope or scopes to the scope list.
           Accept scope as string or multiple scopes in list
        """

        def add_scope_single(s):
            if not s in self.scope:
                self.scope.append(s)

        if isinstance(scope, str):
            add_scope_single(scope)

        elif isinstance(scope, list):
            for s in scope:
                add_scope_single(s)

    def authorize(self):
        raise NotImplementedError()

    def get_http_object(self):
        if self.http is None:
            raise Exception("authorize was not called on Google auth object - http obect is None")

        return self.http

#*************************#
#***ServiceAccountGoogleAuth***#

class ServiceAccountGoogleAuth(BaseGoogleAuth):
    """Representing service account authntication flow
        https://developers.google.com/analytics/devguides/reporting/core/v3/quickstart/service-py
    """

    def __init__(self, account_key_path, scope=[]):
        super(ServiceAccountGoogleAuth, self).__init__(scope)

        self.account_key_path = account_key_path

    def authorize(self):
        self.credentials = ServiceAccountCredentials.from_json_keyfile_name(self.account_key_path, self.scope)

        http = httplib2.Http(timeout=self.timeout)
        self.http = self.credentials.authorize(http=http)
