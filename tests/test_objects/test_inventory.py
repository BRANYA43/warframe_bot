import unittest

from warframe_bot.objects.item import Item

from warframe_bot.objects.inventory import Inventory


class TestInventory(unittest.TestCase):
    """Test Inventory"""

    def setUp(self) -> None:
        self.items = [Item(title=f'title-{i}', cost=10) for i in range(10)]
        self.inventory = Inventory()

    def test_create_inventory_with_correct_values(self):
        """Test: create inventory with correct values"""
        self.assertEqual(self.inventory.items, None)
        inventory = Inventory(items=self.items)
        self.assertEqual(inventory.items, self.items)
        self.assertEqual(len(inventory.items), 10)

    def test_not_create_inventory_with_correct_values(self):
        """Test: not create inventory with incorrect values"""
        with self.assertRaises((TypeError, ValueError)):
            Inventory(items=1)
            Inventory(items=[None])
            Inventory(items=[])

    def test_raise_errors_items_property(self):
        """
        Test: raise TypeError if items isn't list, raise ValueError if items is empty, raise TypeError if items of items
        aren't Item
        """
        with self.assertRaises(TypeError) as e:
            self.inventory.items = 1
        self.assertEqual(str(e.exception), 'Items must be list or None.')

        with self.assertRaises(ValueError) as e:
            self.inventory.items = []
        self.assertEqual(str(e.exception), 'Items cannot be empty.')

        with self.assertRaises(TypeError) as e:
            self.inventory.items = [None]
        self.assertEqual(str(e.exception), 'Items of items must be Item.')

    def test_clear(self):
        """Test: clear all items"""
        self.inventory = self.items
        self.assertEqual(len(self.items), 10)
        self.inventory.clear()
        self.assertEqual(len(self.items), 0)


if __name__ == '__main__':
    unittest.main()
