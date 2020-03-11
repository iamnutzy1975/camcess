import inject
container = inject
from services import IConfigService, DefaultConfigService as ConfigService
from services import ILoggerService, DefaultLoggerService as LoggerService
from services import IEmailService, GmailEmailService as EmailService
from services import IDestinationService, DropboxService as DestinationService
from services import ICloudStorageService, GCSService as CloudStorageService
from services import IProcessingService, ProcessingService as ProcessingService

def config(binder):
    # config service
    config_service = ConfigService()
    binder.bind(IConfigService, config_service)
    assert isinstance(config_service, IConfigService)

    # logger service
    logger_service = LoggerService()
    binder.bind(ILoggerService, logger_service)
    assert isinstance(logger_service, ILoggerService)

    # Email service
    email_service = EmailService()
    binder.bind(IEmailService, email_service)
    assert isinstance(email_service, IEmailService)

    # destination service
    destination_service = DestinationService()
    binder.bind(IDestinationService, destination_service)
    assert isinstance(destination_service, IDestinationService)

    # Cloud Storage Service
    cloud_storage_service = CloudStorageService()
    binder.bind(ICloudStorageService, cloud_storage_service)
    assert isinstance(cloud_storage_service, ICloudStorageService)

    # Processing Service
    processing_service = ProcessingService()
    binder.bind(IProcessingService, processing_service)
    assert isinstance(processing_service, IProcessingService)

# Configure a shared injector.
container.configure(config)