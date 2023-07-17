import requests

from objects.cycle import Cycle


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

    def create_cycle(self, key: str, name: str, cycles: list[str]) -> Cycle:
        """Create Cycle"""
        response = self._response[key]
        cycle = Cycle(
            name=name,
            left_time=response['timeLeft'],
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
        cycle.left_time = response['timeLeft']

    def get_cycles_info(self) -> str:
        """Get cycles info"""
        ret = ''
        for cycle in self._cycles.values():
            ret += cycle.get_info() + '\n'
        return ret
