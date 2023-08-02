from datetime import datetime

from objects import Timer


class TimerMixin:
    """Timer Mixin"""

    def __init__(self, expiry: datetime):
        self._timer = Timer(expiry)

    @property
    def timer(self) -> Timer:
        return self._timer
