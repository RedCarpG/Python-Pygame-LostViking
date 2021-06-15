""" Player controllable object
Includes:
    -> PlayerPlane
"""
from abc import abstractmethod, ABC
import pygame

from ..generic_items.SoundHelper import SoundHelper
from ..generic_items.ImageHelper import LoopImageHelper
from ..generic_items.MovementHelper import InertialMoveHelper
from .PlayerBullet import PlayerBullet1
from ..constants import SCREEN
from ..groups import Player1_G, Player2_G


class BasicPlayerPlane(SoundHelper, LoopImageHelper, InertialMoveHelper, pygame.sprite.Sprite, ABC):
    """ Basic Player Abstract class with behavior defined below:
     -> movement (from StaticMoveHelper)
     -> acceleration (from InertialMoveHelper)
     -> shoot
     -> damaged
     To implement this Class:
        -> set _init_image() (from LoopImageHelper)
        -> set _init_speed() (from StaticMoveHelper)
        -> set _init_acc() (from InertialMoveHelper)
        -> set init() for globally initialize every properties
        -> (optional) set self.start_position (from StaticMoveHelper)
     """

    def __init__(self, point=None):
        # Init
        if not hasattr(self, "_INIT_FLAG") or not self._INIT_FLAG:
            raise Exception("!!!ERROR: class is not init! {}".format(self))
        if not self._MAX_HEALTH:
            raise Exception("!!!ERROR: _MAX_HEALTH value is not set! {}".format(self))
        SoundHelper.__init__(self)
        LoopImageHelper.__init__(self)
        InertialMoveHelper.__init__(self)
        pygame.sprite.Sprite.__init__(self)

        # Set bullet type
        ''' Init Weapon '''
        self.start_position = (int(pygame.display.get_surface().get_width() // 2),
                               int(pygame.display.get_surface().get_height() - self.rect.height // 2 - 30))

        self._set_image_type("MoveNormal")

        ''' Init States '''
        self.is_active = True
        self.is_invincible = False
        # self.invincible_reset = 0
        # self.crash_animation = 0

        ''' Init Weapon '''
        self._bullet_type = PlayerBullet1
        self._lever = 1

        self._attack_speed = 500

        self._health = self._MAX_HEALTH

        # Set init position
        self.set_pos(point)

    """ --------------------- Player Plane Behavior --------------------- """

    def _damaged(self, damage) -> bool:
        if self._health > 0:
            self._health -= damage
            return False
        else:
            self._health = 0
            return True

    def _shoot(self):
        self._bullet_type.shoot_bullets(self.rect.center, self._lever)

    """ ------------------ Real-time methods ------------------ """

    def update(self) -> None:
        """
        Overwrites update from Sprite,
        This method is called in every frame
        """
        # If alive
        if self.is_active:
            # When _speed_x/_speed_y is not 0
            if self._speed_y != 0 or self._speed_x != 0:
                # Move this object
                # (Note: this is the only place when the object is really moving)
                self._move()
                # Speed down if there's no movement command on X or Y
                # (Note: Only values of _speed_x/_speed_y will be changed here)
                self._inertial_deceleration()
                # Restrict the plane inside the screen
                if self.rect.bottom > SCREEN.get_h():
                    self.rect.bottom = SCREEN.get_h()
                if self.rect.left < 0:
                    self.rect.left = 0
                if self.rect.right > SCREEN.get_w():
                    self.rect.right = SCREEN.get_w()
                if self.rect.top < 0:
                    self.rect.top = 0
            self._switch_image()
        else:
            finished = self._switch_image()
            if finished:
                self.reset()

    """ ------------------ Collision detect ------------------ """

    def hit(self, damage=100) -> bool:
        """
        This function is called in collision detection
        """
        if not self.is_invincible:
            if self._damaged(damage):
                self.is_active = False
                self._image_switch = 0
                self._set_image_type("Explode")
                self._SOUND["Player_Explo"].play()
            return True
        else:
            return False

    """
    def invincible(self, ticks, rate=60):
        if self.is_invincible:
            if self.current_time < ticks + rate:
                self.invincible_reset = (self.invincible_reset + 1) % 50
                if self.invincible_reset == 49:
                    self.is_invincible = False
    """
    """ ------------------ Trigger-Action-Commands ------------------"""

    def attack(self) -> None:
        """
        This method is called from a user attack event
        """
        if self.is_active:
            self._SOUND["Player_Shoot"].stop()
            self._SOUND["Player_Shoot"].play()
            self._shoot()

    """ ------------------ Trigger-Movement-Commands ------------------"""
    """ ------------------ (Instant trigger method called by events) --"""

    # Trigger Move Up
    def trigger_move_up(self) -> None:
        """ Trigger this object to move Up (with acceleration)
        Called by event (e.g. Button press)
        """
        # If it was not moving before, change image
        if not self._move_flag_y:
            self._set_image_type("MoveUp")
        # If not outside the screen
        if self.rect.top > 0:
            self._accelerate_up()
        else:
            self._speed_y = 0
            self.rect.top = 0
            self._set_image_type("MoveNormal")

    # Trigger Move Down
    def trigger_move_back(self) -> None:
        """ Trigger this object to move Down (with acceleration)
        Called by event (e.g. Button press)
        (Note: This method only change the value of _speed_x / _speed_y)
        """
        # If it was not moving before, change image
        if not self._move_flag_y:
            self._set_image_type("MoveDown")
        # If not outside the screen
        if self.rect.bottom < SCREEN.get_h():
            self._accelerate_down()
        else:
            self._speed_y = 0
            self.rect.bottom = SCREEN.get_h()
            self._set_image_type("MoveNormal")

    # Trigger Move Left
    def trigger_move_left(self) -> None:
        """ Trigger this object to move Left (with acceleration)
        Called by event (e.g. Button press)
        (Note: This method only change the value of _speed_x / _speed_y)
        """
        # If not outside the screen
        if self.rect.left > 0:
            self._accelerate_left()
        else:
            self._speed_x = 0
            self.rect.left = 0

    # Trigger Move Right
    def trigger_move_right(self) -> None:
        """ Trigger this object to move Right (with acceleration)
        Called by event (e.g. Button press)
        (Note: This method only change the value of _speed_x / _speed_y)
        """
        # If not outside the screen
        if self.rect.right < SCREEN.get_w():
            self._accelerate_right()
        else:
            self._speed_x = 0
            self.rect.right = SCREEN.get_w()

    # Trigger Brake y, only triggered when lease the button
    def trigger_stop_y(self) -> None:
        """ Trigger this object to stop in y axis (with acceleration)
        Triggered by event (e.g. Button release)
        (Note: This only sets the flag, the deceleration will be done
        by _inertial_deceleration automatically in update)
        """
        self._move_flag_y = False

    # Trigger Brake x
    def trigger_stop_x(self) -> None:
        """ Trigger this object to stop in x axis (with acceleration)
        Triggered by event (e.g. Button release)
        (Note: This only sets the flag, the deceleration will be done
        by _inertial_deceleration automatically in update)
        """
        self._move_flag_x = False

    """ ------------------ Interface-----------------"""

    # Bullet Type
    def change_bullet_type(self, bul_class) -> None:
        from LostViking.src.generic_items.BasicBullet import BasicBullet
        if not issubclass(bul_class, BasicBullet):
            raise Exception("ERROR: Bullet type {} is not supported".format(bul_class))
        if self._bullet_type != bul_class:
            self._bullet_type = bul_class
            self._lever = 1

    def get_bullet_type(self):
        return self._bullet_type

    # Bullet Level
    def set_level(self, up=True) -> None:
        if up:
            if self._bullet_type.get_max_level() > self._lever:
                self._lever += 1
            else:
                print("Max level")
        else:
            if 1 < self._lever:
                self._lever -= 1
            else:
                print("0 level")

    def get_level(self) -> int:
        return self._lever

    # Attack Speed
    def set_attack_speed(self, attack_speed) -> None:
        self._attack_speed = attack_speed

    def get_attack_speed(self) -> int:
        return self._attack_speed

    # Health
    def set_health(self, health) -> None:
        self._health = health

    def get_health(self) -> int:
        return self._health

    """ ----------------- Reset methods -----------------"""

    # Reset
    def reset(self, point=None) -> None:
        self.is_active = True
        self._image_switch = 0
        self.set_pos(point)
        # self.is_invincible = True
        self._set_image_type("MoveNormal")
        self._bullet_type = PlayerBullet1
        self._lever = 1
        self._health = self._MAX_HEALTH

    """ ----------------- Class init methods -----------------"""

    @classmethod
    def _init_speed(cls) -> None:
        if not hasattr(cls, "_INIT_FLAG_SPEED") or not cls._INIT_FLAG_SPEED:
            cls._MAX_SPEED_L = 8
            cls._MAX_SPEED_R = 8
            cls._MAX_SPEED_UP = 10
            cls._MAX_SPEED_DOWN = 5
            cls._INIT_FLAG_SPEED = True

    @classmethod
    def _init_acc(cls) -> None:
        if not hasattr(cls, "_INIT_FLAG_ACC") or not cls._INIT_FLAG_ACC:
            cls._ACC_L = 0.8
            cls._ACC_R = 0.8
            cls._ACC_UP = 1
            cls._ACC_DOWN = 0.6
            cls._INIT_FLAG_ACC = True

    @classmethod
    def _init_sound(cls) -> None:
        if not hasattr(cls, "_INIT_FLAG_SOUND") or not cls._INIT_FLAG_SOUND:
            cls._SOUND = dict()
            from LostViking.src.generic_loader.sound_loader import load_sound
            from LostViking.src.constants import MAIN_VOLUME
            cls._SOUND.setdefault("Player_Shoot", load_sound("Player_Shoot.wav", MAIN_VOLUME - 0.2))
            cls._SOUND.setdefault("Player_Explo", load_sound("Player_Explo.wav", MAIN_VOLUME))
            cls._INIT_FLAG_SOUND = True

    @classmethod
    def init(cls) -> None:
        if not hasattr(cls, "_INIT_FLAG") or not cls._INIT_FLAG:
            cls._init_image()
            cls._init_speed()
            cls._init_acc()
            cls._init_sound()
            cls._MAX_HEALTH = 300
            cls._INIT_FLAG = True


class Player1(BasicPlayerPlane):

    def __init__(self):
        BasicPlayerPlane.__init__(self)
        self.add(Player1_G)

    @classmethod
    def _init_image(cls) -> None:
        if not hasattr(cls, "_INIT_FLAG_IMAGE") or not cls._INIT_FLAG_IMAGE:
            cls._IMAGE = dict()
            from LostViking.src.generic_loader.image_loader import load_image
            cls._IMAGE["Base"] = [load_image("PlayerPlane/Viking_body.png")]
            cls._IMAGE.setdefault("Invincible", [load_image("PlayerPlane/PlayerPlane_Invincible.png")])
            cls._IMAGE.setdefault("MoveUp", [load_image("PlayerPlane/PlayerPlane_moveUp1.png"),
                                             load_image("PlayerPlane/PlayerPlane_moveUp2.png")])
            cls._IMAGE.setdefault("MoveDown", [load_image("PlayerPlane/PlayerPlane_moveDown1.png"),
                                               load_image("PlayerPlane/PlayerPlane_moveDown2.png")])
            cls._IMAGE.setdefault("MoveNormal", [load_image("PlayerPlane/PlayerPlane_moveNormal1.png"),
                                                 load_image("PlayerPlane/PlayerPlane_moveNormal2.png")])
            cls._IMAGE.setdefault("Explode", [load_image("PlayerPlane/PlayerPlane_explode1.png"),
                                              load_image("PlayerPlane/PlayerPlane_explode2.png"),
                                              load_image("PlayerPlane/PlayerPlane_explode3.png"),
                                              load_image("PlayerPlane/PlayerPlane_explode4.png"),
                                              load_image("PlayerPlane/PlayerPlane_explode5.png"),
                                              load_image("PlayerPlane/PlayerPlane_explode6.png")])
            cls._INIT_FLAG_IMAGE = True


class Player2(BasicPlayerPlane):

    def __init__(self):
        BasicPlayerPlane.__init__(self)
        self.add(Player2_G)

    @classmethod
    def _init_image(cls) -> None:
        if not hasattr(cls, "_INIT_FLAG_IMAGE") or not cls._INIT_FLAG_IMAGE:
            cls._IMAGE = dict()
            from LostViking.src.generic_loader.image_loader import load_image
            cls._IMAGE["Base"] = [load_image("PlayerPlane/Viking_body.png")]
            cls._IMAGE.setdefault("Invincible", [load_image("PlayerPlane/PlayerPlane_Invincible.png")])
            cls._IMAGE.setdefault("MoveUp", [load_image("PlayerPlane/PlayerPlane_moveUp1.png"),
                                             load_image("PlayerPlane/PlayerPlane_moveUp2.png")])
            cls._IMAGE.setdefault("MoveDown", [load_image("PlayerPlane/PlayerPlane_moveDown1.png"),
                                               load_image("PlayerPlane/PlayerPlane_moveDown2.png")])
            cls._IMAGE.setdefault("MoveNormal", [load_image("PlayerPlane/PlayerPlane_moveNormal1.png"),
                                                 load_image("PlayerPlane/PlayerPlane_moveNormal2.png")])
            cls._IMAGE.setdefault("Explode", [load_image("PlayerPlane/PlayerPlane_explode1.png"),
                                              load_image("PlayerPlane/PlayerPlane_explode2.png"),
                                              load_image("PlayerPlane/PlayerPlane_explode3.png"),
                                              load_image("PlayerPlane/PlayerPlane_explode4.png"),
                                              load_image("PlayerPlane/PlayerPlane_explode5.png"),
                                              load_image("PlayerPlane/PlayerPlane_explode6.png")])
            cls._INIT_FLAG_IMAGE = True
