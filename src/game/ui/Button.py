from src.game.animation import AnimeSprite
from src.util.type import Pos, Size
from pygame.sprite import AbstractGroup


class Button:

    def __init__(self, surface, function, frames: dict, *groups: AbstractGroup, **kwargs):
        self.surface = surface
        self.frames = frames
        self.image = frames["IDLE"]
        self.rect = self.image.get_rect()

        if "pos" in kwargs:
            self.rect.move_ip(kwargs["pos"].x, kwargs["pos"].y)
        elif "center" in kwargs:
            self.rect.center = (kwargs["center"].x, kwargs["center"].y)

        self.function = function
        self.is_hidden = False
        self.is_chosen = False

    def toggle_hide(self):
        self.is_hidden = not self.is_hidden

    def clicked(self):
        self.function(self)

    def toggle_choose(self, is_chosen=None):
        if is_chosen is not None:
            self.is_chosen = is_chosen
        else:
            self.is_chosen = not self.is_chosen
        if self.is_chosen:
            self.image = self.frames["CHOSEN"]
        else:
            self.image = self.frames["IDLE"]

    def blit(self):
        self.surface.blit(self.image, self.rect)
