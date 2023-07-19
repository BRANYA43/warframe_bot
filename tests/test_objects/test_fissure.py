import unittest

from objects.fissure import Fissure
from objects.mission import Mission
from objects.timer import Timer
from tests.test_objects.base_test import BaseTest


class TestFissure(BaseTest):
    """Test Fissure"""

    def setUp(self) -> None:
        self.id_ = 'id'
        self.timer = Timer(Timer.DAY + Timer.HOUR + Timer.MINUTE)
        self.mission = Mission(name='name', location=Mission.locations[0], enemy=Mission.enemies[0],
                               type=Mission.types[0], is_storm=False, is_hard=False)
        self.data = {
            'id': self.id_,
            'mission': self.mission,
            'tier': Fissure.tiers[0],
            'timer': self.timer,
        }
        self.fissure = Fissure(**self.data)

    def test_create_fissure_with_correct_values(self):
        """Test: create fissure with correct values."""
        self.assertEqual(self.fissure.id, self.id_)
        self.assertIsInstance(self.fissure.mission, Mission)
        self.assertEqual(self.fissure.tier, Fissure.tiers[0])
        self.assertIsInstance(self.fissure.timer, Timer)

    def test_raise_error_id_property(self):
        """Test: raise TyperError if id isn't str, raise ValueError if id is empty string."""
        del self.data['id']
        error_msgs = ['id must be str.', 'id cannot be empty string.']
        incorrect_values = [None, '']
        for value, error_msg in zip(incorrect_values, error_msgs):
            with self.assertRaises((TypeError, ValueError)) as e:
                Fissure(id=value, **self.data)
            self.check_error_message(e, error_msg)

    def test_raise_error_mission_property(self):
        """Test: raise TypeError if mission isn't Mission"""
        del self.data['mission']
        with self.assertRaises(TypeError) as e:
            Fissure(mission=None, **self.data)
        self.check_error_message(e, 'mission must be Mission.')

    def test_raise_error_tier_property(self):
        """Test: raise TyperError if tier isn't str, raise ValueError if tier is empty string, raise ValueError if type
        isn't within TIERS."""
        del self.data['tier']
        error_msgs = ['tier must be str.', 'tier cannot be empty string.', "'incorrect' is not in list"]
        incorrect_values = [None, '', 'incorrect']
        for value, error_msg in zip(incorrect_values, error_msgs):
            with self.assertRaises((TypeError, ValueError)) as e:
                Fissure(tier=value, **self.data)
            self.check_error_message(e, error_msg)

    def test_get_info(self):
        """Test: get correct info get_info"""
        correct_info = f'{self.mission.get_info()}' \
                       f'Relic Tier: {Fissure.tiers[0]}\n' \
                       f'Left time: {self.timer.get_str_time()}\n'
        self.assertEqual(self.fissure.get_info(), correct_info)


if __name__ == '__main__':
    unittest.main()
