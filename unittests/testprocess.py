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

        cloud_storage.setup(bucket_name='camcess-bucket'
                , credentials_file='C:\\code\\sanbox\\camcess\\credentials\\abstract-gizmo-269816-d1cb94a4eea9.json')
        download_path = cloud_storage.get_object(object_name='IMG_0011.JPG')

        compressed_image_path = processing.compress(image_path=download_path)

        destination.push_file(source_file=compressed_image_path
                              , destination_file='/trailcameras/perfect/{}'.format(os.path.basename(compressed_image_path)))
        self.assertTrue(True)