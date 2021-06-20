def init_player():
    # Init Player Plane
    from .PlayerPlane import Player1
    Player1.init()
    from .PlayerWeapon import PlayerBullet1
    PlayerBullet1.init()
    from .PlayerBomb import PlayerNucBomb, NucExplosion
    PlayerNucBomb.init()
    NucExplosion.init()
