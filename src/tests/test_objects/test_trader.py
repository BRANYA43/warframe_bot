import unittest
from datetime import datetime, timedelta

from objects import Inventory, Item, Trader
from objects.mixins import NameMixin, TimerMixin


class TestTrader(unittest.TestCase):
    """Test Trader"""

    def setUp(self) -> None:
        inventory = Inventory([Item(f'{i}', i * 10) for i in range(1, 11)])
        self.data = {
            'name': 'name',
            'inventory': inventory,
            'expiry': datetime.utcnow() + timedelta(days=1)
        }

    def test_trader_inherit_needed_mixins(self):
        """Test: Trader inherit NameMixin and TimerMixin."""
        self.assertTrue(issubclass(Trader, NameMixin))
        self.assertTrue(issubclass(Trader, TimerMixin))

    def test_create_trader_with_correct_values(self):
        """Test: create Trader with correct Inventory."""
        trader = Trader(**self.data)

        self.assertEqual(trader.name, self.data['name'])
        self.assertIs(trader.inventory, self.data['inventory'])
        self.assertFalse(trader.active)

    def test_not_create_trader_with_incorrect_inventory(self):
        """Test: not create Trader with incorrect Inventory."""
        del self.data['inventory']
        self.assertRaisesRegex(TypeError, r'Expected Inventory, but got (.+).', Trader, inventory=None, **self.data)

    def test_not_create_trader_with_incorrect_active(self):
        """Test: not create Trader with incorrect active."""
        self.assertRaisesRegex(TypeError, r'Expected bool, but got (.+).', Trader, active=None, **self.data)

    def test_set_active_correct_value(self):
        """Test: set active correct value."""
        trader = Trader(**self.data)

        self.assertFalse(trader.active)

        trader.active = True

        self.assertTrue(trader.active)

    def test_not_set_active_incorrect_value(self):
        """Test: not set active incorrect value."""
        trader = Trader(**self.data)

        with self.assertRaisesRegex(TypeError, r'Expected bool, but got (.+).'):
            trader.active = None


if __name__ == '__main__':
    unittest.main()
