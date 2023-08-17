from datetime import timedelta

from objects import Cycle

CYCLES = {
    'earthCycle': (
        Cycle('day', timedelta(hours=4)),
        Cycle('night', timedelta(hours=4))
    ),
    'cetusCycle': (
        Cycle('day', timedelta(hours=1, minutes=40)),
        Cycle('night', timedelta(minutes=50))
    ),
    'vallisCycle': (
        Cycle('cold', timedelta(minutes=20)),
        Cycle('warm', timedelta(minutes=6, seconds=40))
    ),
    'cambionCycle': (
        Cycle('fass', timedelta(hours=1, minutes=40)),
        Cycle('vome', timedelta(minutes=50))
    ),
    'zarimanCycle': (
        Cycle('grineer', timedelta(hours=2, minutes=30)),
        Cycle('corpus', timedelta(hours=2, minutes=30))
    ),
    # 'duviriCycle': (
    #     Cycle('anger', timedelta(hours=2)),
    #     Cycle('joy', timedelta(hours=2)),
    #     Cycle('envy', timedelta(hours=2)),
    #     Cycle('fear', timedelta(hours=2)),
    #     Cycle('sorrow', timedelta(hours=2)),
    # ),
}

MAIN_URL = 'https://api.warframestat.us/pc/'
CYCLE_URLS = (
    MAIN_URL + 'earthCycle/',
    MAIN_URL + 'cetusCycle/',
    MAIN_URL + 'vallisCycle/',
    MAIN_URL + 'cambionCycle/',
    MAIN_URL + 'zarimanCycle/',
    # MAIN_URL + 'duviriCycle/',
)
TRADERS_URLS = (
    MAIN_URL + 'voidTrader/',
    MAIN_URL + 'steelPath/',
)

PLACES = (
    'Earth',
    'Cetus',
    'Fortune',
    'Cambion Drift',
    'Zariman',
    # 'Duviri',
)

TRADERS = (
    'Baro Ki\'teer',
    'Teshin',
)

RELAY = (
    'Larunda (Mercury)',
    'Strata (Earth)',
    'Kronia (Saturn)',
    'Orcus (Pluto)',
)

LOCATIONS = (
    'Mercury',
    'Venus',
    'Fortune',
    'Earth',
    'Cetus',
    'Mars',
    'Phobos',
    'Deimos',
    'Cambion Drift',
    'Ceres',
    'Jupiter',
    'Europa',
    'Saturn',
    'Uranus',
    'Neptune',
    'Pluto',
    'Sedna',
    'Eris',
    'Void',
    'Lua',
    'Kuva Fortress',
    'Zariman',
    'Earth Proxima',
    'Venus Proxima',
    'Saturn Proxima',
    'Neptune Proxima',
    'Pluto Proxima',
    'Veil Proxima',
)

ENEMIES = (
    'Corpus',
    'Grineer',
    'Orokin',
    'Infested',
    'Crossfire',
)

TYPES = (
    'Assault',
    'Capture',
    'Defense',
    'Disruption',
    'Excavation',
    'Extermination',
    'Interception',
    'Mobile Defense',
    'Rescue',
    'Sabotage',
    'Skirmish',
    'Spy',
    'Survival',
    'Volatile',
    'Orphix',
    'Hive',
)

TIERS = (
    'Lith',
    'Meso',
    'Neo',
    'Axi',
    'Requiem',
)
