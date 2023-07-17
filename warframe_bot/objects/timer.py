from validators.validators import *


class Timer:
    """Timer"""

    DAY = 86400
    HOUR = 3600
    MINUTE = 60

    def __init__(self, raw_seconds: int):
        self.raw_seconds = raw_seconds

    @property
    def raw_seconds(self) -> int:
        return self._raw_seconds

    @raw_seconds.setter
    def raw_seconds(self, value: int):
        validate_type(value, int, 'raw_seconds')
        validate_not_negative(value, 'raw_seconds')
        self._raw_seconds = value

    @property
    def days(self) -> int:
        return self._raw_seconds // self.DAY

    @property
    def hours(self) -> int:
        return self._raw_seconds % self.DAY // self.HOUR

    @property
    def minutes(self) -> int:
        return self._raw_seconds % self.DAY % self.HOUR // self.MINUTE

    def get_str_time(self) -> str:
        ret = ''
        days = self.days
        hours = self.hours
        minutes = self.minutes

        if days:
            ret += f'{self.days}d '
        if hours:
            ret += f'{self.hours}h '
        if minutes:
            ret += f'{self.minutes}m'
        if ret == '':
            ret = '0m'
        return ret

    def update(self):
        """Decreases raw_seconds on 60 sec."""
        if not self._raw_seconds:
            return

        self._raw_seconds -= 60

        if self._raw_seconds < 0:
            self._raw_seconds = 0
