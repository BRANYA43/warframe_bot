from datetime import datetime, timedelta

import data
from objects.mixins import TimerMixin, NameMixin
from validators import validate_type, validate_types, validate_is_not_empty_string, validate_is_not_negative_number


class Item(NameMixin):
    """Item of inventory"""

    def __init__(self, name: str, cost: int):
        super().__init__(name)

        validate_type(cost, int)
        if cost < 0:
            raise ValueError('Cost cannot be less 0.')
        self._cost = cost

    @property
    def cost(self):
        return self._cost

    def get_info(self) -> tuple[str, ...]:
        return (
            f'Name: {self.name}',
            f'Cost: {self.cost}',
        )


class Inventory:
    """Inventory"""

    def __init__(self):
        self._items = []

    @property
    def items(self) -> list[Item]:
        return self._items.copy()

    def add_item(self, item: Item):
        validate_type(item, Item)
        self._items.append(item)

    def add_items(self, items: list[Item, ...]):
        validate_type(items, list)
        if len(items) == 0:
            raise ValueError('Items cannot be empty list.')
        if any(not isinstance(item, Item) for item in items):
            raise TypeError('Each item in items list must be Item.')
        self._items += items

    def get_index_item_by_item_name(self, value: str) -> int | None:
        validate_is_not_empty_string(value)
        for i, item in enumerate(self._items):
            if value == item.name:
                return i

    def clear(self):
        self._items.clear()

    def get_info(self) -> tuple[tuple[str, ...]]:
        return tuple([item.get_info() for item in self.items])


class Trader(NameMixin, TimerMixin):
    """Trader"""

    def __init__(self, name: str, expiry: datetime):
        NameMixin.__init__(self, name)
        TimerMixin.__init__(self, expiry)
        self._inventory = Inventory()

    @property
    def inventory(self) -> Inventory:
        return self._inventory

    def get_info(self) -> tuple[str, ...]:
        return (
            f'Name: {self.name}',
            f'Left time: {self.timer.get_str_time()}',
        )


class VoidTrader(Trader):
    """Void Trader"""

    TIME_TO_ARRIVING = timedelta(weeks=2)
    TIME_TO_DEPARTING = timedelta(days=2)

    def __init__(self, expiry: datetime, relay: str, *, active: bool = False):
        super().__init__(name=data.TRADERS[0], expiry=expiry)
        self.relay = relay
        self.active = active

    @property
    def relay(self) -> str:
        return self._relay

    @relay.setter
    def relay(self, value: str):
        validate_is_not_empty_string(value)
        if value not in data.RELAY and 'TennoCon' not in value:
            raise ValueError('No such a relay name in data.')
        self._relay = value

    @property
    def active(self) -> bool:
        return self._active

    @active.setter
    def active(self, value: bool):
        validate_type(value, bool)
        self._active = value

    def get_info(self):
        name, left_time = super().get_info()
        if self.active:
            ret = (name, f'Relay: {self.relay}', left_time)
        else:
            ret = (name, 'Location: Void', left_time)
        return ret

    def update(self):
        if self.timer.total_seconds <= 0:
            if self.active:
                self.timer.expiry += self.TIME_TO_ARRIVING
                self.inventory.clear()
            else:
                self.timer.expiry += self.TIME_TO_DEPARTING
            self.active = not self.active


class SteelTrader(Trader):
    """SteelTrader"""

    TIME_TO_CHANGING_OFFER = timedelta(weeks=1)

    def __init__(self, expiry: datetime, offers: list[Item, ...], current_offer: str):
        super().__init__(name=data.TRADERS[1], expiry=expiry)
        self.inventory.add_items(offers)
        self._set_current_offer_by_name(current_offer)

    @property
    def offers(self) -> list[Item, ...]:
        return self.inventory.items

    @property
    def current_offer(self) -> Item:
        return self.inventory.items[self._current_offer]

    def _set_current_offer_by_name(self, value):
        if (offer := self.inventory.get_index_item_by_item_name(value)) is None:
            raise ValueError('No such a offer in offers.')
        self._current_offer = offer
        self._set_next_offer()

    def _set_next_current_offers(self):
        items = self.inventory.items
        index = (self._current_offer + 1) % len(items)
        self._current_offer = index
        self._set_next_offer()

    @property
    def next_offer(self) -> Item:
        return self.inventory.items[self._next_offer]

    def _set_next_offer(self):
        items = self.inventory.items
        index = (self._current_offer + 1) % len(items)
        self._next_offer = index

    def update(self):
        if self.timer.total_seconds == 0:
            self._set_next_current_offers()
            self.timer.expiry += self.TIME_TO_CHANGING_OFFER

    def get_info(self) -> tuple[str, ...]:
        return (
            f'Name: {self.name}',
            f'Current offer: {self.current_offer.name}',
            f'Next offer: {self.next_offer.name}',
            f'Left time: {self.timer.get_str_time()}',
        )
