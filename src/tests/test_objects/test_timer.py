import unittest
from datetime import datetime, timedelta
from objects import Timer


class TestTimer(unittest.TestCase):
    """Test Timer"""

    def setUp(self) -> None:
        self.time_delta = timedelta(days=1)
        self.expiry = datetime.utcnow() + self.time_delta

    def test_create_timer_with_correct_values(self):
        """Test: create timer with correct values."""
        timer = Timer(self.expiry)

        self.assertIsInstance(timer.expiry, datetime)
        self.assertIs(timer.expiry, self.expiry)
        self.assertIsInstance(timer.total_seconds, int)
        self.assertAlmostEqual(timer.total_seconds, int(self.time_delta.total_seconds()), delta=5)

    def test_not_create_timer_with_incorrect_expiry(self):
        """Test: not create timer with incorrect expiry."""
        past_datetime = datetime.utcnow() - self.time_delta

        self.assertRaisesRegex(TypeError, r'Expected datetime, but got (.+).', Timer, None)
        self.assertRaisesRegex(ValueError, r'Expiry cannot be past datetime.', Timer, past_datetime)

    def test_set_new_expiry_and_change_total_seconds(self):
        """Test: set new expiry and change total seconds."""
        timer = Timer(self.expiry)

        self.assertIs(timer.expiry, self.expiry)
        self.assertAlmostEqual(timer.total_seconds, int(self.time_delta.total_seconds()), delta=5)

        time_delta = timedelta(days=10)
        timer.expiry = datetime.utcnow() + time_delta

        self.assertIsInstance(timer.expiry, datetime)
        self.assertAlmostEqual(timer.total_seconds, int(time_delta.total_seconds()), delta=5)

    def test_set_now_expiry_and_total_seconds_set_0(self):
        timer = Timer(self.expiry)

        self.assertIs(timer.expiry, self.expiry)
        self.assertAlmostEqual(timer.total_seconds, int(self.time_delta.total_seconds()), delta=5)

        timer.expiry = datetime.utcnow() + timedelta(milliseconds=500)

        self.assertIsInstance(timer.expiry, datetime)
        self.assertAlmostEqual(timer.total_seconds, 0, delta=5)

    def test_not_set_new_expiry_if_value_is_incorrect(self):
        """Test: not set new expiry if value is incorrect."""
        timer = Timer(self.expiry)

        with self.assertRaisesRegex(TypeError, r'Expected datetime, but got (.+).'):
            timer.expiry = None

        past_datetime = datetime.utcnow() - self.time_delta

        with self.assertRaisesRegex(ValueError, r'Expiry cannot be past datetime.'):
            timer.expiry = past_datetime

    def test_reduce(self):
        """Test: after reduce, total_seconds will be less."""
        timer = Timer(self.expiry)

        self.assertAlmostEqual(timer.total_seconds, int(self.time_delta.total_seconds()), delta=5)

        seconds = 60
        timer.reduce(seconds)

        self.assertLess(timer.total_seconds, int(self.time_delta.total_seconds()))
        self.assertAlmostEqual(timer.total_seconds, int(self.time_delta.total_seconds() - seconds), delta=5)

    def test_if_total_seconds_equal_0_reduce_dont_change_total_seconds(self):
        """Test: if total_seconds = 0, reduce don't change total_seconds."""
        timer = Timer(self.expiry)
        timer.expiry = datetime.utcnow() + timedelta(milliseconds=500)

        self.assertEqual(timer.total_seconds, 0)

        seconds = 60
        timer.reduce(seconds)

        self.assertEqual(timer.total_seconds, 0)

    def test_get_str_time(self):
        """Test: get_str_time returns correct time."""
        now = datetime.utcnow()
        timer = Timer(self.expiry)
        correct_times = (
            '[1d 1h 1m]',
            '[1d 1h]',
            '[1h 1m]',
            '[1d 1m]',
            '[1d]',
            '[1h]',
            '[1m]',
            '[0m]',
        )
        time_deltas = (
            timedelta(days=1, hours=1, minutes=1, seconds=1),
            timedelta(days=1, hours=1, seconds=1),
            timedelta(hours=1, minutes=1, seconds=1),
            timedelta(days=1, minutes=1, seconds=1),
            timedelta(days=1, seconds=1),
            timedelta(hours=1, seconds=1),
            timedelta(minutes=1, seconds=1),
            timedelta(seconds=1),
        )
        for time_delta, correct_time in zip(time_deltas, correct_times):
            timer.expiry = datetime.utcnow() + time_delta
            self.assertEqual(timer.get_str_time(), correct_time)


if __name__ == '__main__':
    unittest.main()
