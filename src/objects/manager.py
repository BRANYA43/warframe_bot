from copy import copy
from datetime import datetime
from pprint import pprint

import requests

import data
from objects import Place, VoidTrader, Item, SteelTrader, Fissure, FissureStorage
from validators import validate_type


class Manager:
    """Manager"""

    SEC_FOR_REDUCE = 60

    def __init__(self):
        self._is_ready = False
        self._is_delete_fissures = False
        self._places = {}
        self._void_trader = None
        self._steel_trader = None
        self._fissure_storage = FissureStorage()

    @property
    def is_delete_fissures(self) -> bool:
        return self._is_delete_fissures

    @is_delete_fissures.setter
    def is_delete_fissures(self, value: bool):
        validate_type(value, bool)
        self._is_delete_fissures = value

    @property
    def void_trader(self):
        return copy(self._void_trader)

    @property
    def steel_trader(self):
        return copy(self._steel_trader)

    @property
    def fissure_storage(self) -> FissureStorage:
        return self._fissure_storage

    @property
    def is_ready(self) -> bool:
        return self._is_ready

    @staticmethod
    def format_expiry(value: str) -> datetime:
        expiry = datetime.fromisoformat(value.replace('Z', ''))
        return expiry

    @staticmethod
    def get_response(url: str):
        return requests.get(url, headers={'content-language': 'en'}).json()

    @staticmethod
    def get_item_list(items_data: list[dict]) -> list[Item, ...]:
        if items_data[0].get('name') is not None and items_data[0].get('cost') is not None:
            return [Item(**data_) for data_ in items_data]
        return [Item(data_['item'], data_['ducats']) for data_ in items_data]

    def prepare(self):
        self.prepare_places()
        self.prepare_void_trader()
        self.prepare_steel_trader()
        self.prepare_fissures()
        self._is_ready = True

    def update(self):
        self.update_places()
        self.update_void_trader()
        self.update_steel_trader()
        self.update_fissures()

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
        for url, key, name in zip(data.CYCLE_URLS, data.CYCLES.keys(), data.PLACES):
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

    def create_fissure(self, response: dict) -> Fissure:
        name, location = response['node'].split(' (')
        location = location[:-1]

        if response['isStorm']:
            location += ' Proxima'

        fissure = Fissure(
            id=response['id'],
            name=name,
            location=location,
            type=response['missionType'],
            enemy=response['enemy'],
            tier=response['tier'],
            expiry=self.format_expiry(response['expiry']),
            is_storm=response['isStorm'],
            is_hard=response['isHard'],
        )

        self._fissure_storage.add(fissure)

        return fissure

    def prepare_fissures(self):
        response = self.get_response(data.FISSURES_URL)

        for fissure_response in response:
            if fissure_response['active'] \
                    and datetime.fromisoformat(fissure_response['expiry'].replace('Z', '')) > datetime.utcnow():
                self.create_fissure(fissure_response)

    def update_fissures(self):
        fissures = self._fissure_storage.get_all_fissure_list()
        for fissure in fissures:
            fissure.timer.reduce(self.SEC_FOR_REDUCE)
            fissure.update()

            if not fissure.active:
                self._fissure_storage.delete_fissure(fissure)
                if not self._is_delete_fissures:
                    self._is_delete_fissures = True

    def get_fissures_info(self, type: str):
        fissures_by_tier = self.fissure_storage.get_fissures(type)
        if type == 'kuva':
            return [fissure.get_info() for fissure in fissures_by_tier]
        return [[fissure.get_info() for fissure in fissures] for fissures in fissures_by_tier.values()]

    def add_new_fissures(self):
        response = self.get_response(data.FISSURES_URL)
        existed_ids = self._fissure_storage.get_all_ids()
        for fissure_response in response:
            if fissure_response['id'] not in existed_ids \
                    and fissure_response['active'] \
                    and self.format_expiry(fissure_response['expiry']) > datetime.utcnow():
                self.create_fissure(fissure_response)
