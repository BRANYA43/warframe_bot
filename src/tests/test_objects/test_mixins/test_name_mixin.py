import unittest

from objects.mixins import NameMixin


class TestNameMixin(unittest.TestCase):
    """Test NameMixin"""

    def setUp(self) -> None:
        self.name = 'name'

    def test_create_name_mixin_with_correct_name(self):
        """Test: create NameMixin with correct name."""
        name_mixin = NameMixin(self.name)

        self.assertIsInstance(name_mixin.name, str)
        self.assertEqual(name_mixin.name, self.name)

    def test_not_create_name_mixin_with_incorrect_name(self):
        """Test: not create NameMixin with incorrect name."""
        self.assertRaisesRegex(TypeError, r'Expected str, but got (.+).', NameMixin, None)
        self.assertRaisesRegex(ValueError, r'Value cannot be empty string.', NameMixin, '')

    def test_set_new_name(self):
        """Test: set new name."""
        name_mixin = NameMixin(self.name)

        self.assertEqual(name_mixin.name, self.name)

        new_name = 'new_name'
        name_mixin.name = new_name

        self.assertEqual(name_mixin.name, new_name)

    def test_not_set_new_name_if_value_is_incorrect(self):
        """Test: not set new name if value is incorrect."""
        name_mixin = NameMixin(self.name)

        with self.assertRaisesRegex(TypeError, r'Expected str, but got (.+).'):
            name_mixin.name = None

        with self.assertRaisesRegex(ValueError, r'Value cannot be empty string.'):
            name_mixin.name = ''


if __name__ == '__main__':
    unittest.main()
