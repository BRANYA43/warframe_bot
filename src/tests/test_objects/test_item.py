import unittest

from objects.mixins import NameMixin
from objects import Item


class TestItem(unittest.TestCase):
    """Test Item"""

    def setUp(self) -> None:
        self.data = {
            'name': 'name',
            'cost': 100,
        }

    def test_item_inherit_name_mixin(self):
        """Test: Item inherit NameMixin."""
        self.assertTrue(issubclass(Item, NameMixin))

    def test_create_item_with_correct_cost(self):
        """Test: create Item with correct cost."""
        item = Item(**self.data)

        self.assertEqual(item.name, self.data['name'])
        self.assertEqual(item.cost, self.data['cost'])

    def test_not_create_item_with_incorrect_cost(self):
        """Test: not create Item with incorrect cost."""
        del self.data['cost']

        self.assertRaisesRegex(TypeError, r'Expected int, but got (.+).', Item, cost=None, **self.data)
        self.assertRaisesRegex(ValueError, r'Cost cannot be less 0.', Item, cost=-1, **self.data)


if __name__ == '__main__':
    unittest.main()
