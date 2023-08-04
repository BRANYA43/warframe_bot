import unittest

from objects import Inventory
from objects import Item


class TestInventory(unittest.TestCase):
    """Test Item"""

    def setUp(self) -> None:
        self.items = [Item(f'{i}', i * 10) for i in range(1, 11)]

    def test_create_inventory_by_default(self):
        """Test: create empty Inventory."""
        inventory = Inventory()

        self.assertEqual(len(inventory.items), 0)

    def test_create_inventory_with_correct_items(self):
        """Test: create Item with correct cost."""
        inventory = Inventory(self.items)

        self.assertNotEqual(len(inventory.items), 0)
        self.assertIsNot(inventory.items, self.items)
        self.assertEqual(inventory.items, self.items)

    def test_not_create_inventory_with_incorrect_items(self):
        """Test: not create Item with incorrect cost."""
        self.assertRaisesRegex(TypeError, r'Expected list or tuple, but got (.+).', Inventory, 'None')
        self.assertRaisesRegex(TypeError, 'Each item of items must be Item type.', Inventory, [None])

    def test_set_items_correct_value(self):
        """Test: set items correct value."""
        inventory = Inventory(self.items)
        old_items = inventory.items
        new_items = [Item('name', 100)]
        inventory.items = new_items

        self.assertNotEqual(inventory.items, old_items)
        self.assertEqual(inventory.items, new_items)

    def test_not_set_items_incorrect_value(self):
        """Test: not set items incorrect value."""
        inventory = Inventory(self.items)

        with self.assertRaisesRegex(TypeError, r'Expected list or tuple, but got (.+).'):
            inventory.items = 'None'

        with self.assertRaisesRegex(TypeError, 'Each item of items must be Item type.'):
            inventory.items = [None]

    def test_get_info(self):
        """Test: get_info return correct info."""
        inventory = Inventory(self.items)
        correct_info = tuple([item.get_info() for item in self.items])

        self.assertIsInstance(inventory.get_info(), tuple)
        self.assertEqual(inventory.get_info(), correct_info)


if __name__ == '__main__':
    unittest.main()
