import datetime
import unittest

from tests.test_objects.base_test import BaseTest
from warframe_bot.objects.inventory import Inventory
from warframe_bot.objects.item import Item
from warframe_bot.objects.trader import Trader


class TestTrader(BaseTest):
    """Test Trader"""
    def setUp(self) -> None:
        self.key = 'key'
        self.name = 'name'
        self.expiry = datetime.datetime.utcnow()
        items = [Item(f'name-{i}', cost=10) for i in range(10)]
        self.inventory = Inventory(items)
        self.trader = Trader(key=self.key, name=self.name, expiry=self.expiry)

    def test_create_trader_with_correct_values(self):
        """Test: create trader with correct values"""
        self.assertEqual(self.trader.key, self.key)
        self.assertEqual(self.trader.name, self.name)
        self.assertEqual(self.trader.expiry, self.expiry)
        self.assertIsInstance(self.trader.inventory, Inventory)

        trader = Trader(key=self.key, name=self.name, expiry=self.expiry, inventory=self.inventory)
        self.assertEqual(trader.inventory, self.inventory)

    def test_create_trader_with_incorrect_values(self):
        """Test: not create trader with incorrect values"""
        with self.assertRaises(TypeError):
            Trader(key=self.key, name=self.name, expiry=self.expiry, inventory=None)

    def test_raise_errors_inventory_property(self):
        """Test: raise TypeError if inventory isn't Inventory"""
        with self.assertRaises(TypeError) as e:
            self.trader.inventory = None
        self.check_error_message(e, 'inventory must be Inventory.')


if __name__ == '__main__':
    unittest.main()
