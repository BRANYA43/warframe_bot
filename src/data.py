from datetime import timedelta

from objects import Cycle

CYCLES = {
    'earth': (
        Cycle('day', timedelta(hours=4)),
        Cycle('night', timedelta(hours=4))
    ),
    'cetus': (
        Cycle('day', timedelta(hours=1, minutes=40)),
        Cycle('night', timedelta(minutes=50))
    ),
    'fortune': (
            Cycle('cold', timedelta(minutes=20)),
            Cycle('warm', timedelta(minutes=6, seconds=40))
        ),
    'cambion': (
            Cycle('fass', timedelta(hours=1, minutes=40)),
            Cycle('vome', timedelta(minutes=50))
        ),
    'zariman': (
            Cycle('grineer', timedelta(hours=2, minutes=30)),
            Cycle('corpus', timedelta(hours=2, minutes=30))
        ),
    'duviri': (
        Cycle('anger', timedelta(hours=2)),
        Cycle('joy', timedelta(hours=2)),
        Cycle('envy', timedelta(hours=2)),
        Cycle('fear', timedelta(hours=2)),
        Cycle('sorrow', timedelta(hours=2)),
    ),
}