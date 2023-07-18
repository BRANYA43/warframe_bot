import unittest

from objects.mission import Mission
from test_objects.base_test import BaseTest


class TestMission(BaseTest):
    """Test Mission"""

    def setUp(self) -> None:
        self.name = 'name'
        self.mission = Mission(name=self.name, location=Mission.LOCATIONS[0], enemy=Mission.ENEMIES[0],
                               type=Mission.TYPES[0], is_storm=False, is_hard=False)

    def test_create_mission_with_correct_values(self):
        """Test: create mission with correct values."""
        self.assertEqual(self.mission.name, self.name)
        self.assertEqual(self.mission.location, Mission.LOCATIONS[0])
        self.assertEqual(self.mission.enemy, Mission.ENEMIES[0])
        self.assertEqual(self.mission.type, Mission.TYPES[0])
        self.assertFalse(self.mission.is_storm)
        self.assertFalse(self.mission.is_hard)

    def test_not_create_mission_with_incorrect_values(self):
        """Test: not create mission with incorrect values."""
        with self.assertRaises((TypeError, ValueError)):
            for incorrect_value in [None, '', 'incorrect']:
                Mission(name=self.name, location=incorrect_value, enemy=incorrect_value, type=incorrect_value,
                        is_storm=False, is_hard=False)

    def test_raise_errors_location_property(self):
        """
        Test: raise TypeError if location isn't str, raise ValueError if location is empty string, raise ValueError
        if location isn't within LOCATIONS.
        """
        with self.assertRaises(TypeError) as e:
            self.mission.location = None
        self.check_error_message(e, 'location must be str.')

        with self.assertRaises(ValueError) as e:
            self.mission.location = ''
        self.check_error_message(e, 'location cannot be empty string.')

        with self.assertRaises(ValueError):
            self.mission.location = 'incorrect'

    def test_raise_errors_enemy_property(self):
        """
        Test: raise TypeError if enemy isn't str, raise ValueError if enemy is empty string, raise ValueError if enemy
        isn't within ENEMIES.
        """
        with self.assertRaises(TypeError) as e:
            self.mission.enemy = None
        self.check_error_message(e, 'enemy must be str.')

        with self.assertRaises(ValueError) as e:
            self.mission.enemy = ''
        self.check_error_message(e, 'enemy cannot be empty string.')

        with self.assertRaises(ValueError):
            self.mission.enemy = 'incorrect'

    def test_raise_errors_type_property(self):
        """
        Test: raise TypeError if type isn't str, raise ValueError if type is empty string, raise ValueError if type
        isn't within TYPES.
        """
        with self.assertRaises(TypeError) as e:
            self.mission.type = None
        self.check_error_message(e, 'type must be str.')

        with self.assertRaises(ValueError) as e:
            self.mission.type = ''
        self.check_error_message(e, 'type cannot be empty string.')

        with self.assertRaises(ValueError):
            self.mission.type = 'incorrect'

    def test_raise_errors_is_storm_property(self):
        """
        Test: raise TypeError if is_storm isn't bool
        """
        with self.assertRaises(TypeError) as e:
            self.mission.is_storm = None
        self.check_error_message(e, 'is_storm must be bool.')

    def test_raise_errors_is_hard_property(self):
        """
        Test: raise TypeError if is_hard isn't bool
        """
        with self.assertRaises(TypeError) as e:
            self.mission.is_hard = None
        self.check_error_message(e, 'is_hard must be bool.')

    def test_get_info(self):
        """Test: get_info return correct info"""
        correct_info = f'Type: {self.mission.type}\n' \
                       f'Location: {self.mission.location}\n' \
                       f'Name: {self.mission.name}\n'
        info = self.mission.get_info()

        self.assertEqual(info, correct_info)

        self.mission.is_storm = True
        self.assertIn('This is mission of railjack.', self.mission.get_info())

        self.mission.is_hard = True
        self.assertIn('This is mission of steel path.', self.mission.get_info())


if __name__ == '__main__':
    unittest.main()
