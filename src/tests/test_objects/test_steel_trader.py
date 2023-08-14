import unittest
from datetime import datetime, timedelta

import data
from objects import SteelTrader, Trader, Item


class TestSteelTrader(unittest.TestCase):
    """Test SteelTrader"""

    def setUp(self) -> None:
        self.offers = [Item(f'name-{i}', i * 10) for i in range(1, 11)]
        self.time_delta = timedelta(days=1)
        self.data = {
            'expiry': datetime.utcnow() + self.time_delta,
            'offers': self.offers,
            'current_offer': self.offers[0].name,

        }

    def test_steel_trader_inherit_trader(self):
        """Test: SteelTrader inherit Trader."""
        self.assertTrue(issubclass(SteelTrader, Trader))

    def test_create_steel_trader_with_correct_values(self):
        """Test: create SteelTrader with correct values."""
        trader = SteelTrader(**self.data)

        self.assertEqual(trader.name, data.TRADER_NAMES[1])
        self.assertEqual(trader._current_offer, 0)
        self.assertEqual(trader._next_offer, 1)
        self.assertEqual(trader.current_offer, self.offers[0])
        self.assertEqual(trader.next_offer, self.offers[1])
        self.assertEqual(trader.offers, self.offers)

    def test_not_create_steel_trader_with_incorrect_current_offer(self):
        """Test: not create SteelTrader with incorrect current_offer."""
        del self.data['current_offer']
        self.assertRaisesRegex(TypeError, r'Expected str, but got (.+).', SteelTrader, current_offer=None, **self.data)
        self.assertRaisesRegex(ValueError, 'Value cannot be empty string.', SteelTrader, current_offer='', **self.data)
        self.assertRaisesRegex(ValueError, r'No such a offer in offers.', SteelTrader,
                               current_offer='incorrect',
                               **self.data)

    def test_not_create_steel_trader_with_incorrect_offers(self):
        """Test: not create SteelTrader with incorrect offers."""
        del self.data['offers']
        self.assertRaisesRegex(TypeError, r'Expected list, but got (.+).', SteelTrader, offers=None, **self.data)
        self.assertRaisesRegex(ValueError, r'Items cannot be empty list.', SteelTrader, offers=[], **self.data)
        self.assertRaisesRegex(TypeError, r'Each item in items list must be Item.', SteelTrader, offers=[None], **self.data)

    def test_not_change_current_and_next_offers_after_update(self):
        """Test: not change current and next offers if timer is not equal 0 after update."""
        trader = SteelTrader(**self.data)

        self.assertEqual(trader.current_offer.name, trader.offers[0].name)
        self.assertEqual(trader.next_offer.name, trader.offers[1].name)

        trader.update()

        self.assertEqual(trader.current_offer.name, trader.offers[0].name)
        self.assertEqual(trader.next_offer.name, trader.offers[1].name)

    def test_change_current_and_next_offers_after_update(self):
        """Test: change current and next offers if timer is equal 0 and set new expiry after update."""
        self.data['expiry'] = datetime.utcnow() + timedelta(milliseconds=500)
        trader = SteelTrader(**self.data)
        old_expiry = trader.timer.expiry

        self.assertEqual(trader.current_offer.name, trader.offers[0].name)
        self.assertEqual(trader.next_offer.name, trader.offers[1].name)

        trader.update()

        self.assertNotEqual(trader.timer.expiry, old_expiry)
        self.assertLess(old_expiry, trader.timer.expiry)
        self.assertEqual(trader.timer.expiry, old_expiry + trader.TIME_TO_CHANGING_OFFER)
        self.assertIs(trader.current_offer, trader.offers[1])
        self.assertIs(trader.next_offer, trader.offers[2])

    def test_get_info(self):
        """Test: get_info returns correct info."""
        trader = SteelTrader(**self.data)
        correct_info = (
            f'Name: {data.TRADER_NAMES[1]}',
            f'Current offer: {trader.current_offer}',
            f'Next offer: {trader.next_offer}',
            f'Left time: {trader.timer.get_str_time()}',
        )

        self.assertEqual(correct_info, trader.get_info())


if __name__ == '__main__':
    unittest.main()
