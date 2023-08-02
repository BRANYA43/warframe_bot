import unittest
from datetime import datetime, timedelta

from objects import Timer
from objects.mixins import TimerMixin


class TestTimerMixin(unittest.TestCase):
    """Test TimerMixin"""

    def setUp(self) -> None:
        self.time_delta = timedelta(days=1)
        self.expiry = datetime.utcnow() + self.time_delta

    def test_create_name_mixin_with_correct_expiry(self):
        """Test: create TimerMixin with correct name."""
        timer_mixin = TimerMixin(self.expiry)

        self.assertIsInstance(timer_mixin.timer, Timer)
        self.assertIs(timer_mixin.timer.expiry, self.expiry)

    def test_not_create_name_timer_with_incorrect_expiry(self):
        """Test: not create TimerMixin with incorrect name."""
        past_datetime = datetime.utcnow() - self.time_delta

        self.assertRaisesRegex(TypeError, r'Expected datetime, but got (.+).', TimerMixin, None)
        self.assertRaisesRegex(ValueError, r'Expiry cannot be past datetime.', TimerMixin, past_datetime)


if __name__ == '__main__':
    unittest.main()
