import datetime
import unittest

from objects.cycle import Cycle
from objects.manager import Manager
from test_objects.base_test import BaseTest


class TestManager(BaseTest):
    """Test Manager"""

    def setUp(self) -> None:
        self.manager = Manager()
        self.fake_response = {
            'earthCycle': {
                'timeLeft': '1d 1m',
                'state': 'day',
            },
            'cetusCycle': {
                'timeLeft': '1d 1m',
                'state': 'day',
            },
        }

    def test_values_of_attrs_after_create_manager(self):
        """Test: create manager"""
        self.assertFalse(self.manager.is_ready)
        self.assertIsNone(self.manager._response)
        self.assertIsInstance(self.manager._cycles, dict)
        self.assertEqual(self.manager._url, 'https://api.warframestat.us/pc/')
        self.assertEqual(self.manager._cycle_keys, ('earthCycle', 'cetusCycle', 'vallisCycle', 'cambionCycle',
                                                    'zarimanCycle',))

    def test_create_cycle(self):
        """Test: create cycle than add Cycle to cycles and return created Cycle."""
        self.manager._response = self.fake_response
        cycle_response = self.fake_response['earthCycle']

        self.assertEqual(len(self.manager._cycles), 0)

        cycle = self.manager.create_cycle(key='earthCycle', name='earth', cycles=['day', 'night'])

        self.assertEqual(len(self.manager._cycles), 1)
        self.assertIsInstance(cycle, Cycle)
        self.assertIsInstance(self.manager._cycles['earthCycle'], Cycle)
        self.assertEqual(cycle.name, 'earth')
        self.assertEqual(cycle.cycles, ['day', 'night'])
        self.assertEqual(cycle.current_cycle, cycle_response['state'])
        self.assertEqual(cycle.next_cycle, 'night')
        self.assertEqual(cycle.left_time, cycle_response['timeLeft'])

    def test_update_cycle(self):
        """Test: update attributes of Cycle"""
        self.manager._response = self.fake_response
        cycle = self.manager.create_cycle(key='earthCycle', name='earth', cycles=['day', 'night'])

        self.fake_response['earthCycle']['timeLeft'] = '2d 3m'
        self.fake_response['earthCycle']['state'] = 'night'
        self.manager._response = self.fake_response
        cycle_response = self.fake_response['earthCycle']

        self.manager.update_cycle(key='earthCycle')

        self.assertEqual(cycle.current_cycle, cycle_response['state'])
        self.assertEqual(cycle.next_cycle, 'day')
        self.assertEqual(cycle.left_time, cycle_response['timeLeft'])

    def test_get_cycles_info(self):
        """Test: get_cycle_data"""
        self.manager._response = self.fake_response
        self.manager.create_cycle(key='earthCycle', name='earth', cycles=['day', 'night'])
        self.manager.create_cycle(key='cetusCycle', name='cetus', cycles=['day', 'night'])
        earth = self.manager._cycles['earthCycle']
        cetus = self.manager._cycles['cetusCycle']
        correct_cycle_info = earth.get_info() + '\n' + cetus.get_info() + '\n'

        cycles_info = self.manager.get_cycles_info()

        self.assertIsInstance(cycles_info, str)
        self.assertEqual(cycles_info, correct_cycle_info)

    def test_set_response(self):
        """Test: set response by url"""
        self.assertIsNone(self.manager._response)

        self.manager.set_response()

        self.assertIsInstance(self.manager._response, dict)
        self.assertEqual(self.manager._response['timestamp'][-1], 'Z')

    def test_prepare(self):
        """Test: prepare manager for start work."""
        self.assertFalse(self.manager.is_ready)
        self.assertIsNone(self.manager._response)
        self.assertEqual(len(self.manager._cycles), 0)

        self.manager.prepare()

        self.assertTrue(self.manager.is_ready)
        self.assertIsInstance(self.manager._response, dict)
        self.assertEqual(self.manager._response['timestamp'][-1], 'Z')

        self.assertNotEqual(len(self.manager._cycles), 0)
        for cycle in self.manager._cycles.values():
            self.assertIsInstance(cycle, Cycle)

    def test_update(self):
        """Test: update values of manager attributes."""
        self.manager.set_response()
        old_response = self.manager._response

        self.test_create_cycle()

        self.assertIsNot(self.manager._response, old_response)


if __name__ == '__main__':
    unittest.main()
