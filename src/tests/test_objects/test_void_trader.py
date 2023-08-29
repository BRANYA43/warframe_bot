import unittest
from datetime import datetime, timedelta

import data
from objects import VoidTrader, Trader, Item


class TestVoidTrader(unittest.TestCase):
    """Test VoidTrader"""

    def setUp(self) -> None:
        self.data = {
            'expiry': datetime.utcnow() + timedelta(days=1),
            'relay': data.RELAYS[0],
        }

    def test_void_trader_inherit_trader(self):
        """Test: VoidTrader inherit Trader."""
        self.assertTrue(issubclass(VoidTrader, Trader))

    def test_create_void_trader_with_correct_values(self):
        """Test: create VoidTrader with correct values."""
        trader = VoidTrader(**self.data)

        self.assertEqual(trader.name, data.TRADERS[0])
        self.assertEqual(trader.relay, data.RELAYS[0])
        self.assertFalse(trader.active)

    def test_not_create_void_trader_with_incorrect_relay(self):
        """Test: not create VoidTrader with incorrect relay."""
        del self.data['relay']
        self.assertRaisesRegex(TypeError, r'Expected str, but got (.+).', VoidTrader, relay=None, **self.data)
        self.assertRaisesRegex(ValueError, 'Value cannot be empty string.', VoidTrader, relay='', **self.data)
        self.assertRaisesRegex(ValueError, 'No such a relay name in data.', VoidTrader, relay='incorrect', **self.data)

    def test_not_create_void_trader_with_incorrect_active(self):
        """Test: not create VoidTrader with incorrect active."""
        self.assertRaisesRegex(TypeError, r'Expected bool, but got (.+).', VoidTrader, active=None, **self.data)

    def test_set_correct_value_for_active(self):
        """Test: set correct value for active."""
        trader = VoidTrader(**self.data)

        self.assertFalse(trader.active)

        trader.active = True

        self.assertTrue(trader.active)

    def test_not_set_incorrect_value_for_active(self):
        """Test: not set incorrect value for active."""
        trader = VoidTrader(**self.data)

        with self.assertRaisesRegex(TypeError, r'Expected bool, but got (.+).'):
            trader.active = None

    def test_set_correct_value_for_relay(self):
        """Test: set correct value for relay."""
        trader = VoidTrader(**self.data)

        self.assertEqual(trader.relay, data.RELAYS[0])

        trader.relay = data.RELAYS[1]

        self.assertEqual(trader.relay, data.RELAYS[1])

    def test_not_set_incorrect_value_for_relay(self):
        """Test: not set incorrect value for relay."""
        trader = VoidTrader(**self.data)

        with self.assertRaisesRegex(TypeError, r'Expected str, but got (.+).'):
            trader.relay = None

        with self.assertRaisesRegex(ValueError, 'Value cannot be empty string.'):
            trader.relay = ''

        with self.assertRaisesRegex(ValueError, 'No such a relay name in data.'):
            trader.relay = 'incorrect'

    def test_get_info_if_active_is_true(self):
        """Test: get_info returns correct info if active is True"""
        trader = VoidTrader(**self.data, active=True)
        correct_info = (
            f'Name: {data.TRADERS[0]}',
            f'Relay: {data.RELAYS[0]}',
            f'Left time: {trader.timer.get_str_time()}',
        )

        self.assertEqual(correct_info, trader.get_info())

    def test_get_info_if_active_is_false(self):
        """Test get_info returns correct info if active is False."""
        trader = VoidTrader(**self.data)
        correct_info = (
            f'Name: {data.TRADERS[0]}',
            'Location: Void',
            f'Left time: {trader.timer.get_str_time()}',
        )

        self.assertEqual(correct_info, trader.get_info())

    def test_not_change_active_and_timer_after_update(self):
        """Test: not change active and timer if timer is not equal 0 after update."""
        trader = VoidTrader(**self.data)

        self.assertFalse(trader.active)
        self.assertEqual(trader.timer.expiry, self.data['expiry'])

        trader.update()

        self.assertFalse(trader.active)
        self.assertEqual(trader.timer.expiry, self.data['expiry'])

    def test_change_active_and_timer_after_update(self):
        """Test: change active and timer if timer is equal 0 after update."""
        self.data['expiry'] = datetime.utcnow() + timedelta(milliseconds=500)
        trader = VoidTrader(**self.data)
        old_expiry = trader.timer.expiry

        self.assertFalse(trader.active)

        trader.update()

        self.assertNotEqual(trader.timer.expiry, old_expiry)
        self.assertLess(old_expiry, trader.timer.expiry)
        self.assertTrue(trader.active)

    def test_clear_inventory_if_active_is_switched_from_true_to_false(self):
        """Test: clear inventory if active is switched from true to false."""
        self.data['expiry'] = datetime.utcnow() + timedelta(milliseconds=500)
        trader = VoidTrader(**self.data, active=True)
        trader.inventory.add_item(Item('name', 100))

        self.assertTrue(trader.active)
        self.assertEqual(len(trader.inventory.items), 1)

        trader.update()

        self.assertFalse(trader.active)
        self.assertEqual(len(trader.inventory.items), 0)


if __name__ == '__main__':
    unittest.main()
