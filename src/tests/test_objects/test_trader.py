import unittest
from datetime import datetime, timedelta

from objects import Inventory, Item, Trader
from objects.mixins import NameMixin, TimerMixin


class TestTrader(unittest.TestCase):
    """Test Trader"""

    def setUp(self) -> None:
        self.items = [Item(name=f'name-{i}', cost=i*10) for i in range(1, 11)]
        self.data = {
            'name': 'name',
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
        self.assertIsInstance(trader.inventory, Inventory)

    def test_get_info(self):
        """Test: get_info return correct info."""
        trader = Trader(**self.data)
        correct_info = (
            f'Name: {trader.name}',
            f'Left Time: {trader.timer.get_str_time()}',
        )

        self.assertIsInstance(trader.get_info(), tuple)
        self.assertEqual(trader.get_info(), correct_info)


if __name__ == '__main__':
    unittest.main()
