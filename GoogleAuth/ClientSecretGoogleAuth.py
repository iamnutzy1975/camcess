import httplib2
from oauth2client import file
from oauth2client import tools

from GoogleAuth.BaseGoogleAuth import BaseGoogleAuth


class ClientSecretGoogleAuth(BaseGoogleAuth):
    """Representing client secrent authntication flow"""

    def __init__(self, client_secret_path, auth_file_path, scope=[]):
        super(ClientSecretGoogleAuth, self).__init__(scope)

        self.client_secret_path = client_secret_path
        self.auth_file_path = auth_file_path

    def authorize(self):
        # Parser command-line arguments.
        # parser = argparse.ArgumentParser(
        # formatter_class=argparse.RawDescriptionHelpFormatter,
        # parents=[tools.argparser])
        # flags = parser.parse_args([])
        #
        # # Set up a Flow object to be used if we need to authenticate.
        # flow = client.flow_from_clientsecrets(self.client_secret_path,
        #                                       scope=self.scope,
        #                                       message=tools.message_if_missing(self.client_secret_path))

        # Prepare credentials, and authorize HTTP object with them.
        # If the credentials don't exist or are invalid run through the native client
        # flow. The Storage object will ensure that if successful the good
        # credentials will get written back to a file.
        storage = file.Storage(self.auth_file_path)
        credentials = storage.get()

        if credentials is None or credentials.invalid:
            credentials = tools.run_flow(flow, storage, flags)

        self.http = credentials.authorize(http=httplib2.Http())

