import unittest

from objects import Inventory
from objects import Item


class TestInventory(unittest.TestCase):
    """Test Item"""

    def test_create_inventory_by_default(self):
        """Test: create empty Inventory."""
        inventory = Inventory()

        self.assertIsInstance(inventory.items, list)
        self.assertEqual(len(inventory.items), 0)

    def test_add_correct_item_to_items(self):
        """Test: add_item add correct item to items."""
        inventory = Inventory()
        item = Item('name', 100)

        self.assertEqual(len(inventory.items), 0)

        inventory.add_item(item=item)

        self.assertEqual(len(inventory.items), 1)
        self.assertIs(inventory.items[0], item)

    def test_not_add_incorrect_item_to_items(self):
        """Test: add_item not add incorrect item to items."""
        inventory = Inventory()

        self.assertEqual(len(inventory.items), 0)

        self.assertRaisesRegex(TypeError, r'Expected Item, but got (.+).', inventory.add_item, None)

        self.assertEqual(len(inventory.items), 0)

    def test_add_correct_items_to_items(self):
        """Test: add_items add correct items to items."""
        inventory = Inventory()
        items = [Item(f'name-{i}', cost=i*10) for i in range(1, 11)]

        self.assertEqual(len(inventory.items), 0)

        inventory.add_items(items)

        self.assertEqual(len(inventory.items), 10)
        for inv_item, item in zip(inventory.items, items):
            self.assertIs(inv_item, item)

    def test_not_add_incorrect_items_to_items(self):
        """Test: add_items not add incorrect items to items."""
        inventory = Inventory()

        self.assertEqual(len(inventory.items), 0)

        self.assertRaisesRegex(TypeError, r'Expected list, but got (.+).', inventory.add_items, None)
        self.assertRaisesRegex(ValueError, r'Items cannot be empty list.', inventory.add_items, [])
        self.assertRaisesRegex(TypeError, r'Each item in items list must be Item.', inventory.add_items, [None])

        self.assertEqual(len(inventory.items), 0)

    def test_clear(self):
        """Test: clear items."""
        inventory = Inventory()
        items = [Item(f'name-{i}', cost=i * 10) for i in range(1, 11)]
        inventory.add_items(items)

        self.assertEqual(len(inventory.items), 10)

        inventory.clear()

        self.assertEqual(len(inventory.items), 0)

    def test_get_info(self):
        """Test: get_info return correct info."""
        inventory = Inventory()
        items = [Item(f'name-{i}', cost=i * 10) for i in range(1, 11)]
        inventory.add_items(items)
        correct_info = tuple([item.get_info() for item in items])

        self.assertIsInstance(inventory.get_info(), tuple)
        self.assertEqual(inventory.get_info(), correct_info)


if __name__ == '__main__':
    unittest.main()
