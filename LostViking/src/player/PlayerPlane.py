""" Player controllable object
Includes:
    -> PlayerPlane
"""
import warnings
from abc import abstractmethod

from ..generic_items.ImageHelper import LoopImageHelper
from .PlayerBullet import PlayerBullet1, PlayerBasicBullet
from ..constants import SCREEN
from ..groups import Player1_G, Player2_G
import pygame


class BasicPlayerPlane(LoopImageHelper, pygame.sprite.Sprite):
    """ Basic Player Abstract class with behavior defined below:
     -> movement
     -> acceleration
     -> shoot
     _> hit
     """

    # Constants
    _MAX_SPEED_L = 0
    _MAX_SPEED_R = 0
    _MAX_SPEED_UP = 0
    _MAX_SPEED_DOWN = 0
    _ACC_L = 0
    _ACC_R = 0
    _ACC_UP = 0
    _ACC_DOWN = 0

    _INIT_FLAG_PLAYER = False

    def __init__(self):
        # Init
        if not self._INIT_FLAG_PLAYER:
            print("!!! WARNING: {} speed value not set", self.__name__)
            self.init_player()
        LoopImageHelper.__init__(self)

        # Set Speed Values
        self._speed_x = 0
        self._speed_y = 0
        self._move_flag_x = False
        self._move_flag_y = False

        # Set Rect
        if hasattr(self, "image"):
            self.rect = self.image.get_rect()
        else:
            warnings.warn("WARNING: Attribute image is not set for {}".format(self))
            self.rect = pygame.rect.Rect(0, 0, 0, 0)

        # Set bullet type
        ''' Init Weapon '''
        self._bullet_type = None
        self._lever = 1

        self._attack_speed = 0

        self._health = 0

    def _move(self) -> None:
        """ Move its rect by its _speed_x and _speed_y"""
        self.rect.move_ip(self._speed_x, self._speed_y)

    """ --------------------- Deceleration --------------------- """

    # Speed down the plane when there's no movement commands on a X or Y direction
    def _inertial_deceleration(self) -> None:
        """ Decrease the _speed_x or _speed_y to 0 automatically
        (Note: This method only change the value of _speed_x / _speed_y)
        """
        # If no speed
        if self._speed_x == 0 and self._speed_y == 0:
            return
        else:
            # If no move X command but _speed_x != 0
            if not self._move_flag_x:

                if self._speed_x > 0:  # If it is moving right, decelerate by _ACC_L
                    self._speed_x -= self._ACC_L
                    if self._speed_x <= 0:
                        self._speed_x = 0
                elif self._speed_x < 0:  # If it is moving left, decelerate by _ACC_R
                    self._speed_x += self._ACC_R
                    if self._speed_x >= 0:
                        self._speed_x = 0

            # If no move Y command but _speed_y != 0
            if not self._move_flag_y:

                if self._speed_y > 0:  # If it is moving down, decelerate by _ACC_UP
                    self._speed_y -= self._ACC_UP
                    if self._speed_y <= 0:
                        self._speed_y = 0
                        if hasattr(self, "_set_image_type"):
                            self._set_image_type("MoveNormal")
                elif self._speed_y < 0:  # If it is moving up, decelerate by _ACC_DOWN
                    self._speed_y += self._ACC_DOWN
                    if self._speed_y >= 0:
                        self._speed_y = 0
                        if hasattr(self, "_set_image_type"):
                            self._set_image_type("MoveNormal")

    """ --------------------- Accelerations --------------------- """

    def _accelerate_up(self) -> None:
        """ In crease the _speed_y by _ACC_UP (negative)
        (Note: This method only change the value of _speed_x / _speed_y)
        """
        self._move_flag_y = True
        # If speed doesn't reach limit
        if self._speed_y > -self._MAX_SPEED_UP:
            self._speed_y -= self._ACC_UP

    def _accelerate_down(self) -> None:
        """ In crease the _speed_x by _ACC_DOWN (positive)
        (Note: This method only change the value of _speed_x / _speed_y)
        """
        self._move_flag_y = True
        # If speed doesn't reach limit
        if self._speed_y < self._MAX_SPEED_DOWN:
            self._speed_y += self._ACC_DOWN

    def _accelerate_left(self) -> None:
        """ In crease the _speed_x by _ACC_L (negative)
        (Note: This method only change the value of _speed_x / _speed_y)
        """
        self._move_flag_x = True
        # If speed doesn't reach limit
        if self._speed_x > -self._MAX_SPEED_L:
            self._speed_x -= self._ACC_L

    def _accelerate_right(self) -> None:
        """ In crease the _speed_x by _ACC_R (positive)
        (Note: This method only change the value of _speed_x / _speed_y)
        """
        self._move_flag_x = True
        # If speed doesn't reach limit
        if self._speed_x < self._MAX_SPEED_R:
            self._speed_x += self._ACC_R

    def _damaged(self, damage) -> bool:
        if self._health > 0:
            self._health -= damage
            return True
        else:
            self._health = 0
            return False

    def _shoot(self):
        self._bullet_type.shoot_bullets(self.rect.center, self._lever)

    @classmethod
    @abstractmethod
    def init_player(cls):
        pass


class PlayerPlane(BasicPlayerPlane):
    """ Player class inherits InertialEntity and Sprite """

    _SOUND = {}
    _INIT_FLAG_SOUND = False

    def __init__(self, point=None, p_id=1):
        BasicPlayerPlane.__init__(self)
        pygame.sprite.Sprite.__init__(self, Player1_G if p_id == 1 else Player2_G)

        if not self._INIT_FLAG_SOUND:
            self._init_sound()

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

        self._health = 300

        # Set init position
        self.set_pos(point)

    """ ------------------ Real-time methods ------------------ """

    def update(self) -> None:
        """ Overwrites update from Sprite,
        need to be called every frame """
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
        else:
            self.reset()
        self._switch_image()

    def hit(self, damage) -> bool:
        """ This function is called from collision test"""
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
        if not issubclass(bul_class, PlayerBasicBullet):
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

    # Position
    def set_pos(self, point=None) -> None:
        """ Move its rect to a point, or a default position """
        if point is None:
            self.rect.center = (int(pygame.display.get_surface().get_width() // 2),
                                int(pygame.display.get_surface().get_height() - self.rect.height // 2 - 30))
        else:
            self.rect.center = point

    def get_position(self) -> (list, tuple):
        return self.rect.center

    # Speed
    def get_speed(self):
        return self._speed_x, self._speed_y
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

    """ ----------------- Class init methods -----------------"""

    @classmethod
    def _init_image(cls) -> None:
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

    @classmethod
    def _clear_image(cls) -> None:
        cls._IMAGE.clear()
        cls._INIT_FLAG_IMAGE = False

    @classmethod
    def _init_sound(cls) -> None:
        from LostViking.src.generic_loader.sound_loader import load_sound
        from LostViking.src.constants import MAIN_VOLUME
        cls._SOUND.setdefault("Player_Shoot", load_sound("Player_Shoot.wav", MAIN_VOLUME - 0.2))
        cls._SOUND.setdefault("Player_Explo", load_sound("Player_Explo.wav", MAIN_VOLUME))
        cls._INIT_FLAG_SOUND = True

    @classmethod
    def init_player(cls) -> None:
        cls._init_image()
        cls._init_sound()
        cls._MAX_SPEED_L = 8
        cls._MAX_SPEED_R = 8
        cls._MAX_SPEED_UP = 10
        cls._MAX_SPEED_DOWN = 5

        cls._ACC_L = 0.8
        cls._ACC_R = 0.8
        cls._ACC_UP = 1
        cls._ACC_DOWN = 0.6
        cls._INIT_FLAG_PLAYER = True
