import datetime
import unittest

from objects.timer import Timer
from test_objects.base_test import BaseTest


class TestTimer(BaseTest):
    """Test Timer"""

    @staticmethod
    def get_fake_expiry() -> str:
        expiry = datetime.datetime.utcnow() + datetime.timedelta(days=1, hours=1, seconds=61)
        return expiry.isoformat()

    def test_create_timer_with_correct_values(self):
        """Test: create timer with correct values"""
        timer = Timer(expiry=self.get_fake_expiry())

        self.assertEqual(timer.days, 1)
        self.assertEqual(timer.hours, 1)
        self.assertEqual(timer.minutes, 1)
        self.assertEqual(timer.raw_seconds, Timer.DAY + Timer.HOUR + Timer.MINUTE)

    def test_not_create_timer_with_incorrect_values(self):
        """Test: not create timer with incorrect values"""
        self.assertRaises(TypeError, Timer, None)
        self.assertRaises(ValueError, Timer, '')
        self.assertRaises(ValueError, Timer, 'None')
    def test_raw_second_is_less_after_update(self):
        """Test: raw_second is less after update"""
        timer = Timer(expiry=self.get_fake_expiry())

        self.assertEqual(timer.raw_seconds, Timer.DAY + Timer.HOUR + Timer.MINUTE)

        timer.update()

        self.assertEqual(timer.raw_seconds, Timer.DAY + Timer.HOUR)

    # def setUp(self) -> None:
    #     self.timer = Timer(raw_seconds=Timer.DAY + Timer.HOUR + Timer.MINUTE)
    #
    # def test_create_timer_with_correct_values(self):
    #     """Test: create time with correct values."""
    #     self.assertEqual(self.timer.raw_seconds, Timer.DAY + Timer.HOUR + Timer.MINUTE)
    #     self.assertEqual(self.timer.days, 1)
    #     self.assertEqual(self.timer.hours, 1)
    #     self.assertEqual(self.timer.minutes, 1)
    #
    # def test_not_create_timer_with_incorrect_values(self):
    #     """Test: not create time with incorrect values."""
    #     with self.assertRaises((TypeError, ValueError)):
    #         Timer(raw_seconds=None)
    #         Timer(raw_seconds=-1)
    #
    # def test_raise_errors_raw_seconds_property(self):
    #     """Test: raise TypeError if raw_seconds isn't int, raise ValueError if raw_seconds is negative."""
    #     with self.assertRaises(TypeError) as e:
    #         self.timer.raw_seconds = None
    #     self.check_error_message(e, 'raw_seconds must be int.')
    #
    #     with self.assertRaises(ValueError) as e:
    #         self.timer.raw_seconds = -1
    #     self.check_error_message(e, 'raw_seconds cannot be negative.')
    #
    # def test_days_property(self):
    #     """Test: days property return number"""
    #     self.assertEqual(self.timer.days, 1)
    #
    #     self.timer.raw_seconds = Timer.DAY * 3
    #     self.assertEqual(self.timer.days, 3)
    #
    # def test_hours_property(self):
    #     """Test: hours property return number"""
    #     self.assertEqual(self.timer.hours, 1)
    #
    #     self.timer.raw_seconds = Timer.HOUR * 3
    #     self.assertEqual(self.timer.hours, 3)
    #
    # def test_minutes_property(self):
    #     """Test: minutes property return number"""
    #     self.assertEqual(self.timer.minutes, 1)
    #
    #     self.timer.raw_seconds = Timer.MINUTE * 3
    #     self.assertEqual(self.timer.minutes, 3)
    #
    # def test_get_str_time(self):
    #     """Test get_str_time returns string and correct time."""
    #     raw_seconds_ = [
    #         Timer.DAY + Timer.MINUTE,
    #         Timer.HOUR + Timer.MINUTE,
    #         Timer.DAY + Timer.HOUR,
    #         Timer.DAY,
    #         Timer.HOUR,
    #         Timer.MINUTE,
    #         0,
    #     ]
    #     str_time_ = [
    #         '1d 1m',
    #         '1h 1m',
    #         '1d 1h ',
    #         '1d ',
    #         '1h ',
    #         '1m',
    #         '0m',
    #     ]
    #     self.assertEqual(self.timer.get_str_time(), '1d 1h 1m')
    #     for raw_seconds, str_time in zip(raw_seconds_, str_time_):
    #         self.timer.raw_seconds = raw_seconds
    #         self.assertEqual(self.timer.get_str_time(), str_time)
    #
    # def test_update(self):
    #     """Test: update time. Every call decreases raw_seconds on 60 sec."""
    #     self.assertEqual(self.timer.raw_seconds, Timer.DAY + Timer.HOUR + Timer.MINUTE)
    #
    #     self.timer.update()
    #
    #     self.assertEqual(self.timer.raw_seconds, Timer.DAY + Timer.HOUR)


if __name__ == '__main__':
    unittest.main()
