import unittest
from datetime import datetime, timedelta

import data
from objects import Mission, Fissure
from objects.mixins import TimerMixin


class TestFissure(unittest.TestCase):
    """Test Fissure"""

    def setUp(self) -> None:
        self.data = {
            'id': 'some-id',
            'name': 'name',
            'location': data.LOCATIONS[0],
            'type': data.TYPES[0],
            'enemy': data.ENEMIES[0],
            'tier': data.TIERS[0],
            'expiry': datetime.utcnow() + timedelta(days=1)
        }

    def test_fissure_inherit_mission_and_timer_mixin(self):
        """Test: Fissure inherit Mission and TimerMixin."""
        self.assertTrue(issubclass(Fissure, Mission))
        self.assertTrue(issubclass(Fissure, TimerMixin))

    def test_create_fissure_with_correct_values(self):
        """Test: create Fissure with correct values."""
        fissure = Fissure(**self.data)

        self.assertEqual(fissure.id, self.data['id'])
        self.assertEqual(fissure.name, self.data['name'])
        self.assertEqual(fissure._location, 0)
        self.assertEqual(fissure.location, self.data['location'])
        self.assertEqual(fissure._type, 0)
        self.assertEqual(fissure.type, self.data['type'])
        self.assertEqual(fissure._enemy, 0)
        self.assertEqual(fissure.enemy, self.data['enemy'])
        self.assertEqual(fissure._tier, 0)
        self.assertEqual(fissure.tier, self.data['tier'])
        self.assertEqual(fissure.timer.expiry, self.data['expiry'])
        self.assertTrue(fissure.active)
        self.assertFalse(fissure.is_storm)
        self.assertFalse(fissure.is_hard)

    def test_create_fissure_with_correct_optional_attr_is_storm(self):
        """Test: create Fissure with correct optional attr is_storm."""
        fissure = Fissure(**self.data, is_storm=True)

        self.assertTrue(fissure.is_storm)

    def test_create_fissure_with_correct_optional_attr_is_hard(self):
        """Test: create Fissure with correct optional attr is_hard."""
        fissure = Fissure(**self.data, is_hard=True)

        self.assertTrue(fissure.is_hard)

    def test_not_create_fissure_with_incorrect_id(self):
        """Test: not create Fissure with incorrect id."""
        del self.data['id']
        self.assertRaisesRegex(TypeError, r'Expected str, but got (.+).', Fissure, id=None, **self.data)
        self.assertRaisesRegex(ValueError, r'Value cannot be empty string.', Fissure, id='', **self.data)

    def test_not_create_fissure_with_incorrect_tier(self):
        """Test: not create Fissure with incorrect tier."""
        del self.data['tier']
        self.assertRaisesRegex(TypeError, r'Expected str, but got (.+).', Fissure, tier=None, **self.data)
        self.assertRaisesRegex(ValueError, r'Value cannot be empty string.', Fissure, tier='', **self.data)
        self.assertRaisesRegex(ValueError, r'No such a tier in tiers data.', Fissure, tier='incorrect',
                               **self.data)

    def test_not_create_fissure_with_incorrect_optional_attr_is_storm(self):
        """Test: not create fissure with incorrect optional attr is_storm."""
        self.assertRaisesRegex(TypeError, r'Expected bool, but got (.+).', Fissure, is_storm=None, **self.data)

    def test_not_create_fissure_with_incorrect_optional_attr_is_hard(self):
        """Test: not create fissure with incorrect optional attr is_hard."""
        self.assertRaisesRegex(TypeError, r'Expected bool, but got (.+).', Fissure, is_hard=None, **self.data)

    def test_not_create_fissure_if_all_optional_attrs_is_true(self):
        """test not create Fissure if all optional attrs is True"""
        self.assertRaisesRegex(ValueError, r'Only one optional attr can be True.', Fissure, is_storm=True, is_hard=True,
                               **self.data)

    def test_not_change_active_after_update(self):
        """Test: not change active after update if timer isn't equal 0."""
        fissure = Fissure(**self.data)

        self.assertTrue(fissure.active)

        fissure.update()

        self.assertTrue(fissure.active)

    def test_change_active_after_update(self):
        """Test: change active after update if timer is equal 0."""
        self.data['expiry'] = datetime.utcnow() + timedelta(milliseconds=500)
        fissure = Fissure(**self.data)

        self.assertTrue(fissure.active)

        fissure.update()

        self.assertFalse(fissure.active)

    def test_get_info(self):
        """Test: get_info returns correct info."""
        fissure = Fissure(**self.data)
        correct_info = (
            f'Node: {fissure.name}',
            f'Location: {fissure.location}',
            f'Type: {fissure.type}',
            f'Enemy: {fissure.enemy}',
            f'Tier: {fissure.tier}',
            f'Left time: {fissure.timer.get_str_time()}',
        )

        self.assertEqual(fissure.get_info(), correct_info)


if __name__ == '__main__':
    unittest.main()
