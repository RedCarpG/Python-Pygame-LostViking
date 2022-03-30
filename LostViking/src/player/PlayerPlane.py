""" Player controllable object
Includes:
    -> PlayerPlane
"""
from abc import ABC
import pygame
from ..generic_items.BasicPlaneEntity import BasicPlaneEntity
from ..generic_loader.sound_loader import play_sound
from .PlayerWeapon import PlayerBullet1
from ..constants import SCREEN_WIDTH, SCREEN_HEIGHT
from ..groups import Player1_G, Player2_G
from ..generic_items.inertial_behavior import accelerate, decelerate


class BasicPlayerPlane(BasicPlaneEntity, ABC):
    """ Basic Player Abstract class
    """

    def __init__(self, point=None, **kwargs):
        # Init
        BasicPlaneEntity.__init__(self, **kwargs)

        # Set bullet type
        ''' Init Weapon '''
        self.start_position = (int(pygame.display.get_surface().get_width() // 2),
                               int(pygame.display.get_surface().get_height() - self.rect.height // 2 - 30))

        ''' Init States '''
        self.is_invincible = False

        ''' Init Weapon '''
        self._weapon_type = PlayerBullet1
        self._lever = 1

        self._attack_speed = 20
        self._count_attack_interval = 0

        self._move_flag_x = False
        self._move_flag_y = False

        # Set init position
        self.set_pos(point)

    # --------------------- Player Plane Behavior ---------------------
    def _shoot(self):
        self._weapon_type.shoot_bullets(self.rect.center, self._lever)

    # ------------------ Status ------------------
    def _action_phase(self, *args, **kwargs) -> None:
        # When _speed_x/_speed_y is not 0
        if self._speed_y != 0 or self._speed_x != 0:
            # Move this object
            # (Note: this is the only place when the object is really moving)
            self._move()

            # Speed down if there's no movement command on X or Y
            # (Note: Only values of _speed_x/_speed_y will be changed here)
            if not self._move_flag_x:
                self._speed_x = decelerate(self._speed_x, self.ACC_X)
            if not self._move_flag_y:
                self._speed_y = decelerate(self._speed_y, self.ACC_DOWN)

            # Restrict the plane inside the screen
            if self.rect.bottom > SCREEN_HEIGHT:
                self.rect.bottom = SCREEN_HEIGHT
            if self.rect.left < 0:
                self.rect.left = 0
            if self.rect.right > SCREEN_WIDTH:
                self.rect.right = SCREEN_WIDTH
            if self.rect.top < 0:
                self.rect.top = 0

        if self._count_attack_interval > 0:
            self._count_attack_interval -= 1

    def _destroy_phase(self, *args, **kwargs) -> None:
        image_loop_finished = kwargs.pop("image_loop_finished", True)
        if image_loop_finished:
            self.reset()

    # ------------------ Collision detect ------------------
    def hit(self, damage=100, **kwargs) -> bool:
        """
        This function is called in collision detection
        """
        if not self.is_invincible:
            if self._damaged(damage):
                self.is_active = False
                self._image_switch = 0
                self._set_image_type("EXPLODE")
                play_sound("PLAYER_EXPLODE")
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

    # ------------------ Trigger-Action-Commands ------------------
    def attack(self) -> None:
        """
        This method is called from a user attack event
        """
        if self.is_active:
            if self._count_attack_interval == 0:
                play_sound("PLAYER_SHOOT")
                self._shoot()
                self._count_attack_interval = self._attack_speed

    # ------------------ Trigger-Movement-Commands ------------------
    # ------------------ (Instant trigger method called by events) --
    # Trigger Move Up
    def trigger_move_up(self) -> None:
        """ Trigger this object to move Up (with acceleration)
        Called by event (e.g. Button press)
        """
        # If it was not moving before, change image
        if not self._move_flag_y:
            self._move_flag_y = True
            self._set_image_type("MOVE_UP")
        # If not outside the screen
        if self.rect.top > 0:
            self._speed_y = accelerate(self._speed_y, self.MAX_SPEED_UP, -1, self.ACC_UP)
        else:
            self._speed_y = 0
            self.rect.top = 0
            self._set_image_type("IDLE")

    # Trigger Move Down
    def trigger_move_back(self) -> None:
        """ Trigger this object to move Down (with acceleration)
        Called by event (e.g. Button press)
        (Note: This method only change the value of _speed_x / _speed_y)
        """
        # If it was not moving before, change image
        if not self._move_flag_y:
            self._move_flag_y = True
            self._set_image_type("MOVE_DOWN")
        # If not outside the screen
        if self.rect.bottom < SCREEN_HEIGHT:
            self._speed_y = accelerate(self._speed_y, self.MAX_SPEED_UP, 1, self.ACC_DOWN)
        else:
            self._speed_y = 0
            self.rect.bottom = SCREEN_HEIGHT
            self._set_image_type("IDLE")

    # Trigger Move Left
    def trigger_move_left(self) -> None:
        """ Trigger this object to move Left (with acceleration)
        Called by event (e.g. Button press)
        (Note: This method only change the value of _speed_x / _speed_y)
        """
        # If not outside the screen
        if self.rect.left > 0:
            self._move_flag_x = True
            self._speed_x = accelerate(self._speed_x, self.MAX_SPEED_X, -1, self.ACC_X)
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
        if self.rect.right < SCREEN_WIDTH:
            self._move_flag_x = True
            self._speed_x = accelerate(self._speed_x, self.MAX_SPEED_X, 1, self.ACC_X)
        else:
            self._speed_x = 0
            self.rect.right = SCREEN_WIDTH

    # Trigger Brake y, only triggered when lease the button
    def trigger_stop_y(self) -> None:
        """ Trigger this object to stop in y axis (with acceleration)
        Triggered by event (e.g. Button release)
        (Note: This only sets the flag, the deceleration will be done
        by _inertial_deceleration automatically in update)
        """
        self._move_flag_y = False
        self._set_image_type("IDLE")

    # Trigger Brake x
    def trigger_stop_x(self) -> None:
        """ Trigger this object to stop in x axis (with acceleration)
        Triggered by event (e.g. Button release)
        (Note: This only sets the flag, the deceleration will be done
        by _inertial_deceleration automatically in update)
        """
        self._move_flag_x = False

    # ------------------ Interface-----------------
    # Bullet Type
    def change_bullet_type(self, bul_class) -> None:
        from LostViking.src.generic_items.BasicBullet import BasicBullet
        if not issubclass(bul_class, BasicBullet):
            raise Exception("ERROR: Bullet type {} is not supported".format(bul_class))
        if self._weapon_type != bul_class:
            self._weapon_type = bul_class
            self._lever = 1

    def get_bullet_type(self):
        return self._weapon_type

    # Bullet Level
    def set_level(self, up=True) -> None:
        if up:
            if self._weapon_type.get_max_level() > self._lever:
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

    def set_pos(self, point) -> None:
        if not point:
            self.rect.center = self.start_position
        else:
            # Move its rect to a point, or a default position
            self.rect.center = point

    # ----------------- Reset methods -----------------
    # Reset
    def reset(self, point=None) -> None:
        self.is_active = True
        self._image_switch = 0
        self.set_pos(point)
        # self.is_invincible = True
        self._set_image_type("IDLE")
        self._weapon_type = PlayerBullet1
        self._lever = 1
        self._health = self.MAX_HEALTH

    # ----------------- Class init methods -----------------
    @classmethod
    def _init_attributes(cls) -> None:
        cls.MAX_SPEED_X = 8
        cls.MAX_SPEED_UP = 10
        cls.MAX_SPEED_DOWN = 5
        cls.ACC_X = 0.8
        cls.ACC_UP = 1
        cls.ACC_DOWN = 0.6
        cls.MAX_HEALTH = 300
        cls._IS_SET_ATTRS = True


class Player1(BasicPlayerPlane):

    def __init__(self):
        BasicPlayerPlane.__init__(self)
        self.add(Player1_G)

    @classmethod
    def _init_image(cls) -> None:
        cls.IMAGE = dict()
        from ..generic_loader.image_loader import load_image
        cls.IMAGE["BASE"] = [load_image("PlayerPlane/VikingBody.png")]
        cls.IMAGE["IDLE"] = [load_image("PlayerPlane/VikingMoveDown1.png"),
                             load_image("PlayerPlane/VikingMoveDown2.png"),
                             load_image("PlayerPlane/VikingMoveDown3.png"),
                             load_image("PlayerPlane/VikingMoveDown4.png"),
                             load_image("PlayerPlane/VikingMoveDown5.png"),
                             load_image("PlayerPlane/VikingMoveDown6.png"),
                             load_image("PlayerPlane/VikingMoveDown7.png"),
                             load_image("PlayerPlane/VikingMoveDown8.png")]
        cls.IMAGE["MOVE_UP"] = [load_image("PlayerPlane/VikingMoveUp1.png"),
                                load_image("PlayerPlane/VikingMoveUp2.png"),
                                load_image("PlayerPlane/VikingMoveUp3.png"),
                                load_image("PlayerPlane/VikingMoveUp4.png"),
                                load_image("PlayerPlane/VikingMoveUp5.png"),
                                load_image("PlayerPlane/VikingMoveUp6.png"),
                                load_image("PlayerPlane/VikingMoveUp7.png"),
                                load_image("PlayerPlane/VikingMoveUp8.png")]
        cls.IMAGE["MOVE_DOWN"] = cls.IMAGE["IDLE"]
        cls.IMAGE["EXPLODE"] = [load_image("PlayerPlane/PlayerPlane_explode1.png"),
                                load_image("PlayerPlane/PlayerPlane_explode2.png"),
                                load_image("PlayerPlane/PlayerPlane_explode3.png"),
                                load_image("PlayerPlane/PlayerPlane_explode4.png"),
                                load_image("PlayerPlane/PlayerPlane_explode5.png"),
                                load_image("PlayerPlane/PlayerPlane_explode6.png")]
        cls.IMAGE["INVINCIBLE"] = [load_image("PlayerPlane/PlayerPlane_Invincible.png")]
        cls._IS_SET_IMAGE = True


class Player2(BasicPlayerPlane):

    def __init__(self):
        BasicPlayerPlane.__init__(self)
        self.add(Player2_G)

    @classmethod
    def _init_image(cls) -> None:
        cls._IMAGE = dict()
        from ..generic_loader.image_loader import load_image
        cls.IMAGE["BASE"] = [load_image("PlayerPlane/Viking_body.png")]
        cls.IMAGE["IDLE"] = [load_image("PlayerPlane/PlayerPlane_moveNormal1.png"),
                             load_image("PlayerPlane/PlayerPlane_moveNormal2.png")]
        cls.IMAGE["MOVE_UP"] = [load_image("PlayerPlane/PlayerPlane_moveUp1.png"),
                                load_image("PlayerPlane/PlayerPlane_moveUp2.png")]
        cls.IMAGE["MOVE_DOWN"] = [load_image("PlayerPlane/PlayerPlane_moveDown1.png"),
                                  load_image("PlayerPlane/PlayerPlane_moveDown2.png")]
        cls.IMAGE["EXPLODE"] = [load_image("PlayerPlane/PlayerPlane_explode1.png"),
                                load_image("PlayerPlane/PlayerPlane_explode2.png"),
                                load_image("PlayerPlane/PlayerPlane_explode3.png"),
                                load_image("PlayerPlane/PlayerPlane_explode4.png"),
                                load_image("PlayerPlane/PlayerPlane_explode5.png"),
                                load_image("PlayerPlane/PlayerPlane_explode6.png")]
        cls.IMAGE["INVINCIBLE"] = [load_image("PlayerPlane/PlayerPlane_Invincible.png")]
        cls._IS_SET_IMAGE = True


# ----------------- Create Function -----------------
def create_player(player_num=1):
    if player_num == 1:
        return Player1(), None
    else:
        # TODO Point for P1, P2
        # return PlayerPlane(point=None), PlayerPlane(point=None, p_id=2)
        return None
