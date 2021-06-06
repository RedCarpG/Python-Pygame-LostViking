""" Player controllable object
Includes:
    -> MyPlane
"""
from ..generic_items.entity import InertialEntity
from ..generic_items.graphic_helper import LoopImageHelper
from .player_bullet import PlayerBullet1, PlayerBasicBullet
from ..constants import SCREEN
from ..groups import Player1_G, Player2_G
import pygame


class MyPlane(LoopImageHelper, InertialEntity, pygame.sprite.Sprite):
    """ Player class inherits InertialEntity and Sprite """
    _MAX_SPEED_L = 8
    _MAX_SPEED_R = 8
    _MAX_SPEED_UP = 10
    _MAX_SPEED_DOWN = 5
    _ACC_L = 0.8
    _ACC_R = 0.8
    _ACC_UP = 1
    _ACC_DOWN = 0.6

    _SOUND = {}
    _SOUND_INIT_FLAG = False

    def __init__(self, point=None, p_id=1):
        LoopImageHelper.__init__(self)
        InertialEntity.__init__(self, point)
        pygame.sprite.Sprite.__init__(self, Player1_G if p_id == 1 else Player2_G)

        if not self._SOUND_INIT_FLAG:
            self.init_sound()

        self._set_image_type("MoveNormal")

        ''' Init States '''
        self.is_active = True
        self.is_invincible = False
        # self.invincible_reset = 0
        # self.crash_animation = 0

        ''' Init Weapon '''
        self._bullet_type = PlayerBullet1
        self._lever = 1

        self.attack_speed = 500

    """ ------------------ Real-time methods ------------------ """

    def update(self) -> None:
        """ Overwrites update from Sprite,
        need to be called every frame """
        # If alive
        if self.is_active:
            # When _speed_x/_speed_y is not 0
            if self.speed_y != 0 or self.speed_x != 0:
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
        else:
            self.reset()
        self._switch_image()

    def hit(self) -> bool:
        """ This function is called from collision test"""
        if not self.is_invincible:
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

    def shoot(self) -> None:
        self._SOUND["Player_Shoot"].stop()
        self._SOUND["Player_Shoot"].play()
        self._bullet_type.shoot_bullets(self.rect.center, self._lever)

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
            self.speed_y = 0
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
            self.speed_y = 0
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
            self.speed_x = 0
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
            self.speed_x = 0
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

    """ ------------------ Other ------------------"""

    # Set Bullet Type
    def change_bullet_type(self, bul_class) -> None:
        if not issubclass(bul_class, PlayerBasicBullet):
            raise Exception("ERROR: Bullet type {} is not supported".format(bul_class))
        if self._bullet_type != bul_class:
            self._bullet_type = bul_class
            self._lever = 1

    def level_up(self) -> None:
        if self._bullet_type.get_max_level() > self._lever:
            self._lever += 1
        else:
            print("Max_level")

    def get_level(self) -> int:
        return self._lever

    def get_position(self) -> list:
        return self.rect.center

    def get_attack_speed(self) -> int:
        return self.attack_speed

    # Reset
    def reset(self, point=None) -> None:
        self.is_active = True
        self._image_switch = 0
        self._set_pos(point)
        # self.is_invincible = True
        self._set_image_type("MoveNormal")
        self._bullet_type = PlayerBullet1
        self._lever = 1

    """ ----------------- Class init methods -----------------"""

    @classmethod
    def init_image(cls) -> None:
        from LostViking.src.generic_loader.image_loader import load_image
        cls._IMAGE["Base"] = [load_image("MyPlane/Viking_body.png")]
        cls._IMAGE.setdefault("Invincible", [load_image("MyPlane/MyPlane_Invincible.png")])
        cls._IMAGE.setdefault("MoveUp", [load_image("MyPlane/MyPlane_moveUp1.png"),
                                         load_image("MyPlane/MyPlane_moveUp2.png")])
        cls._IMAGE.setdefault("MoveDown", [load_image("MyPlane/MyPlane_moveDown1.png"),
                                           load_image("MyPlane/MyPlane_moveDown2.png")])
        cls._IMAGE.setdefault("MoveNormal", [load_image("MyPlane/MyPlane_moveNormal1.png"),
                                             load_image("MyPlane/MyPlane_moveNormal2.png")])
        cls._IMAGE.setdefault("Explode", [load_image("MyPlane/MyPlane_explode1.png"),
                                          load_image("MyPlane/MyPlane_explode2.png"),
                                          load_image("MyPlane/MyPlane_explode3.png"),
                                          load_image("MyPlane/MyPlane_explode4.png"),
                                          load_image("MyPlane/MyPlane_explode5.png"),
                                          load_image("MyPlane/MyPlane_explode6.png")])
        cls._INIT_FLAG = True

    @classmethod
    def _clear_image(cls) -> None:
        cls._IMAGE.clear()
        cls._INIT_FLAG = False

    @classmethod
    def init_sound(cls) -> None:
        from LostViking.src.generic_loader.sound_loader import load_sound
        from LostViking.src.constants import MAIN_VOLUME
        cls._SOUND.setdefault("Player_Shoot", load_sound("Player_Shoot.wav", MAIN_VOLUME - 0.2))
        cls._SOUND.setdefault("Player_Explo", load_sound("Player_Explo.wav", MAIN_VOLUME))
