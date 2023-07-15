import datetime
import unittest

from warframe_bot.objects.inventory import Inventory
from warframe_bot.objects.item import Item
from warframe_bot.objects.trader import Trader


class TestTrader(unittest.TestCase):
    """Test Trader"""
    def setUp(self) -> None:
        self.expiry = datetime.datetime.utcnow()
        items = [Item(f'title-{i}', cost=10) for i in range(10)]
        self.inventory = Inventory(items)
        self.trader = Trader(name='Name', title='Title', expiry=self.expiry, inventory=self.inventory)

    def test_create_trader_with_correct_values(self):
        """Test: create trader with correct values"""
        self.assertEqual(self.trader.name, 'Name')
        self.assertEqual(self.trader.title, 'Title')
        self.assertEqual(self.trader.expiry, self.expiry)
        self.assertEqual(self.trader.inventory, self.inventory)

    def test_create_trader_with_incorrect_values(self):
        """Test: not create trader with incorrect values"""
        with self.assertRaises(TypeError):
            Trader(inventory=None)

    def test_raise_errors_inventory_property(self):
        """Test: raise TypeError if inventory isn't Inventory"""
        with self.assertRaises(TypeError) as e:
            self.trader.inventory = None
        self.assertEqual(str(e.exception), 'Inventory must be Inventory.')


if __name__ == '__main__':
    unittest.main()
