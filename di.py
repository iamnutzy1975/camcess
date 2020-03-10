import inject
container = inject
from services import IConfigService, DefaultConfigService as ConfigService
from services import ILoggerService, DefaultLoggerService as LoggerService
from services import IEmailService, GmailEmailService as EmailService

def config(binder):
    # config service
    config_service = ConfigService()
    binder.bind(IConfigService, config_service)
    assert isinstance(config_service, IConfigService)

    # logger service
    logger_service = LoggerService()
    binder.bind(ILoggerService, logger_service)

    # Email service
    email_service = EmailService()
    binder.bind(IEmailService, email_service)


# Configure a shared injector.
container.configure(config)