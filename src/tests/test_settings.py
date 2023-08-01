import os
import unittest

from src import settings


class TestConfig(unittest.TestCase):
    def test_set_BASE_DIR(self):
        """Test: set BASE_DIR for all projects, dir must equal src"""
        self.assertTrue(os.path.exists(settings.BASE_DIR))
        self.assertEqual(os.path.basename(settings.BASE_DIR), 'src')
        self.assertEqual(os.path.basename(os.getcwd()), 'src')


if __name__ == '__main__':
    unittest.main()
