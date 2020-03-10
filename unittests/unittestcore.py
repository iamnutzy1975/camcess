import unittest
import os
import yaml
from services import IConfigService, ILoggerService, IEmailService
from di import container

class BaseUnitTest(unittest.TestCase):

    def setUp(self):
        self.container = container

        # find path to env.dev.yaml
        env_path = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "env.dev.yaml"))

        # load env variables from yaml
        env_vars = None
        with open(env_path, "r") as f:
            env_vars = yaml.load(f)

        for k, v in env_vars.items():
            os.environ[k] = v

        self.config = self.container.instance(IConfigService)
        assert isinstance(self.config, IConfigService)

        self.logger = self.container.instance(ILoggerService)
        assert isinstance(self.logger, ILoggerService)

        self.email = self.container.instance(IEmailService)
        assert isinstance(self.email, IEmailService)


