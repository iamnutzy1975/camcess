import unittest
import os, sys

sys.path.append(
    os.path.normpath(os.path.join(os.path.dirname(__file__), ".."))
)
from unittests.testconfig import TestConfig
from unittests.testlogger import TestLogger

if __name__ == '__main__':
    test_suite = unittest.TestSuite()

    # tests
    test_suite.addTest(unittest.makeSuite(TestConfig))
    test_suite.addTest(unittest.makeSuite(TestLogger))

    runner = unittest.TextTestRunner()
    runner.run(test_suite)
