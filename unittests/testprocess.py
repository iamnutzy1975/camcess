from unittests.unittestcore import BaseUnitTest
from services import ICloudStorageService
from services import IDestinationService
from services import IProcessingService
from di import container
import os

cloud_storage = container.instance(ICloudStorageService)
assert isinstance(cloud_storage,ICloudStorageService)

destination = container.instance(IDestinationService)
assert isinstance(destination, IDestinationService)

processing = container.instance(IProcessingService)
assert isinstance(processing,IProcessingService)

class TestProcess(BaseUnitTest):

    def test_process(self):

        # Get the file that has been uploaded to GCS

        obj_name = 'camcess/barbwire/2020-03/20200318233403_KAS2-RCON0238.JPG'
        path_breakdown = obj_name.split("/")
        path = "/".join(path_breakdown[:-1])

        cloud_storage.setup(bucket_name='camcess-bucket'
                , credentials_file='C:\\code\\sanbox\\camcess\\credentials\\abstract-gizmo-269816-9c206f640ecc.json')
        download_path = cloud_storage.get_object(object_name=obj_name)

        compressed_image_path = processing.process(image_path=download_path)

        destination.push_file(source_file=compressed_image_path
                              , destination_file='/{}/{}'.format(path,os.path.basename(compressed_image_path)))
        self.assertTrue(True)