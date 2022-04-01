from .player_event_handler import detect_player_event, detect_key_pressed
from .PlayerWeapon import (
    PlayerWeapon,
    PlayerWeaponViking,
    PlayerBulletViking
)
from .PlayerPlane import (
    PlayerPlane,
    PlayerViking
)


def load_asset_player():
    from src.helper.image import load_image
    load_image("PlayerPlane/bullet.png")
    # Init sound
    from src.helper.sound import load_sound
    from src.setting import MAIN_VOLUME
    # Player
    load_sound("Player_Shoot.wav", MAIN_VOLUME - 0.2, "PLAYER_SHOOT")
    load_sound("Player_Explo.wav", MAIN_VOLUME, "PLAYER_EXPLODE")
    # Nuc bomb
    load_sound("NuclearLaunch_Detected.wav", MAIN_VOLUME - 0.1, "NUC_LAUNCH")
    load_sound("NuclearMissile_Ready.wav", MAIN_VOLUME - 0.1, "NUC_READY")
    load_sound("Error.wav", MAIN_VOLUME, "NUC_ERROR")
    load_sound("Player_Explo.wav", MAIN_VOLUME, "NUC_EXPLODE")
