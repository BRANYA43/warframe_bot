import asyncio
import unittest
from datetime import datetime, timedelta

import data
from objects import Manager, Place, Item, VoidTrader, SteelTrader, Fissure, FissureStorage


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
                'location': data.RELAYS[0],
                'inventory': []
            },
            'steelPath': {
                'currentReward':
                    {
                        'name': 'name-1',
                        'cost': 10,
                    },
                'expiry': self.steel_path_trader_expiry.isoformat(),
                'rotation': [{'name': f'name-{i}', 'cost': i * 10} for i in range(1, 9)]
            },
        }
        self.manager = Manager()

    def test_manager_has_void_trader_and_steel_trader(self):
        """Test: Manager has void_trader and steel_trader."""
        self.assertIsNone(self.manager._void_trader)
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

    def test_create_steel_trader(self):
        """Test: create_steel_trader set steel_trader and returns SteelTrader."""
        response = self.fake_response['steelPath']
        steel_trader = self.manager.create_steel_trader(response)

        self.assertIsNotNone(self.manager._steel_trader)
        self.assertIsInstance(self.manager._steel_trader, SteelTrader)
        self.assertEqual(steel_trader, self.manager._steel_trader)
        self.assertEqual(steel_trader.timer.expiry, self.steel_path_trader_expiry)
        self.assertEqual(steel_trader.current_offer.name, response['currentReward']['name'])
        self.assertEqual(steel_trader.current_offer.cost, response['currentReward']['cost'])
        self.assertEqual(steel_trader.next_offer.name, response['rotation'][1]['name'])
        self.assertEqual(steel_trader.next_offer.cost, response['rotation'][1]['cost'])
        for item, item_data in zip(steel_trader.offers, response['rotation']):
            self.assertEqual(item.name, item_data['name'])
            self.assertEqual(item.cost, item_data['cost'])

    def test_prepare_steel_trader(self):
        """Test: steel_trader is set after prepare_steel_trader."""
        self.assertIsNone(self.manager._steel_trader)

        self.manager.prepare_steel_trader()

        self.assertIsNotNone(self.manager._steel_trader)

    def test_reduce_timer_after_update_steel_trader(self):
        """Test: reduce timer after update_steel_trader."""
        self.manager.create_steel_trader(self.fake_response['steelPath'])
        old_total_second = self.manager._steel_trader.timer.total_seconds

        self.manager.update_steel_trader()

        self.assertNotEqual(self.manager._steel_trader.timer.total_seconds, old_total_second)
        self.assertLess(self.manager._steel_trader.timer.total_seconds, old_total_second)
        self.assertEqual(self.manager._steel_trader.timer.total_seconds, old_total_second - 60)

    def test_update_timer_if_timer_is_equal_0_and_update_trader_attrs_after_update_steel_trader(self):
        """Test: update timer if timer is equal 0 and update trader attrs after update_steel_trader."""
        expiry = datetime.utcnow() + timedelta(microseconds=500)
        self.fake_response['steelPath']['expiry'] = expiry.isoformat()
        self.manager.create_steel_trader(self.fake_response['steelPath'])
        old_expiry = self.manager._steel_trader.timer.expiry

        self.assertEqual(self.manager._steel_trader.current_offer.name, 'name-1')
        self.assertEqual(self.manager._steel_trader.next_offer.name, 'name-2')

        self.manager.update_steel_trader()

        self.assertEqual(self.manager._steel_trader.current_offer.name, 'name-2')
        self.assertEqual(self.manager._steel_trader.next_offer.name, 'name-3')
        self.assertNotEqual(self.manager._steel_trader.timer.expiry, old_expiry)
        self.assertLess(old_expiry, self.manager._steel_trader.timer.expiry)
        self.assertEqual(self.manager._steel_trader.timer.expiry,
                         old_expiry + self.manager._steel_trader.TIME_TO_CHANGING_OFFER)


class TestManagerWorkForFissures(unittest.TestCase):
    """Test manager's work for fissures"""

    def setUp(self) -> None:
        expiry = datetime.utcnow() + timedelta(days=1)
        self.fake_response = {
            'id': 'some_id',
            'expiry': expiry.isoformat(),
            'active': True,
            'node': 'node (Earth)',
            'missionType': data.TYPES[0],
            'enemy': data.ENEMIES[0],
            'tier': data.TIERS[0],
            'isStorm': False,
            'isHard': False,
        }

        self.manager = Manager()

    def test_manager_has_needed_attrs(self):
        """Test: Manager has fissure_storage."""
        self.assertIsInstance(self.manager.fissure_storage, FissureStorage)
        self.assertFalse(self.manager.is_delete_fissures)

    def test_create_fissure(self):
        """Test: create_fissure add fissure to fissure_storage and has correct attrs."""
        fissure = self.manager.create_fissure(self.fake_response)
        name, location = self.fake_response['node'].split()
        location = location[1:-1]

        self.assertIsInstance(fissure, Fissure)
        self.assertEqual(len(self.manager._fissure_storage.get_all_fissure_list()), 1)
        self.assertIs(fissure, self.manager._fissure_storage.get_all_fissure_list()[0])
        self.assertEqual(fissure.name, name)
        self.assertEqual(fissure.location, location)
        self.assertEqual(fissure.type, self.fake_response['missionType'])
        self.assertEqual(fissure.enemy, self.fake_response['enemy'])
        self.assertEqual(fissure.tier, self.fake_response['tier'])
        self.assertFalse(fissure.is_storm)
        self.assertFalse(fissure.is_hard)

    def test_prepare_fissures(self):
        """Test: prepare_fissures fill fissure_storage"""
        self.assertEqual(len(self.manager._fissure_storage.get_all_fissure_list()), 0)

        self.manager.prepare_fissures()

        self.assertLess(0, len(self.manager._fissure_storage.get_all_fissure_list()))

    def test_reduce_timer_after_update_fissures(self):
        fissure = self.manager.create_fissure(self.fake_response)
        old_total_seconds = fissure.timer.total_seconds

        self.manager.update_fissures()

        self.assertNotEqual(fissure.timer.total_seconds, old_total_seconds)
        self.assertLess(fissure.timer.total_seconds, old_total_seconds)
        self.assertEqual(fissure.timer.total_seconds, old_total_seconds - 60)

    def test_update_attrs_fissures_after_update_fissures(self):
        """Test: update fissure attrs after update_fissures if timer is equal 0."""
        expiry = datetime.utcnow() + timedelta(milliseconds=500)
        self.fake_response['expiry'] = expiry.isoformat()
        fissure = self.manager.create_fissure(self.fake_response)

        self.assertTrue(fissure.active)

        self.manager.update_fissures()

        self.assertFalse(fissure.active)

    def test_delete_fissure_after_update_fissures(self):
        """Test: delete fissure after update_fissures if active is False."""
        expiry = datetime.utcnow() + timedelta(milliseconds=500)
        self.fake_response['expiry'] = expiry.isoformat()
        self.manager.create_fissure(self.fake_response)

        self.assertFalse(self.manager.is_delete_fissures)
        self.assertEqual(len(self.manager._fissure_storage.get_all_fissure_list()), 1)

        self.manager.update_fissures()

        self.assertTrue(self.manager.is_delete_fissures)
        self.assertEqual(len(self.manager._fissure_storage.get_all_fissure_list()), 0)

    def test_get_info_of_simple_fissures(self):
        """Test: get_info_of_simple_fissures is correct info."""
        self.manager.prepare_fissures()
        fissures_by_tier = self.manager.fissure_storage.get_fissures('simple')
        correct_info = [[fissure.get_info() for fissure in fissures] for fissures in fissures_by_tier.values()]

        self.assertEqual(self.manager.get_fissures_info('simple'), correct_info)

    def test_get_info_of_storm_fissures(self):
        """Test: get_info_of_storm_fissures is correct info."""
        self.manager.prepare_fissures()
        fissures_by_tier = self.manager.fissure_storage.get_fissures('storm')
        correct_info = [[fissure.get_info() for fissure in fissures] for fissures in fissures_by_tier.values()]

        self.assertEqual(self.manager.get_fissures_info('storm'), correct_info)

    def test_get_info_of_hard_fissures(self):
        """Test: get_info_of_hard_fissures is correct info."""
        self.manager.prepare_fissures()
        fissures_by_tier = self.manager.fissure_storage.get_fissures('hard')
        correct_info = [[fissure.get_info() for fissure in fissures] for fissures in fissures_by_tier.values()]

        self.assertEqual(self.manager.get_fissures_info('hard'), correct_info)

    def test_get_info_of_kuva_fissures(self):
        """Test: get_info_of_kuva_fissures is correct info."""
        self.manager.prepare_fissures()
        fissures = self.manager.fissure_storage.get_fissures('kuva')
        correct_info = [fissure.get_info() for fissure in fissures]

        self.assertEqual(self.manager.get_fissures_info('kuva'), correct_info)


if __name__ == '__main__':
    unittest.main()
