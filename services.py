from credentials.dropbox_credentials import DROPBOX_TOKEN
import dropbox
import os
import logging
from google.cloud import storage
from PIL import Image

ENV_DEVELOPMENT = "development"
ENV_PRODUCTION = "production"
ENV_STAGING = 'staging'

#Configuration Services
class IConfigService(object):

    def get_env(self):
        raise NotImplementedError()

    def is_production_env(self):
        raise NotImplementedError()

    def get_project_id(self):
        raise NotImplementedError()

    def get_service_account_path(self):
        raise NotImplementedError()

    def get_env_var(self, key):
        raise NotImplementedError()
class DefaultConfigService(IConfigService):

    def __init__(self):
        pass

    def get_env(self):
        return os.environ["ENV"]

    def is_production_env(self):
        return self.get_env() == ENV_PRODUCTION

    def get_project_id(self):
        return os.environ["GCP_PROJECT_ID"]

    def get_service_account_path(self):
        return os.path.join(os.path.dirname(__file__), 'credentials'
                     , os.environ["SERVICE_ACCOUNT_NAME"])

    def get_env_var(self, key):
        return os.environ.get(key, None)

#Logging Services
class ILoggerService(object):

    def log(self, component, msg, params=None, level=logging.INFO):
        raise NotImplementedError()
class DefaultLoggerService(ILoggerService):

    def log(self, component, msg, params=None, level=logging.INFO):
        logging.log(level,
                    "{c}|{msg}|{params}".format(
                        c=component, msg=msg,
                        params=params if params else ""
                    )
                )

#Email Services
class IEmailService(object):
    def connect(self):
        raise NotImplementedError()

    def check_for_messages(self,message_filter):
        raise NotImplementedError()

    def save_attachment(self):
        raise NotImplementedError()
class GmailEmailService(IEmailService):

    def __init__(self):
        pass

    def connect(self):
        raise NotImplementedError()

    def check_for_messages(self, message_filter):
        raise NotImplementedError()

    def save_attachment_to_cloud_storage_bucket(self):
        raise NotImplementedError()

# Destination Services
class IDestinationService(object):
    def __init__(self):
        raise NotImplementedError()

    def push_file(self,source_file, destination_file):
        raise NotImplementedError()
class DropboxService(IDestinationService):

    def __init__(self):
        self.dbx = dropbox.Dropbox(DROPBOX_TOKEN)

    def push_file(self, source_file, destination_file):
        with open(source_file, 'rb') as f:
            self.dbx.files_upload(f.read(), destination_file)

# Cloud Storage Services
class ICloudStorageService(object):
    def __init__(self):
        raise NotImplementedError

    def setup(self):
        raise NotImplementedError

    def get_object(self):
        raise NotImplementedError
class GCSService(ICloudStorageService):
    def __init__(self):
        pass

    def setup(self,bucket_name, credentials_file):
        self.storage_client = storage.Client.from_service_account_json(credentials_file)
        self.bucket = self.storage_client.get_bucket(bucket_name)

    def get_object(self, object_name):
        blob = self.bucket.blob(object_name)
        try:
            path = os.path.join(os.sep, 'c:',os.sep,'tmp', os.path.basename(object_name))
        except:
            path = os.path.join(os.sep, 'tmp', os.sep, os.path.basename(object_name))

        with open(path, 'wb') as file_obj:
            blob.download_to_file(file_obj)

        return path

# Processing Service
class IProcessingService(object):
    def __init__(self):
        raise NotImplementedError
class ProcessingService(IProcessingService):
    def __init__(self):
        pass

    def compress(self, image_path):
        picture = Image.open(image_path)

        # set quality= to the preferred quality.
        # I found that 85 has no difference in my 6-10mb files and that 65 is the lowest reasonable number
        compressed_filename = '{a}_compressed{b}'.format(a=image_path[:-4],b=image_path[-4:])
        picture.save(compressed_filename, "JPEG", optimize=True, quality=212
        return compressed_filename
