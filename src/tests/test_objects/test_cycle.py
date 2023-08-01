import unittest
from datetime import timedelta

from objects.mixins import NameMixin
from objects import Cycle


class TestCycle(unittest.TestCase):
    """Test Cycle"""

    def setUp(self) -> None:
        self.data = {
            'name': 'name',
            'duration': timedelta(days=1),
        }

    def test_cycle_inherit_name_mixin(self):
        """Test: cycle inherit NameMixin."""
        self.assertTrue(issubclass(Cycle, NameMixin))

    def test_create_cycle_with_correct_values(self):
        """Test: create Cycle with correct values."""
        cycle = Cycle(**self.data)

        self.assertEqual(cycle.name, self.data['name'])
        self.assertIsInstance(cycle.duration, timedelta)
        self.assertIs(cycle.duration, self.data['duration'])

    def test_not_create_cycle_with_incorrect_duration(self):
        """Test: not create Cycle with incorrect values."""
        del self.data['duration']
        self.assertRaisesRegex(TypeError, r'Expected timedelta, but got (.+).', Cycle, duration=None, **self.data)
        self.assertRaisesRegex(ValueError, r'Duration cannot be less 1 minute.', Cycle, duration=timedelta(seconds=1),
                               **self.data)


if __name__ == '__main__':
    unittest.main()
