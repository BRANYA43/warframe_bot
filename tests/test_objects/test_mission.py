import unittest

from objects.timer import Timer
from objects.mission import Mission
from test_objects.base_test import BaseTest


class TestMission(BaseTest):
    """Test Mission"""

    def setUp(self) -> None:
        self.name = 'name'
        self.timer = Timer(Timer.DAY + Timer.HOUR + Timer.MINUTE)
        self.mission = Mission(name=self.name, location=Mission.LOCATIONS[0], enemy=Mission.ENEMIES[0],
                               type_=Mission.TYPES[0], timer=self.timer)

    def test_create_mission_with_correct_values(self):
        """Test: create mission with correct values."""
        self.assertEqual(self.mission.name, self.name)
        self.assertEqual(self.mission.location, Mission.LOCATIONS[0])
        self.assertEqual(self.mission.enemy, Mission.ENEMIES[0])

    def test_not_create_mission_with_incorrect_values(self):
        """Test: not create mission with incorrect values."""
        with self.assertRaises((TypeError, ValueError)):
            for incorrect_value in [None, '', 'incorrect']:
                Mission(name=self.name, location=incorrect_value, enemy=incorrect_value)

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

    def test_get_info(self):
        """Test: get_info return correct info"""

        correct_info = f'Type: {self.mission.type}\n' \
                       f'Location: {self.mission.location}\n' \
                       f'Name: {self.mission.name}\n'
        info = self.mission.get_info()

        self.assertEqual(info, correct_info)


if __name__ == '__main__':
    unittest.main()
