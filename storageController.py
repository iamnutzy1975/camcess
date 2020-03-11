from google.cloud import storage
from utils.gcs import GCSObjectStreamUpload
import pickle
import io

class baseStorageController(object):

    def __init__(self):
        raise NotImplementedError()

    def write_pickled_object(self, object, object_key_name):
        raise NotImplementedError()

    def read_pickled_object(self, object_key_name):
        raise NotImplementedError()

    def upload_object(self, object_key_name):
        raise NotImplementedError()

    def download_object(self, object_key_name):
        raise NotImplementedError()

class storageController(baseStorageController):

    def __init__(self, bucket_name, credentials_file):
        self.storage_client = storage.Client.from_service_account_json(credentials_file)
        self.bucket = self.storage_client.get_bucket(bucket_name)
        self.bucket_name = bucket_name
        # Explicitly use service account credentials by specifying the private key file.


    def write_pickled_object(self, object, object_key_name):
        inmemoryfile = io.BytesIO(pickle.dumps(object))
        blob = self.bucket.blob('{}'.format(object_key_name))
        blob.upload_from_file(file_obj=inmemoryfile)

    def read_pickled_object(self, object_key_name):
        blob = self.bucket.blob('{}'.format(object_key_name))
        return(pickle.loads( blob.download_as_string()))

    def upload_object(self, object_data, object_key_name):
        with GCSObjectStreamUpload(client=self.storage_client
                , bucket_name=self.bucket_name, blob_name=object_key_name) as gcss:
            gcss.write(object_data)

    def download_object(self, object_key_name):
        raise NotImplementedError