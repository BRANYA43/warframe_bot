import datetime
import unittest

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
            'fissures': [
                {
                    'id': 'id_0',
                    'expiry': self.expiry_str,
                    'node': f'name ({Mission.locations[0]})',
                    'missionType': Mission.types[0],
                    'enemy': Mission.enemies[0],
                    'tier': Fissure.tiers[0],
                    'isStorm': False,
                    'isHard': False,

                },
                {
                    'id': 'id_1',
                    'expiry': self.expiry_str,
                    'node': f'name ({Mission.locations[3]})',
                    'missionType': Mission.types[0],
                    'enemy': Mission.enemies[0],
                    'tier': Fissure.tiers[0],
                    'isStorm': True,
                    'isHard': False,

                },
                {
                    'id': 'id_2',
                    'expiry': self.expiry_str,
                    'node': f'name ({Mission.locations[0]})',
                    'missionType': Mission.types[0],
                    'enemy': Mission.enemies[0],
                    'tier': Fissure.tiers[0],
                    'isStorm': False,
                    'isHard': True,

                },
            ]
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
        self.assertIsInstance(self.manager._fissures, dict)
        self.assertIsInstance(self.manager._fissures_for_delete, list)
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

    def test_after_update_cycle_the_timer_time_is_less(self):
        """Test: update cycle after that the timer time must be less."""
        self.manager._response = self.fake_response
        cycle = self.manager.create_cycle(key='earthCycle', name='earth', cycles=['day', 'night'])
        old_raw_seconds = cycle.timer.raw_seconds

        self.manager.update_cycle(key='earthCycle')

        self.assertLess(cycle.timer.raw_seconds, old_raw_seconds)

    def test_after_update_cycle_the_timer_must_have_new_time(self):
        """Test: update cycle after that the timer time that equal 0 must have new time."""
        self.manager._response = self.fake_response
        cycle = self.manager.create_cycle(key='earthCycle', name='earth', cycles=['day', 'night'])
        cycle.timer.raw_seconds = 0

        self.manager._response = self.fake_response

        self.manager.update_cycle(key='earthCycle')

        self.assertEqual(cycle.timer.days, 1)

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
        self.assertEqual(mission.location, Mission.locations[0])
        self.assertEqual(mission.type, Mission.types[0])
        self.assertEqual(mission.enemy, Mission.enemies[0])
        self.assertFalse(mission.is_storm)
        self.assertFalse(mission.is_hard)

    def test_create_mission_with_is_storm_is_true(self):
        """Test: create Mission and return Mission with location 'Earth Proxima'"""
        fissure_response = self.fake_response['fissures'][1]
        data = self.get_mission_data(fissure_response)
        mission = self.manager.create_mission(**data)

        self.assertEqual(mission.location, Mission.locations[22])
        self.assertTrue(mission.is_storm)
        self.assertFalse(mission.is_hard)

    def test_create_mission_with_is_hard_is_true(self):
        """Test: create Mission and return Mission where get_info return 'This is mission of steel path'"""
        fissure_response = self.fake_response['fissures'][2]
        data = self.get_mission_data(fissure_response)
        mission = self.manager.create_mission(**data)

        self.assertFalse(mission.is_storm)
        self.assertTrue(mission.is_hard)

    def test_create_fissure(self):
        """Test: create Fissure than add Fissure to fissures and return created Fissure."""
        self.manager._response = self.fake_response
        fissure = self.manager.create_fissure(index=0)
        managers_fissure = self.manager._fissures.get(fissure.id)

        self.assertIsNotNone(managers_fissure)
        self.assertIsInstance(managers_fissure, Fissure)
        self.assertIs(fissure, managers_fissure)
        self.assertEqual(fissure.mission.name, 'name')
        self.assertEqual(fissure.mission.location, Mission.locations[0])
        self.assertEqual(fissure.mission.type, Mission.types[0])
        self.assertEqual(fissure.mission.enemy, Mission.enemies[0])
        self.assertFalse(fissure.mission.is_hard)
        self.assertEqual(fissure.timer.days, 1)

    def test_timer_is_less_after_update_fissure(self):
        """Test: timer is less after update_fissure."""
        self.manager._response = self.fake_response
        fissure = self.manager.create_fissure(index=0)
        old_raw_seconds = fissure.timer.raw_seconds

        self.manager.update_fissure(id=fissure.id)

        self.assertLess(fissure.timer.raw_seconds, old_raw_seconds)

    def test_not_append_fissure_id_in_the_fissures_for_delete_after_update_fissure(self):
        """Test: not append Fissure.id in fissures_for_delete after update_fissure if timer is 0 and fissure.id is in response."""
        self.manager._response = self.fake_response
        fissure = self.manager.create_fissure(index=0)
        id_ = fissure.id

        self.assertIsNotNone(self.manager._fissures.get(id_))
        self.assertEqual(len(self.manager._fissures_for_delete), 0)

        fissure.timer.raw_seconds = 0
        self.manager.update_fissure(id_)

        self.assertIsNotNone(self.manager._fissures.get(id_))
        self.assertEqual(len(self.manager._fissures_for_delete), 0)

    def test_append_fissure_id_in_the_fissures_for_delete_after_update(self):
        """
        Test: append Fissure.id in fissures_for_delete after update_fissure if timer is 0 and if id isn't in response.
        """
        self.manager._response = self.fake_response
        fissure = self.manager.create_fissure(index=0)
        id_ = fissure.id

        self.assertIsNotNone(self.manager._fissures.get(id_))
        self.assertEqual(len(self.manager._fissures_for_delete), 0)

        del self.manager._response['fissures'][0]
        fissure.timer.raw_seconds = 0
        self.manager.update_fissure(id_)

        self.assertEqual(len(self.manager._fissures_for_delete), 1)
        self.assertIn(fissure.id, self.manager._fissures_for_delete)

    def test_not_append_fissure_id_in_fissures_for_delete_after_update_if_id_is_in_this_list(self):
        """Test: not append Fissure.id in fissures_for_delete after update_fissure if id is in fissures_for_delete."""
        self.manager._response = self.fake_response
        fissure = self.manager.create_fissure(index=0)
        id_ = fissure.id

        self.assertIsNotNone(self.manager._fissures.get(id_))
        self.assertEqual(len(self.manager._fissures_for_delete), 0)

        del self.manager._response['fissures'][0]
        fissure.timer.raw_seconds = 0
        self.manager.update_fissure(id_)

        self.assertEqual(len(self.manager._fissures_for_delete), 1)
        self.assertIn(fissure.id, self.manager._fissures_for_delete)

        self.manager.update_fissure(id_)

        self.assertEqual(len(self.manager._fissures_for_delete), 1)
        self.assertIn(fissure.id, self.manager._fissures_for_delete)

    def test_delete_fissure(self):
        """Test: delete Fissure of fissures."""
        self.manager._response = self.fake_response
        fissure = self.manager.create_fissure(index=0)
        self.manager._fissures_for_delete.append(fissure.id)

        self.assertEqual(len(self.manager._fissures_for_delete), 1)
        self.assertIsNotNone(self.manager._fissures.get(fissure.id))

        self.manager.delete_fissure(fissure.id)

        self.assertEqual(len(self.manager._fissures_for_delete), 0)
        self.assertIsNone(self.manager._fissures.get(fissure.id))

    def test_get_fissures_info(self):
        """Test: get_fissures_info returns correct info"""
        self.manager._response = self.fake_response
        fissure_0 = self.manager.create_fissure(index=0)
        fissure_1 = self.manager.create_fissure(index=1)
        fissure_2 = self.manager.create_fissure(index=2)

        info = self.manager.get_fissures_info()

        self.assertIn(
            'Missions of Simple\n' + fissure_0.get_info(),
            info,
        )
        self.assertIn(
            'Missions of Railjack\n' + fissure_1.get_info(),
            info,
        )
        self.assertIn(
            'Missions of Steel Path\n' + fissure_2.get_info(),
            info,
        )

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
        self.assertEqual(len(self.manager._fissures), 0)

        self.manager.prepare()

        self.assertTrue(self.manager.is_ready)
        self.assertIsInstance(self.manager._response, dict)
        self.assertEqual(self.manager._response['timestamp'][-1], 'Z')

        self.assertNotEqual(len(self.manager._cycles), 0)
        for cycle in self.manager._cycles.values():
            self.assertIsInstance(cycle, Cycle)

        self.assertNotEqual(len(self.manager._fissures), 0)
        for fissure in self.manager._fissures.values():
            self.assertIsInstance(fissure, Fissure)

    def test_update(self):
        """Test: update values of manager attributes."""
        self.manager.set_response()
        old_response = self.manager._response
        self.manager.prepare()
        self.manager.update()

        # TODO придумать как проверить обновленны ли циклы и тд

        self.assertIsNot(self.manager._response, old_response)


if __name__ == '__main__':
    unittest.main()
