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

    def test_add_item_to_items(self):
        """Test: add_item add Item to items."""
        inventory = Inventory()
        item = Item('name', 100)

        self.assertEqual(len(inventory.items), 0)

        inventory.add_item(item=item)

        self.assertEqual(len(inventory.items), 1)
        self.assertIs(inventory.items[0], item)

    def test_create_item_from_values_and_add_item_to_items(self):
        """Test: add_item create Item from values and add it to items."""
        inventory = Inventory()

        self.assertEqual(len(inventory.items), 0)

        inventory.add_item_from_values('name', 100)

        self.assertEqual(len(inventory.items), 1)
        self.assertIsInstance(inventory.items[0], Item)
        self.assertEqual(inventory.items[0].name, 'name')
        self.assertEqual(inventory.items[0].cost, 100)

    def test_add_items_to_items(self):
        """Test: add_items add items to items."""
        inventory = Inventory()
        items = [Item(f'name-{i}', cost=i*10) for i in range(1, 11)]

        self.assertEqual(len(inventory.items), 0)

        inventory.add_items(items)

        self.assertEqual(len(inventory.items), 10)
        for inv_item, item in zip(inventory.items, items):
            self.assertIs(inv_item, item)

    def test_create_items_from_values_and_add_items_to_items(self):
        """Test: add_items create Item from item_values and add items to items."""
        inventory = Inventory()
        items = [(f'name-{i}', i * 10) for i in range(1, 11)]

        self.assertEqual(len(inventory.items), 0)

        inventory.add_items_from_values(items)

        self.assertEqual(len(inventory.items), 10)
        for inv_item, item in zip(inventory.items, items):
            self.assertIsInstance(inv_item, Item)
            self.assertEqual(inv_item.name, item[0])
            self.assertEqual(inv_item.cost, item[1])

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
