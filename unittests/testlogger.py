from unittests.unittestcore import BaseUnitTest
from services import ILoggerService

class TestLogger(BaseUnitTest):

    def test_log(self):
        self.assertIsInstance(self.logger, ILoggerService)
        self.logger.log("component name","message to log")
        self.assertTrue(True)