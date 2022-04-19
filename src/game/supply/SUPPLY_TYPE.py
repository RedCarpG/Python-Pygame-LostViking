from enum import Enum


class SUPPLY_TYPE(Enum):
    Life = 0
    Level = 1
    Bomb = 2

    @classmethod
    def get_types(cls):
        return [cls.Life, cls.Level, cls.Bomb]
