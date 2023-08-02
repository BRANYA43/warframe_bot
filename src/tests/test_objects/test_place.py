import unittest
from datetime import datetime, timedelta

import data
from objects.mixins import NameMixin, TimerMixin
from objects import Place, Cycle


class TestPlace(unittest.TestCase):
    """Test Place"""

    def setUp(self) -> None:
        self.expiry = datetime.utcnow() + timedelta(days=1)
        self.data = {
            'name': 'name',
            'expiry': self.expiry,
            'cycles': data.CYCLES['earth'],
            'current_cycle': 'day',
        }

    def test_place_inherit_needed_mixins(self):
        """Test: Place inherit NameMixin and TimerMixin"""
        self.assertTrue(issubclass(Place, NameMixin))
        self.assertTrue(issubclass(Place, TimerMixin))

    def test_create_place_with_correct_values(self):
        """Test: create Place with correct values"""
        place = Place(**self.data)

        self.assertIsInstance(place._cycles, tuple)
        self.assertEqual(place._cycles, self.data['cycles'])
        self.assertIsInstance(place._cycles[0], Cycle)
        self.assertIsInstance(place._cycles[1], Cycle)
        self.assertEqual(place._cycles[0].name, 'day')
        self.assertEqual(place._cycles[1].name, 'night')
        self.assertEqual(place._cycles[0].duration, timedelta(hours=4))
        self.assertEqual(place._cycles[1].duration, timedelta(hours=4))
        self.assertEqual(place._current_cycle, 0)  # index item of place._cycles
        self.assertEqual(place._next_cycle, 1)  # index item of place._cycles

    def test_not_create_place_with_incorrect_cycles(self):
        """Test: not create Place with incorrect cycles."""
        del self.data['cycles']
        self.assertRaisesRegex(TypeError, r'Expected tuple, but got (.+).', Place, cycles=None, **self.data)
        self.assertRaisesRegex(ValueError, r'Cycles must have 2 items minimal.', Place, cycles=(), **self.data)
        self.assertRaisesRegex(ValueError, r'Cycles must have 2 items minimal.', Place, cycles=(None,), **self.data)
        self.assertRaisesRegex(TypeError, r'Each item in cycles tuple must be Cycle.', Place, cycles=(None, None),
                               **self.data)
        self.assertRaisesRegex(TypeError, r'Each item in cycles tuple must be Cycle.', Place,
                               cycles=(data.CYCLES['earth'][0], None), **self.data)

    def test_not_create_place_with_incorrect_current_cycle(self):
        """Test: not create Place with incorrect current_cycle."""
        del self.data['current_cycle']
        self.assertRaisesRegex(TypeError, r'Expected str, but got (.+).', Place, current_cycle=None, **self.data)
        self.assertRaisesRegex(ValueError, r'Value cannot be empty string.', Place, current_cycle='', **self.data)
        self.assertRaisesRegex(ValueError, 'Current cycle must be name of Cycle from cycles tuple.', Place,
                               current_cycle='incorrect', **self.data)

    def test_set_next_current_as_index_next_item_of_tuple_cycles(self):
        """Test: set next_current as index of next item of tuple cycles that different from current_cycle."""
        place = Place(**self.data)

        self.assertEqual(place._current_cycle, 0)
        self.assertEqual(place._next_cycle, 1)

        self.data['current_cycle'] = 'night'
        place = Place(**self.data)

        self.assertEqual(place._current_cycle, 1)
        self.assertEqual(place._next_cycle, 0)

    def test_update_if_timer_is_0(self):
        """Test: change current and next cycles when timer is 0, and update timer expiry."""
        place = Place(**self.data)

        self.assertEqual(place._current_cycle, 0)
        self.assertEqual(place._next_cycle, 1)

        place.timer.expiry = datetime.utcnow() + timedelta(milliseconds=500)

        self.assertEqual(place.timer.total_seconds, 0)
        self.assertEqual(place._current_cycle, 0)
        self.assertEqual(place._next_cycle, 1)

        old_expiry = place.timer.expiry
        place.update()

        self.assertEqual(place._current_cycle, 1)
        self.assertEqual(place._next_cycle, 0)
        self.assertNotEqual(place.timer.expiry, old_expiry)
        self.assertEqual(place.timer.expiry, old_expiry + data.CYCLES['earth'][1].duration)
        self.assertAlmostEqual(place.timer.total_seconds, int(data.CYCLES['earth'][1].duration.total_seconds()),
                               delta=5)

    def test_not_update_if_timer_is_not_0(self):
        """Test: not change current and next cycles when timer isn't 0, and not update timer expiry."""
        place = Place(**self.data)

        self.assertIs(place.timer.expiry, self.expiry)
        self.assertEqual(place._current_cycle, 0)
        self.assertEqual(place._next_cycle, 1)

        place.update()

        self.assertIs(place.timer.expiry, self.expiry)
        self.assertEqual(place._current_cycle, 0)
        self.assertEqual(place._next_cycle, 1)

    def test_get_info(self):
        """Test: get_info return correct info."""
        place = Place(**self.data)
        expected_info = 'Name: name\n' \
                        'Current cycle: Day\n' \
                        'Next cycle: Night\n' \
                        'Left time: [23h 59m]\n'

        self.assertIn(expected_info, place.get_info())


if __name__ == '__main__':
    unittest.main()
