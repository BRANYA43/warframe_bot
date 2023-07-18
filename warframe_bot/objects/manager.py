import datetime

import requests

from objects.cycle import Cycle
from objects.mission import Mission
from objects.timer import Timer


class Manager:
    """Manager"""

    def __init__(self):
        self.is_ready = False
        self._url = 'https://api.warframestat.us/pc/'
        self._response = None
        self._cycles = {}
        self._cycle_keys = (
            'earthCycle',
            'cetusCycle',
            'vallisCycle',
            'cambionCycle',
            'zarimanCycle',
        )

    def set_response(self):
        """Set response by url"""
        self._response = requests.get(self._url).json()

    def prepare(self):
        """Prepare manager for start work."""
        cycle_names = ['Earth', 'Cetus', 'Fortune', 'Cambion Drift', 'Zariman']
        cycle_cycles = [
            ['day', 'night'],
            ['day', 'night'],
            ['cold', 'warm'],
            ['vome', 'fass'],
            ['corpus', 'grineer'],
        ]
        self.set_response()
        for cycle_key, cycle_name, cycles in zip(self._cycle_keys, cycle_names, cycle_cycles):
            self.create_cycle(cycle_key, cycle_name, cycles)

        self.is_ready = True

    def update(self):
        """Update values of manager attributes."""
        self.set_response()

        for cycle_key in self._cycle_keys:
            self.update_cycle(cycle_key)

    def get_timer(self, expiry: str) -> Timer:
        time = datetime.datetime.fromisoformat(expiry.replace('Z', ''))
        now = datetime.datetime.utcnow()
        if now < time:
            delta = time - datetime.datetime.utcnow()
            raw_seconds = int(delta.total_seconds())
        else:
            raw_seconds = 0
        return Timer(raw_seconds)

    def create_cycle(self, key: str, name: str, cycles: list[str]) -> Cycle:
        """Create Cycle"""
        response = self._response[key]
        cycle = Cycle(
            name=name,
            timer=self.get_timer(response['expiry']),
            cycles=cycles,
            current_cycle=response['state'],
        )
        self._cycles.setdefault(key, cycle)
        return cycle

    def update_cycle(self, key: str):
        """Update Cycle attributes."""
        response = self._response[key]
        cycle = self._cycles[key]
        cycle.current_cycle = response['state']
        cycle.timer.update()
        if cycle.timer.raw_seconds == 0:
            cycle.timer = self.get_timer(response['expiry'])

    def get_cycles_info(self) -> str:
        """Get cycles info"""
        ret = ''
        for cycle in self._cycles.values():
            ret += cycle.get_info() + '\n'
        return ret

    def create_mission(self, node: str, type: str, enemy: str, is_storm: bool, is_hard: bool):
        """Create Mission"""
        name, location = node.split()
        location = location[1:-1]
        if is_storm:
            location += ' Proxima'

        mission = Mission(name=name, location=location, type_=type, enemy=enemy, is_hard=is_hard)
        return mission
