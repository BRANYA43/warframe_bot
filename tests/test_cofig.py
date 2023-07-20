import os
import unittest

from warframe_bot import config


class TestConfig(unittest.TestCase):
    def test_set_BASE_DIR(self):
        """Test: set BASE_DIR for all projects, dir must equal warframe_bot"""
        self.assertTrue(os.path.exists(config.BASE_DIR))
        self.assertEqual(os.path.basename(config.BASE_DIR), 'warframe_bot')
        self.assertEqual(os.path.basename(os.getcwd()), 'warframe_bot')

    def test_correct_constants(self):
        """Test: constants is correct. they aren't empty string and None. They are correct type"""
        self.assertIsNotNone(config.BOT_TOKEN)
        self.assertNotEqual(config.BOT_TOKEN, '')
        self.assertIsInstance(config.BOT_TOKEN, str)


if __name__ == '__main__':
    unittest.main()