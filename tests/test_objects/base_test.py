import unittest


class BaseTest(unittest.TestCase):
    """Base Test"""

    def check_error_message(self, exception, message):
        self.assertEqual(str(exception.exception), message)