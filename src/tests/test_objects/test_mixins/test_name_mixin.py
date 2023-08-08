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


if __name__ == '__main__':
    unittest.main()
