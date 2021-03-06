from dropbox_credentials import DROPBOX_TOKEN
import dropbox
import os
import logging
from google.cloud import storage
from PIL import Image
from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True

import piexif
import piexif.helper

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

    def process(self, image_path):
        zeroth_ifd = {
            piexif.ImageIFD.ImageDescription: image_path.split('.')[0].split('_')[1]
        }
        exif_dict = {"0th":zeroth_ifd}
        exif_bytes = piexif.dump(exif_dict)
        img = Image.open(image_path)

        #Date Taken
        # Either it exists in the picture Exif data (not the case for Reconeco pictures) or we must extract it from
        # the image using the VISION API.  Best to write it to the Date Taken field and not include two timestamps
        # in the filename because it's hard to sort by.
        date_taken = 'todo - date taken'

        #Exif has "tags" fields.  Good spot to write vision API too
        #Exif has "rating"

        # set quality= to the preferred quality.
        # I found that 85 has no difference in my 6-10mb files and that 65 is the lowest reasonable number
        compressed_filename = '{a}_p{b}'.format(a=image_path[:-4],b=image_path[-4:])
        img.save(compressed_filename, "JPEG", optimize=True, exif=exif_bytes, quality=85)
        return compressed_filename
