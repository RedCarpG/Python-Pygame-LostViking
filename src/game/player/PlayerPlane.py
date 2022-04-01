""" Player controllable object
Includes:
    -> PlayerPlane
"""
import pygame
from src.game.animation import AnimSprite
from src.setting import SCREEN_WIDTH, SCREEN_HEIGHT

from src.helper.sound import play_sound
from src.util.inertial import accelerate, decelerate
from src.helper.image import get_image
from src.util.type import Pos
from src.game.generic_items.Effect import AttachEffect
from .PlayerWeapon import PlayerWeapon, PlayerWeaponViking


class PlayerPlane(AnimSprite):
    """ Basic Player Abstract class
    """
    BOMB_COUNT_MAX = 3
    BOMB_COUNT_DEFAULT = 3

    LIFE_MAX = 5
    LIFE_DEFAULT = 3

    LEVEL_MAX = 3

    MAX_SPEED_X = 8
    MAX_SPEED_UP = 10
    MAX_SPEED_DOWN = 5
    ACC_X = 0.8
    ACC_UP = 1
    ACC_DOWN = 0.6
    MAX_HEALTH = 300

    def __init__(self, weapon: PlayerWeapon, pos, frames, frame_size):
        # Init
        AnimSprite.__init__(self, frames=frames, frame_size=frame_size)

        if pos:
            self.start_position = pos
        else:
            self.start_position = (int(pygame.display.get_surface().get_width() // 2),
                                   int(pygame.display.get_surface().get_height() - self.rect.height // 2 - 30))

        # Set bullet type
        ''' Init Weapon '''
        self._weapon = weapon

        self.score = 0
        self._life = self.LIFE_DEFAULT
        self._bomb_count = self.BOMB_COUNT_DEFAULT
        self._level = 1

        self._speed = pygame.Vector2(0, 0)
        self._health = self.MAX_HEALTH

        self._attack_speed = 20
        self._count_attack_interval = 0

        ''' States '''
        self.state = None
        self.is_invincible = False
        self.is_active = True
        self._is_moving_x = False
        self._is_moving_y = False

        # Set init position
        self.set_pos(pos)

    def anime_end_loop_hook(self):
        if not self.is_active:
            self.reset()

    # --------------------- Player Plane Behavior ---------------------

    def update(self) -> None:
        """ Update method from Sprite, is called per frame """
        self.anime()
        self._move()
        self._reload()

    def _move(self) -> None:
        if self._speed.y != 0 or self._speed.x != 0:
            # Move this object
            # (Note: this is the only place when the object is really moving)
            self.rect.move_ip(self._speed)

            # Speed down if there's no movement command on X or Y
            # (Note: Only values of _speed_x/_speed_y will be changed here)
            if not self._is_moving_x:
                self._speed.x = decelerate(self._speed.x, self.ACC_X)
            if not self._is_moving_y:
                self._speed.y = decelerate(self._speed.y, self.ACC_DOWN)

            # Restrict the plane inside the screen
            if self.rect.bottom > SCREEN_HEIGHT:
                self.rect.bottom = SCREEN_HEIGHT
            if self.rect.left < 0:
                self.rect.left = 0
            if self.rect.right > SCREEN_WIDTH:
                self.rect.right = SCREEN_WIDTH
            if self.rect.top < 0:
                self.rect.top = 0

    def _reload(self):
        if self._count_attack_interval > 0:
            self._count_attack_interval -= 1

    def _destroy(self) -> None:
        self.is_active = False
        self._is_moving_y = False
        self._is_moving_x = False
        self.set_anime_state("EXPLODE")
        play_sound("PLAYER_EXPLODE")

    # ------------------ Battle ------------------
    def hit(self, damage=100, **kwargs) -> bool:
        """
        This function is called in collision detection
        """
        if not self.is_invincible and self.is_active:
            # Take damage
            self._health -= damage
            if self._health > 0:
                # Get Hit effect
                AttachEffect(self.rect, frames={
                    "IDLE": self.frames["HIT"]
                }, frame_size=self.frame_size)
            else:
                # HP below 0
                self._health = 0
                self._destroy()
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

    def attack(self) -> None:
        """
        This method is called from a user attack event
        """
        if self.is_active:
            if self._count_attack_interval == 0:
                play_sound("PLAYER_SHOOT")
                self._weapon.shoot(pos=Pos(self.rect.center))
                self._count_attack_interval = self._attack_speed

    # ------------------ Trigger-Movement-Commands ------------------
    # ------------------ (Instant trigger method called by events) --
    # Trigger Move Up
    def trigger_move_up(self) -> None:
        """ Trigger this object to move Up (with acceleration)
        Called by event (e.g. Button press)
        """
        if not self.is_active:
            return
        # If the plane starts to move, switch frame to "MOVE_UP"
        if not self._is_moving_y:
            self._is_moving_y = True
            self.set_anime_state("MOVE_UP")
        # If not outside the screen
        if self.rect.top > 0:
            self._speed.y = accelerate(
                self._speed.y, self.MAX_SPEED_UP, -1, self.ACC_UP)
        else:
            self._speed.y = 0
            self.rect.top = 0

    # Trigger Move Down
    def trigger_move_back(self) -> None:
        """ Trigger this object to move Down (with acceleration)
        Called by event (e.g. Button press)
        (Note: This method only change the value of _speed_x / _speed_y)
        """
        if not self.is_active:
            return
        # If it was not moving before, change image
        if not self._is_moving_y:
            self._is_moving_y = True
            self.set_anime_state("MOVE_DOWN")
        # If not outside the screen
        if self.rect.bottom < SCREEN_HEIGHT:
            self._speed.y = accelerate(
                self._speed.y, self.MAX_SPEED_UP, 1, self.ACC_DOWN)
        else:
            self._speed.y = 0
            self.rect.bottom = SCREEN_HEIGHT

    # Trigger Move Left
    def trigger_move_left(self) -> None:
        """ Trigger this object to move Left (with acceleration)
        Called by event (e.g. Button press)
        (Note: This method only change the value of _speed_x / _speed_y)
        """
        if not self.is_active:
            return
        # If not outside the screen
        if self.rect.left > 0:
            self._is_moving_x = True
            self._speed.x = accelerate(
                self._speed.x, self.MAX_SPEED_X, -1, self.ACC_X)
        else:
            self._speed.x = 0
            self.rect.left = 0

    # Trigger Move Right
    def trigger_move_right(self) -> None:
        """ Trigger this object to move Right (with acceleration)
        Called by event (e.g. Button press)
        (Note: This method only change the value of _speed_x / _speed_y)
        """
        if not self.is_active:
            return
        # If not outside the screen
        if self.rect.right < SCREEN_WIDTH:
            self._is_moving_x = True
            self._speed.x = accelerate(
                self._speed.x, self.MAX_SPEED_X, 1, self.ACC_X)
        else:
            self._speed.x = 0
            self.rect.right = SCREEN_WIDTH

    # Trigger Brake y, only triggered when lease the button
    def trigger_stop_y(self) -> None:
        """ Trigger this object to stop in y axis (with acceleration)
        Triggered by event (e.g. Button release)
        (Note: This only sets the flag, the deceleration will be done
        by _inertial_deceleration automatically in update)
        """
        self._is_moving_y = False
        if self.is_active:
            self.set_anime_state("IDLE")

    # Trigger Brake x
    def trigger_stop_x(self) -> None:
        """ Trigger this object to stop in x axis (with acceleration)
        Triggered by event (e.g. Button release)
        (Note: This only sets the flag, the deceleration will be done
        by _inertial_deceleration automatically in update)
        """
        self._is_moving_x = False

    # ------------------ Interface-----------------

    # ----- Life
    @property
    def life(self) -> int:
        return self._life

    def add_life(self) -> None:
        if self._life >= self.LIFE_MAX:
            raise("Error: Max life attend.")
        self._life += 1

    def dec_life(self) -> None:
        if self._life <= 0:
            raise("Error: Can't decrease life under 0.")
        self._life -= 1

    # ----- Weapon & Level

    @property
    def weapon(self) -> PlayerWeapon:
        return self._weapon

    @weapon.setter
    def weapon(self, weapon_type) -> None:
        self._weapon = weapon_type

    @property
    def level(self) -> int:
        return self.weapon.level

    def level_up(self) -> None:
        self.weapon.level_up()

    def level_down(self) -> None:
        self.weapon.level_down()

    def reset_level(self) -> None:
        self.weapon.reset_level()

    # ----- Attack Speed
    @property
    def attack_speed(self) -> int:
        return self._attack_speed

    def set_attack_speed(self, attack_speed) -> None:
        self._attack_speed = attack_speed

    # ----- Position
    @property
    def pos(self) -> tuple[int, int]:
        return self.rect.center

    def set_pos(self, point=None) -> None:
        if point is None:
            self.rect.center = self.start_position
        else:
            # Move its rect to a point, or a default position
            self.rect.center = point

    # ----- Speed
    @property
    def speed(self) -> pygame.Vector2:
        return self._speed

    # ----- Health
    @property
    def health(self) -> int:
        return self._health

    def set_health(self, health) -> None:
        self._health = health

    # ----- Bomb
    @property
    def bomb_count(self) -> int:
        return self._bomb_count

    def add_nuc_bomb(self) -> None:
        if self._bomb_count >= self.BOMB_COUNT_MAX:
            return
        self._bomb_count += 1

    def dec_nuc_bomb(self) -> None:
        if self._bomb_count <= 0:
            return
        self._bomb_count -= 1

    # ----------------- Reset method -----------------
    # Reset
    def reset(self, point=None) -> None:
        self.is_active = True
        self.set_anime_state("IDLE")
        self.set_pos(point)
        # self.is_invincible = True
        self._weapon.reset_level()
        self._health = self.MAX_HEALTH


class PlayerViking(PlayerPlane):
    def __init__(self, pos):
        super().__init__(
            weapon=PlayerWeaponViking(),
            pos=pos,
            frames={
                "BASE": get_image("PlayerPlane/VikingBase.png"),
                "IDLE": get_image("PlayerPlane/VikingIdle.png"),

                "MOVE_UP": get_image("PlayerPlane/VikingMoveUp.png"),
                "MOVE_DOWN": get_image("PlayerPlane/VikingMoveDown.png"),
                "EXPLODE": get_image("PlayerPlane/VikingExplode.png"),

                "HIT": get_image("PlayerPlane/VikingHit.png")
            },
            frame_size=None)
