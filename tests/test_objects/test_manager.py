import datetime
import unittest
from pprint import pprint

from objects.cycle import Cycle
from objects.fissure import Fissure
from objects.manager import Manager
from objects.mission import Mission
from objects.timer import Timer
from test_objects.base_test import BaseTest


class TestManager(BaseTest):
    """Test Manager"""

    def setUp(self) -> None:
        self.expiry_datetime = datetime.datetime.utcnow() + datetime.timedelta(hours=25)
        self.expiry_str = self.expiry_datetime.isoformat() + 'Z'
        self.manager = Manager()
        self.fake_response = {
            'earthCycle': {
                'expiry': self.expiry_str,
                'state': 'day',
            },
            'cetusCycle': {
                'expiry': self.expiry_str,
                'state': 'day',
            },
            'fissures': {
                0: {
                    'id': 'id_0',
                    'expiry': self.expiry_str,
                    'node': f'name ({Mission.LOCATIONS[0]})',
                    'missionType': Mission.TYPES[0],
                    'enemy': Mission.ENEMIES[0],
                    'tier': Fissure.TIERS[0],
                    'isStorm': False,
                    'isHard': False,

                },
                1: {
                    'id': 'id_1',
                    'expiry': self.expiry_str,
                    'node': f'name ({Mission.LOCATIONS[2]})',
                    'missionType': Mission.TYPES[0],
                    'enemy': Mission.ENEMIES[0],
                    'tier': Fissure.TIERS[0],
                    'isStorm': True,
                    'isHard': False,

                },
                2: {
                    'id': 'id_2',
                    'expiry': self.expiry_str,
                    'node': f'name ({Mission.LOCATIONS[0]})',
                    'missionType': Mission.TYPES[0],
                    'enemy': Mission.ENEMIES[0],
                    'tier': Fissure.TIERS[0],
                    'isStorm': False,
                    'isHard': True,

                },
            }
        }

    @staticmethod
    def get_mission_data(response: dict) -> dict:
        return {
            'node': response['node'],
            'type': response['missionType'],
            'enemy': response['enemy'],
            'is_storm': response['isStorm'],
            'is_hard': response['isHard'],
        }

    def test_values_of_attrs_after_create_manager(self):
        """Test: create manager"""
        self.assertFalse(self.manager.is_ready)
        self.assertIsNone(self.manager._response)
        self.assertIsInstance(self.manager._cycles, dict)
        self.assertEqual(self.manager._url, 'https://api.warframestat.us/pc/')
        self.assertEqual(self.manager._cycle_keys, ('earthCycle', 'cetusCycle', 'vallisCycle', 'cambionCycle',
                                                    'zarimanCycle',))

    def test_get_timer(self):
        """Test: get_timer"""
        expiry = self.fake_response['earthCycle']['expiry']
        timer = self.manager.get_timer(expiry=expiry)

        self.assertIsInstance(timer, Timer)
        self.assertEqual(timer.days, 1)

        expiry = datetime.datetime.utcnow().isoformat() + 'Z'
        timer = self.manager.get_timer(expiry=expiry)
        self.assertEqual(timer.raw_seconds, 0)

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
        self.assertIsInstance(cycle.timer, Timer)
        self.assertEqual(cycle.timer.days, 1)

    def test_update_cycle(self):
        """Test: update attributes of Cycle"""
        self.manager._response = self.fake_response
        cycle = self.manager.create_cycle(key='earthCycle', name='earth', cycles=['day', 'night'])
        self.expiry_datetime = self.expiry_datetime + datetime.timedelta(days=1)
        self.expiry_str = self.expiry_datetime.isoformat() + 'Z'
        self.fake_response['earthCycle']['expiry'] = self.expiry_str
        self.fake_response['earthCycle']['state'] = 'night'
        self.manager._response = self.fake_response
        cycle_response = self.fake_response['earthCycle']
        cycle.timer.raw_seconds = 0

        self.manager.update_cycle(key='earthCycle')

        self.assertEqual(cycle.current_cycle, cycle_response['state'])
        self.assertEqual(cycle.next_cycle, 'day')
        self.assertEqual(cycle.timer.days, 2)

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

    def test_create_mission(self):
        """Test: create Mission that return created Mission"""
        fissure_response = self.fake_response['fissures'][0]
        data = self.get_mission_data(fissure_response)
        mission = self.manager.create_mission(**data)

        self.assertEqual(mission.name, 'name')
        self.assertEqual(mission.location, Mission.LOCATIONS[0])
        self.assertEqual(mission.type, Mission.TYPES[0])
        self.assertEqual(mission.enemy, Mission.ENEMIES[0])
        self.assertFalse(mission.is_hard)

    def test_create_mission_with_is_storm_is_true(self):
        """Test: create Mission and return Mission with location 'Earth Proxima'"""
        fissure_response = self.fake_response['fissures'][1]
        data = self.get_mission_data(fissure_response)
        mission = self.manager.create_mission(**data)

        self.assertEqual(mission.location, Mission.LOCATIONS[19])

    def test_create_mission_with_is_hard_is_true(self):
        """Test: create Mission and return Mission where get_info return 'This is mission of steel path'"""
        fissure_response = self.fake_response['fissures'][2]
        data = self.get_mission_data(fissure_response)
        mission = self.manager.create_mission(**data)

        self.assertTrue(mission.is_hard)
        self.assertIn('This is mission of steel path', mission.get_info())

    def test_create_fissure(self):
        """Test: create Fissure than add Fissure to fissures and return created Fissure."""

    def test_update_fissure(self):
        """Test: update fissures timers."""

    def test_delete_fissure(self):
        """Test: delete Fissure of fissures."""

    def test_get_fissures_info(self):
        """Test: get_fissures_info returns correct info"""

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
