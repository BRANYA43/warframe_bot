import unittest

from tests.test_objects.base_test import BaseTest
from warframe_bot.objects.item import Item


class TestItem(BaseTest):
    """Test Item"""

    def setUp(self) -> None:
        self.item = Item(title='title', cost=100)

    def test_create_item_with_correct_values(self):
        """Test: create item with correct value"""
        self.assertEqual(self.item.title, 'title')
        self.assertEqual(self.item.cost, 100)

    def test_not_create_item_with_incorrect_values(self):
        """Test: not create item with incorrect value"""
        with self.assertRaises((TypeError, ValueError)):
            Item(title=None, cost=None)
            Item(title='', cost=-1)

    def test_raise_errors_of_title_property(self):
        with self.assertRaises(TypeError) as e:
            self.item.title = None
        self.check_error_message(e, 'Title must be str.')

        with self.assertRaises(ValueError) as e:
            self.item.title = ''
        self.check_error_message(e, 'Title cannot be empty string.')

    def test_raise_errors_of_cost_property(self):
        with self.assertRaises(TypeError) as e:
            self.item.cost = None
        self.check_error_message(e, 'Cost must be int.')

        with self.assertRaises(ValueError) as e:
            self.item.cost = -1
        self.check_error_message(e, 'Cost cannot be negative.')


if __name__ == '__main__':
    unittest.main()
