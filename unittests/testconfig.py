from unittests.unittestcore import BaseUnitTest
from services import IConfigService

class TestConfig(BaseUnitTest):

    def test_env(self):
        self.assertIsInstance(self.config, IConfigService)
        self.assertTrue(not self.config.is_production_env(), msg="Unit tests set to production env!")
        self.assertTrue(True)