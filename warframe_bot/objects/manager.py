import datetime

import requests

from objects.cycle import Cycle
from objects.fissure import Fissure
from objects.mission import Mission
from objects.timer import Timer
from translater import get_text as _


class Manager:
    """Manager"""

    def __init__(self):
        self.is_ready = False
        self._url = 'https://api.warframestat.us/pc/'
        self._response = None
        self._cycles = {}
        self._fissures = {}
        self._fissures_for_delete = []
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
        self.set_response()

        cycle_names = ['Earth', 'Cetus', 'Fortune', 'Cambion Drift', 'Zariman']
        cycle_cycles = [
            ['day', 'night'],
            ['day', 'night'],
            ['cold', 'warm'],
            ['vome', 'fass'],
            ['corpus', 'grineer'],
        ]
        for cycle_key, cycle_name, cycles in zip(self._cycle_keys, cycle_names, cycle_cycles):
            self.create_cycle(cycle_key, cycle_name, cycles)

        for fissure_response in self._response['fissures']:
            self.create_fissure(fissure_response)

        self.is_ready = True

    def update_fissures(self):
        """Update all fissures and create new fissures"""
        for fissure_id in self._fissures.keys():
            self.update_fissure(fissure_id)

        for fissure_id in self._fissures_for_delete:
            self.delete_fissure(fissure_id)

        for fissure_response in self._response['fissures']:
            if not fissure_response['id'] in self._fissures.keys():
                fissure = self.create_fissure(fissure_response)

    def update(self):
        """Update values of manager attributes."""
        self.set_response()

        for cycle_key in self._cycle_keys:
            self.update_cycle(cycle_key)

        self.update_fissures()

    def get_timer(self, expiry: str) -> Timer:
        time = datetime.datetime.fromisoformat(expiry.replace('Z', ''))
        now = datetime.datetime.utcnow()
        if now < time:
            delta = time - now
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
        name, location = node.split(' (', maxsplit=1)
        location = location[:-1]
        if is_storm:
            location += ' Proxima'

        mission = Mission(name=name, location=location, type=type, enemy=enemy, is_storm=is_storm, is_hard=is_hard)
        return mission

    def create_fissure(self, fissure_response: dict):
        """Create Fissure"""
        mission = self.create_mission(
            node=fissure_response['node'],
            type=fissure_response['missionType'],
            enemy=fissure_response['enemy'],
            is_storm=fissure_response['isStorm'],
            is_hard=fissure_response['isHard'],
        )
        timer = self.get_timer(fissure_response['expiry'])
        fissure = Fissure(
            id=fissure_response['id'],
            mission=mission,
            tier=fissure_response['tier'],
            timer=timer,
        )
        self._fissures.setdefault(fissure.id, fissure)
        return fissure

    def delete_fissure(self, id: str):
        """Delete Fissure from fissures"""
        del self._fissures[id]
        self._fissures_for_delete.remove(id)

    def update_fissure(self, id: str):
        """Update fissure timer"""
        fissure = self._fissures[id]
        fissure.timer.update()
        if fissure.timer.raw_seconds == 0:
            ids = [fissure_['id'] for fissure_ in self._response['fissures']]
            if not fissure.id in ids and not fissure.id in self._fissures_for_delete:
                self._fissures_for_delete.append(fissure.id)

    def get_fissures_info(self) -> str:
        simple = _('Missions of Simple\n')
        storm = _('Missions of Railjack\n')
        hard = _('Missions of Steel Path\n')

        for fissure in self._fissures.values():
            if not fissure.mission.is_storm and not fissure.mission.is_hard:
                simple += fissure.get_info() + '\n'

            if fissure.mission.is_storm:
                storm += fissure.get_info() + '\n'

            if fissure.mission.is_hard:
                hard += fissure.get_info() + '\n'

        return simple + storm + hard
