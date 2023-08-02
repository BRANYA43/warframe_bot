from datetime import datetime

from validators import validate_type


class Timer:
    """Timer"""

    def __init__(self, expiry: datetime):
        self._total_seconds = None
        self.expiry = expiry

    @property
    def expiry(self) -> datetime:
        return self._expiry

    @expiry.setter
    def expiry(self, value: datetime):
        validate_type(value, datetime)
        if value < datetime.now():
            raise ValueError('Expiry cannot be past datetime.')
        self._expiry = value
        self._set_total_seconds()

    @property
    def total_seconds(self) -> int:
        return self._total_seconds

    def _set_total_seconds(self):
        time_delta = self.expiry - datetime.now()
        self._total_seconds = int(time_delta.total_seconds())

    def reduce(self, sec: int):
        if self._total_seconds == 0:
            return
        self._total_seconds -= sec
        if self._total_seconds < 0:
            self._total_seconds = 0

    DAY = 86400
    HOUR = 3600
    MINUTE = 60

    def get_str_time(self):
        time = ''
        if (days := self._total_seconds // self.DAY) != 0:
            time = f'{days}d'
            remainder = self._total_seconds % self.DAY
        else:
            remainder = self._total_seconds

        if (hours := remainder // self.HOUR) != 0:
            if time == '':
                time = f'{hours}h'
            else:
                time += f' {hours}h'

            remainder %= self.HOUR

        if (minutes := remainder // self.MINUTE) != 0:
            if time == '':
                time = f'{minutes}m'
            else:
                time += f' {minutes}m'

        if time == '':
            time = '0m'

        return f'[{time}]'

