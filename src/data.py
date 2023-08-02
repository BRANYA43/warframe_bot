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
    'villasCycle': (
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
