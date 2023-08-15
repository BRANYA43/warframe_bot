from datetime import datetime

import requests

import data
from objects import Place, VoidTrader, Item, SteelTrader


class Manager:
    """Manager"""

    SEC_FOR_REDUCE = 60

    def __init__(self):
        self._is_ready = False
        self._places = {}
        self._void_trader = None
        self._steel_trader = None

    @property
    def void_trader(self):
        return self._void_trader.copy()

    @property
    def steel_trader(self):
        return self._steel_trader.copy()

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

    @staticmethod
    def get_item_list(items_data: list[dict]) -> list[Item, ...]:
        return [Item(**data_) for data_ in items_data]

    def prepare(self):
        self.prepare_places()
        self.prepare_void_trader()
        self.prepare_steel_trader()
        self._is_ready = True

    def update(self):
        self.update_places()
        self.update_void_trader()
        self.update_steel_trader()

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
        return [place.get_info() for place in self._places.values()]

    def create_void_trader(self, response: dict) -> VoidTrader:
        void_trader = VoidTrader(
            expiry=self.format_expiry(response['expiry']),
            relay=response['location'].replace(' Relay', ''),
            active=response['active'],
        )

        if void_trader.active:
            void_trader.inventory.add_items(self.get_item_list(response['inventory']))

        self._void_trader = void_trader
        return void_trader

    def prepare_void_trader(self):
        response = self.get_response(data.TRADERS_URLS[0])
        self.create_void_trader(response)

    def update_void_trader(self):
        self._void_trader.timer.reduce(self.SEC_FOR_REDUCE)
        self._void_trader.update()
        if self._void_trader.active and not self._void_trader.inventory.items:
            response = self.get_response(data.TRADERS_URLS[0])
            if inventory := response['inventory']:
                items = self.get_item_list(inventory)
                self._void_trader.inventory.add_items(items)

    def create_steel_trader(self, response: dict) -> SteelTrader:
        steel_trader = SteelTrader(
            expiry=self.format_expiry(response['expiry']),
            offers=self.get_item_list(response['rotation']),
            current_offer=response['currentReward']['name'],
        )
        self._steel_trader = steel_trader

        return steel_trader

    def prepare_steel_trader(self):
        response = self.get_response(data.TRADERS_URLS[1])
        self.create_steel_trader(response)

    def update_steel_trader(self):
        self._steel_trader.timer.reduce(self.SEC_FOR_REDUCE)
        self._steel_trader.update()
