def init_player():
    # Init Player Plane
    from .PlayerPlane import Player1
    Player1.init()
    from .PlayerWeapon import PlayerBullet1
    PlayerBullet1.init()
    from .PlayerBomb import PlayerNucBomb, NucExplosion
    PlayerNucBomb.init()
    NucExplosion.init()

    # Init sound
    from ..generic_loader.sound_loader import load_sound
    from ..constants import MAIN_VOLUME
    # Player
    load_sound("Player_Shoot.wav", MAIN_VOLUME - 0.2, "PLAYER_SHOOT")
    load_sound("Player_Explo.wav", MAIN_VOLUME, "PLAYER_EXPLODE")
    # Nuc bomb
    load_sound("NuclearLaunch_Detected.wav", MAIN_VOLUME - 0.1, "NUC_LAUNCH")
    load_sound("NuclearMissile_Ready.wav", MAIN_VOLUME - 0.1, "NUC_READY")
    load_sound("Error.wav", MAIN_VOLUME, "NUC_ERROR")
    load_sound("Player_Explo.wav", MAIN_VOLUME, "NUC_EXPLODE")
