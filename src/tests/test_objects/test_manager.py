import asyncio
import unittest
from datetime import datetime, timedelta

import data
from objects import Manager, Place, Item, VoidTrader, SteelTrader


class TestManager(unittest.TestCase):
    """Test Manager"""

    def setUp(self) -> None:
        self.manager = Manager()

    def test_manager_have_response_dict(self):
        """Test: Manager have response."""
        self.assertFalse(self.manager._is_ready)

    def test_format_expiry(self):
        """Test: format_expiry returns datetime."""
        manager = Manager()
        expiry = datetime.utcnow() + timedelta(days=1)
        return_expiry = manager.format_expiry(expiry.isoformat() + 'Z')

        self.assertEqual(return_expiry, expiry)
        self.assertIsInstance(return_expiry, datetime)

    def test_get_response(self) -> dict:
        """Test: get_response returns response dict by url."""
        response = self.manager.get_response(data.MAIN_URL)
        self.assertIsInstance(response, dict)

    def test_after_prepare_is_ready_is_true(self):
        """Test: after prepare is_ready is True."""
        self.assertFalse(self.manager.is_ready)

        self.manager.prepare()

        self.assertTrue(self.manager.is_ready)

    def test_get_item_list(self):
        items_data = [{'name': f'name-{i}', 'cost': i * 10} for i in range(1, 10)]
        item_list = self.manager.get_item_list(items_data)

        self.assertIsInstance(item_list, list)
        for item in item_list:
            self.assertIsInstance(item, Item)

        for item, item_data in zip(item_list, items_data):
            self.assertEqual(item.name, item_data['name'])
            self.assertEqual(item.cost, item_data['cost'])


class TestManagerWorkWithPlaces(unittest.TestCase):
    """Test manager work with places"""

    def setUp(self) -> None:
        self.earth_expiry = datetime.utcnow() + timedelta(days=1)
        self.cetus_expiry = datetime.utcnow() + timedelta(minutes=2)
        self.fake_response = {
            'earthCycle': {
                'expiry': self.earth_expiry.isoformat() + 'Z',
                'state': 'day',
            },
            'cetusCycle': {
                'expiry': self.cetus_expiry.isoformat() + 'Z',
                'state': 'night',
            },
        }
        self.manager = Manager()

    def test_manager_have_places_dict(self):
        """Test: Manager have place dict."""
        self.assertEqual(len(self.manager._places), 0)

    def test_create_place(self):
        """Test: create_place add Place to places dict and return it."""
        key = 'earthCycle'

        self.assertEqual(len(self.manager._places), 0)

        place_response = self.fake_response[key]
        place = self.manager.create_place(place_response, 'Earth', key)

        self.assertIsInstance(place, Place)
        self.assertEqual(len(self.manager._places), 1)
        self.assertIs(place, self.manager._places[key])
        self.assertEqual(place.timer.expiry, self.earth_expiry)
        self.assertIs(place._cycles, data.CYCLES[key])
        self.assertEqual(place.current_cycle, place_response['state'])

    def test_prepare_places(self):
        """Test prepare_places create places from response API Warframe."""
        self.assertEqual(len(self.manager._places), 0)

        self.manager.prepare_places()

        self.assertEqual(len(self.manager._places), len(data.CYCLE_URLS))

    def test_update_places_reduces_timer_of_places(self):
        """Test update_places reduce timer of places"""
        self.manager.create_place(self.fake_response['earthCycle'], 'Earth', 'earthCycle')
        self.manager.create_place(self.fake_response['cetusCycle'], 'Cetus', 'cetusCycle')
        old_times = [place.timer.total_seconds for place in self.manager._places.values()]
        self.manager.update_places()

        for old_time, place in zip(old_times, self.manager._places.values()):
            self.assertLess(place.timer.total_seconds, old_time, msg=f'Place({place.name} timer is not less old time.')

    def test_update_places_update_timer_and_cycles_of_places(self):
        """Test: update_places update timer and cycles of places if timer is 0."""
        cetus_expiry = datetime.utcnow() + timedelta(minutes=1)
        self.fake_response['cetusCycle']['expiry'] = cetus_expiry.isoformat() + 'Z'
        self.manager.create_place(self.fake_response['earthCycle'], 'Earth', 'earthCycle')
        cetus = self.manager.create_place(self.fake_response['cetusCycle'], 'Cetus', 'cetusCycle')
        old_expiry = cetus.timer.expiry

        self.assertEqual(cetus.timer.expiry, cetus_expiry)
        self.assertEqual(cetus.current_cycle, 'night')
        self.assertEqual(cetus.next_cycle, 'day')

        self.manager.update_places()

        self.assertNotEqual(cetus.timer.expiry, old_expiry)
        self.assertEqual(cetus.timer.expiry, old_expiry + data.CYCLES['cetusCycle'][0].duration)
        self.assertEqual(cetus.current_cycle, 'day')
        self.assertEqual(cetus.next_cycle, 'night')


class TestManagerWorkForTraders(unittest.TestCase):
    """Test manager work for Trader"""

    def setUp(self) -> None:
        self.void_trader_expiry = datetime.utcnow() + timedelta(days=1)
        self.steel_path_trader_expiry = datetime.utcnow() + timedelta(days=1)
        self.fake_response = {
            'voidTrader': {
                'expiry': self.void_trader_expiry.isoformat(),
                'active': False,
                'location': data.RELAY_NAMES[0],
                'inventory': []
            },
        }
        self.manager = Manager()

    def test_manager_has_void_trader_and_steel_trader(self):
        """Test: Manager has void_trader and steel_trader."""
        self.assertIsNone(self.manager._steel_trader)

    def test_create_void_trader(self):
        """Test: create_void_trader set void_trader and returns VoidTrader."""
        response = self.fake_response['voidTrader']
        void_trader = self.manager.create_void_trader(response)

        self.assertIsNotNone(self.manager._void_trader)
        self.assertIsInstance(self.manager._void_trader, VoidTrader)
        self.assertIs(void_trader, self.manager._void_trader)
        self.assertEqual(void_trader.timer.expiry, self.void_trader_expiry)
        self.assertFalse(void_trader.active)
        self.assertEqual(void_trader.relay, response['location'])
        self.assertEqual(len(void_trader.inventory.items), 0)

    def test_create_void_trader_with_not_empty_inventory(self):
        """Test: create_void_trader set void_trader and returns VoidTrader with not empty inventory."""
        response = self.fake_response['voidTrader']
        response['active'] = True
        response['inventory'] = [{'name': f'name-{i}', 'cost': i * 10} for i in range(1, 9)]
        void_trader = self.manager.create_void_trader(response)

        self.assertTrue(void_trader.active)
        self.assertNotEqual(len(void_trader.inventory.items), 0)
        for item, item_data in zip(void_trader.inventory.items, response['inventory']):
            self.assertEqual(item.name, item_data['name'])
            self.assertEqual(item.cost, item_data['cost'])

    def test_prepare_void_trader(self):
        """Test: void_trader is set after prepare_void_trader."""
        self.assertIsNone(self.manager._void_trader)

        self.manager.prepare_void_trader()

        self.assertIsNotNone(self.manager._void_trader)

    def test_reduce_timer_of_trader_after_update_void_trader(self):
        """Test: reduce timer of trader after update_void_trader."""
        self.manager.create_void_trader(self.fake_response['voidTrader'])
        void_trader_old_time = self.manager._void_trader.timer.total_seconds
        self.manager.update_void_trader()

        self.assertNotEqual(self.manager._void_trader.timer.total_seconds, void_trader_old_time)
        self.assertLess(self.manager._void_trader.timer.total_seconds, void_trader_old_time)
        self.assertEqual(self.manager._void_trader.timer.total_seconds, void_trader_old_time - 60)

    def test_not_clear_inventory_while_timer_is_not_equal_0_after_update_void_trader(self):
        """Test: not clear inventory while timer is not equal 0 after update_void_trader."""
        self.fake_response['voidTrader']['active'] = True
        self.fake_response['voidTrader']['inventory'] = [{'name': f'name-{i}', 'cost': 10 * i} for i in range(1, 11)]
        self.manager.create_void_trader(self.fake_response['voidTrader'])

        self.assertTrue(self.manager._void_trader.active)
        self.assertEqual(len(self.manager._void_trader.inventory.items), 10)

        self.manager.update_void_trader()

        self.assertTrue(self.manager._void_trader.active)
        self.assertEqual(len(self.manager._void_trader.inventory.items), 10)

    def test_if_timer_is_equal_0_and_active_is_switched_from_true_to_false_after_update_void_trader(self):
        """Test: update timer and update trader attrs if timer is equal 0 and if active is switched from True to
        False."""
        expiry = datetime.utcnow() + timedelta(microseconds=500)
        self.fake_response['voidTrader']['expiry'] = expiry.isoformat()
        self.fake_response['voidTrader']['active'] = True
        self.fake_response['voidTrader']['inventory'] = [{'name': f'name-{i}', 'cost': 10 * i} for i in range(1, 11)]
        self.manager.create_void_trader(self.fake_response['voidTrader'])

        self.assertTrue(self.manager._void_trader.active)
        self.assertEqual(len(self.manager._void_trader.inventory.items), 10)

        self.manager.update_void_trader()

        self.assertFalse(self.manager._void_trader.active)
        self.assertEqual(len(self.manager._void_trader.inventory.items), 0)

    def test_if_timer_is_equal_0_and_active_is_switched_from_false_to_true_after_update_void_trader(self):
        """Test: update timer and update trader attrs if timer is equal 0 and if active is switched from False to
        True."""
        expiry = datetime.utcnow() + timedelta(microseconds=500)
        self.fake_response['voidTrader']['expiry'] = expiry.isoformat()

        self.manager.create_void_trader(self.fake_response['voidTrader'])

        self.assertFalse(self.manager._void_trader.active)
        self.assertEqual(len(self.manager._void_trader.inventory.items), 0)

        self.manager.update_void_trader()

        self.assertTrue(self.manager._void_trader.active)
        self.assertNotEqual(len(self.manager._void_trader.inventory.items), 0)


if __name__ == '__main__':
    unittest.main()
