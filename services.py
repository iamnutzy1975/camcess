import os
import logging

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
        return os.environ["SERVICE_ACCOUNT_NAME"]

    def get_export_bucket(self):
        return os.environ["EXPORT_BUCKET_NAME"]

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