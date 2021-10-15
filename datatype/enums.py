from enum import IntEnum

class MatchStatus(IntEnum):
    INVALID = 0
    WAITING = 1
    IN_PROGRESS = 2
    FINISHED = 3