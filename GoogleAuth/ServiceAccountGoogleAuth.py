import httplib2
from oauth2client.service_account import ServiceAccountCredentials
from GoogleAuth.BaseGoogleAuth import BaseGoogleAuth

class ServiceAccountGoogleAuth(BaseGoogleAuth):
    """Representing service account authntication flow
        https://developers.google.com/analytics/devguides/reporting/core/v3/quickstart/service-py
    """

    def __init__(self, account_key_path, scope=[]):
        super(ServiceAccountGoogleAuth, self).__init__(scope)

        self.account_key_path = account_key_path

    def authorize(self):
        credentials = ServiceAccountCredentials.from_json_keyfile_name(self.account_key_path, self.scope)

        self.http = credentials.authorize(http=httplib2.Http())