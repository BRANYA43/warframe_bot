import unittest

import data
from objects import Mission
from objects.mixins import NameMixin


class TestMission(unittest.TestCase):
    """Test Mission"""

    def setUp(self) -> None:
        self.data = {
            'name': 'name',
            'location': data.LOCATIONS[0],
            'type': data.TYPES[0],
            'enemy': data.ENEMIES[0],
        }

    def test_mission_inherit_name_mixin(self):
        self.assertTrue(issubclass(Mission, NameMixin))

    def test_create_mission_with_correct_values(self):
        """Test: create Mission with correct values."""
        mission = Mission(**self.data)

        self.assertEqual(mission.name, self.data['name'])
        self.assertEqual(mission._location, 0)
        self.assertEqual(mission.location, self.data['location'])
        self.assertEqual(mission._type, 0)
        self.assertEqual(mission.type, self.data['type'])
        self.assertEqual(mission._enemy, 0)
        self.assertEqual(mission.enemy, self.data['enemy'])

    def test_not_create_mission_with_incorrect_location(self):
        """Test: not create Mission with incorrect location."""
        del self.data['location']
        self.assertRaisesRegex(TypeError, r'Expected str, but got (.+).', Mission, location=None, **self.data)
        self.assertRaisesRegex(ValueError, r'Value cannot be empty string.', Mission, location='', **self.data)
        self.assertRaisesRegex(ValueError, r'No such a location in locations data.', Mission, location='incorrect',
                               **self.data)

    def test_not_create_mission_with_incorrect_type(self):
        """Test: not create Mission with incorrect type."""
        del self.data['type']
        self.assertRaisesRegex(TypeError, r'Expected str, but got (.+).', Mission, type=None, **self.data)
        self.assertRaisesRegex(ValueError, r'Value cannot be empty string.', Mission, type='', **self.data)
        self.assertRaisesRegex(ValueError, r'No such a type in types data.', Mission, type='incorrect',
                               **self.data)

    def test_not_create_mission_with_incorrect_enemy(self):
        """Test: not create Mission with incorrect enemy."""
        del self.data['enemy']
        self.assertRaisesRegex(TypeError, r'Expected str, but got (.+).', Mission, enemy=None, **self.data)
        self.assertRaisesRegex(ValueError, r'Value cannot be empty string.', Mission, enemy='', **self.data)
        self.assertRaisesRegex(ValueError, r'No such a enemy in enemies data.', Mission, enemy='incorrect',
                               **self.data)


if __name__ == '__main__':
    unittest.main()
