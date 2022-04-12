import random
from .Supply import Supply
from .SupplyLife import SupplyLife
from .SupplyBomb import SupplyBomb
from .SupplyLevel import SupplyLevel
from .supply_event import supply_event_config, supply_events_handler, add_supply
from .SUPPLY_TYPE import SUPPLY_TYPE


def load_asset_supply():
    from src.helper.sound import load_sound
    from src.setting import MAIN_VOLUME
    load_sound("Supply/Life.wav", MAIN_VOLUME - 0.3, "SUPPLY_LIFE")
    load_sound("Supply/Upgrade.wav", MAIN_VOLUME - 0.3, "SUPPLY_LEVEL")
    load_sound("Supply/NucReady.wav", MAIN_VOLUME - 0.3, "SUPPLY_BOMB")
    from src.helper.image import load_image
    supply_event_config()
    load_image("Supply/SupplyBase.png")
    load_image("Supply/SupplyLife.png")
    load_image("Supply/SupplyBomb.png")
    load_image("Supply/SupplyLevel.png")


def get_random_supply() -> Supply:
    supply_type = random.choice(SUPPLY_TYPE.get_types())
    if supply_type == SUPPLY_TYPE.Bomb:
        return SupplyBomb
    elif supply_type == SUPPLY_TYPE.Level:
        return SupplyLevel
    elif supply_type == SUPPLY_TYPE.Life:
        return SupplyLife
