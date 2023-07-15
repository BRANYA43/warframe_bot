import datetime
import unittest

from warframe_bot.objects.base import Base


class TestBase(unittest.TestCase):
    """Test Base"""

    def setUp(self) -> None:
        self.expiry = datetime.datetime.utcnow()

    def test_create_base_with_correct_attrs(self):
        """Test: create base with correct attrs"""
        base = Base(name='name', title='title', expiry=self.expiry)
        self.assertEqual(base.name, 'name')
        self.assertEqual(base.title, 'title')
        self.assertEqual(base.expiry, self.expiry)

    def test_not_create_base_with_incorrect_attrs(self):
        """Test: not create base with incorrect attrs"""
        with self.assertRaises((TypeError, ValueError)):
            base = Base(name=None, title=None, expiry=None)
            base = Base(name='', title='', expiry=None)

    def test_raise_errors_of_name_property(self):
        """Test: raise ValueError if name is empty string, raise TypeError if name isn't str."""
        with self.assertRaises(TypeError) as e:
            base = Base(name=None, title='title', expiry=self.expiry)
        self.assertEqual(str(e.exception), 'Name must be str.')

        with self.assertRaises(ValueError) as e:
            base = Base(name='', title='title', expiry=self.expiry)
        self.assertEqual(str(e.exception), 'Name cannot be empty string.')

    def test_raise_errors_of_title_property(self):
        """Test: raise ValueError if title is empty string, raise TypeError if title isn't str."""
        with self.assertRaises(TypeError) as e:
            base = Base(name='name', title=None, expiry=self.expiry)
        self.assertEqual(str(e.exception), 'Title must be str.')

        with self.assertRaises(ValueError) as e:
            base = Base(name='name', title='', expiry=self.expiry)
        self.assertEqual(str(e.exception), 'Title cannot be empty string.')

    def test_raise_errors_of_expiry_property(self):
        """Test: raise TypeError if expiry isn't datetime."""
        with self.assertRaises(TypeError) as e:
            base = Base(name='name', title='title', expiry=None)
        self.assertEqual(str(e.exception), 'Expiry must be datetime.')


if __name__ == '__main__':
    unittest.main()
