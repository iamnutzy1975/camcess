from di import container
from services import IConfigService
from services import ILoggerService
from services import ICloudStorageService
from services import IDestinationService
from services import IProcessingService
import os

config = container.instance(IConfigService)
assert isinstance(config, IConfigService)

logger = container.instance(ILoggerService)
assert isinstance(logger, ILoggerService)

cloud_storage = container.instance(ICloudStorageService)
assert isinstance(cloud_storage,ICloudStorageService)

destination = container.instance(IDestinationService)
assert isinstance(destination, IDestinationService)

processing = container.instance(IProcessingService)
assert isinstance(processing,IProcessingService)


def process_image(data, context):
    logger.log("process_image", "ENV: {}".format(config.get_env()))

    # Get the file that has been uploaded to GCS

    cloud_storage.setup(bucket_name=data['bucket'],credentials_file=config.get_service_account_path())
    download_path = cloud_storage.get_object(object_name=data['name'])

    compressed_image_path = processing.compress(image_path=download_path)

    destination.push_file(source_file=compressed_image_path
                          , destination_file='/trailcameras/perfect/{}'.format(os.path.basename(compressed_image_path)))

    logger.log("process_image", "done")

    return

