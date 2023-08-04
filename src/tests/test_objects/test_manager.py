import unittest
from datetime import datetime, timedelta

import data
from objects import Manager, Place


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


if __name__ == '__main__':
    unittest.main()
