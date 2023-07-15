import datetime
import unittest

from warframe_bot.objects.cycle import Cycle


class TestBase(unittest.TestCase):

    def setUp(self) -> None:
        self.expiry = datetime.datetime.utcnow()
        self.cycle = Cycle(name='cycle_name', title='cycle_title', expiry=self.expiry,
                           current_cycle='cycle_1', cycles=['cycle_1', 'cycle_2'])

    def test_create_cycle_with_correct_values(self):
        """Test: create cycle with correct attrs."""
        self.assertEqual(self.cycle.name, 'cycle_name')
        self.assertEqual(self.cycle.title, 'cycle_title')
        self.assertEqual(self.cycle.current_cycle, 'cycle_1')
        self.assertEqual(self.cycle.cycles, ['cycle_1', 'cycle_2'])

    def test_not_create_cycle_with_incorrect_values(self):
        """Test: not create cycle with incorrect attrs"""
        with self.assertRaises((TypeError, ValueError)):
            Cycle(name='cycle_name', title='cycle_title', expiry=self.expiry, current_cycle=None,
                  cycles=['cycle_1', 'cycle_2'])
            Cycle(name='cycle_name', title='cycle_title', expiry=self.expiry, current_cycle='',
                  cycles=['cycle_1', 'cycle_2'])
            Cycle(name='cycle_name', title='cycle_title', expiry=self.expiry, current_cycle='None',
                  cycles=['cycle_1', 'cycle_2'])
            Cycle(name='cycle_name', title='cycle_title', expiry=self.expiry, current_cycle='cycle_1', cycles=[])
            Cycle(name='cycle_name', title='cycle_title', expiry=self.expiry, current_cycle='cycle_1', cycles=[None])
            Cycle(name='cycle_name', title='cycle_title', expiry=self.expiry, current_cycle='cycle_1', cycles=[''])
            Cycle(name='cycle_name', title='cycle_title', expiry=self.expiry, current_cycle='cycle_1',
                  cycles=['cycle_1'])
            Cycle(name='cycle_name', title='cycle_title', expiry=self.expiry, current_cycle='cycle_1',
                  cycles=[None, 'cycle_1'])
            Cycle(name='cycle_name', title='cycle_title', expiry=self.expiry, current_cycle='cycle_1',
                  cycles=['', 'cycle_1'])

    def test_raise_errors_of_current_cycle_property(self):
        """
        Test: raise TypeError if current_cycle isn't str, raise ValueError if current_cycle is empty string, raise
        ValueError if current_cycle isn't in list of cycles.
        """
        with self.assertRaises(TypeError) as e:
            self.cycle.current_cycle = None
        self.assertEqual(str(e.exception), 'Current cycle must be str.')

        with self.assertRaises(ValueError) as e:
            self.cycle.current_cycle = ''
        self.assertEqual(str(e.exception), 'Current cycle cannot be empty string.')

        with self.assertRaises(ValueError) as e:
            self.cycle.current_cycle = 'None'
        self.assertEqual(str(e.exception), 'Current cycle must be in list of cycles.')

    def test_raise_errors_of_cycles_property(self):
        """
        Test: raise TypeError if cycles isn't list, raise ValueError if cycles is empty, raise ValueError if cycles
        has one item, raise ValueError if items of cycles aren't str.
        """
        with self.assertRaises(TypeError) as e:
            self.cycle.cycles = None
        self.assertEqual(str(e.exception), 'Cycles must be list.')

        with self.assertRaises(ValueError) as e:
            self.cycle.cycles = []
            self.cycle.cycles = ['cycle_1']
        self.assertEqual(str(e.exception), 'Cycles cannot have less 2 items.')

        with self.assertRaises(TypeError) as e:
            self.cycle.cycles = [None, None]
            self.cycle.cycles = ['cycle_1', None]
        self.assertEqual(str(e.exception), 'Items of cycles must be str.')

        with self.assertRaises(ValueError) as e:
            self.cycle.cycles = ['', '']
            self.cycle.cycles = ['cycle_1', '']
        self.assertEqual(str(e.exception), 'Items of cycles cannot be empty string.')

    def test_set_next_cycle_when_setting_current_cycle(self):
        """Test: set next_cycle when setting current_cycle."""
        self.assertEqual(self.cycle.next_cycle, 'cycle_2')

    def test_change_next_cycle_when_setting_current_cycle(self):
        """Test: change next_cycle when setting another current_cycle."""
        self.cycle.current_cycle = 'cycle_2'
        self.assertEqual(self.cycle.next_cycle, 'cycle_1')


if __name__ == '__main__':
    unittest.main()
