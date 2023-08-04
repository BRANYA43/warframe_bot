from datetime import datetime

import requests

import data
from objects import Cycle, Place


class Manager:
    """Manager"""

    SEC_FOR_REDUCE = 60

    def __init__(self):
        self._is_ready = False
        self._places = {}

    @property
    def is_ready(self) -> bool:
        return self._is_ready

    @staticmethod
    def format_expiry(value: str) -> datetime:
        expiry = datetime.fromisoformat(value.replace('Z', ''))
        return expiry

    @staticmethod
    def get_response(url: str):
        return requests.get(url).json()

    def prepare(self):
        self.prepare_places()
        self._is_ready = True

    def update(self):
        self.update_places()

    def create_place(self, response: dict, name: str, key: str) -> Place:
        place = Place(
            name=name,
            expiry=self.format_expiry(response['expiry']),
            cycles=data.CYCLES[key],
            current_cycle=response['state'],
        )
        self._places[key] = place
        return place

    def prepare_places(self):
        for url, key, name in zip(data.CYCLE_URLS, data.CYCLES.keys(), data.CYCLE_NAMES):
            response = self.get_response(url)
            self.create_place(response, name, key)

    def update_places(self):
        for place in self._places.values():
            place.timer.reduce(self.SEC_FOR_REDUCE)
            place.update()

    def get_info_places(self):
        ret = ''
        for place in self._places.values():
            ret += place.get_info() + '\n'
        return ret