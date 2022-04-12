
from src.game.animation import AnimeSprite, AnimeSprite
from src.util.type import Pos, Size
from src.game.groups import G_Effects


class Effect(AnimeSprite):

    def __init__(self, pos: Pos, frames, frame_size: Size) -> None:
        super().__init__(frames, frame_size)

        self.rect.center = pos.to_list()
        G_Effects.add(self)

    def anime_end_loop_hook(self):
        self.kill()

    def update(self):
        self.anime()


class AttachEffect(AnimeSprite):

    def __init__(self, ref, frames, frame_size: Size, enable_rotate=True, angle=0, cb_func=None) -> None:
        super().__init__(frames, frame_size, enable_rotate=enable_rotate, angle=angle)

        self.rect.center = ref.rect.center
        self.ref = ref
        G_Effects.add(self)
        self.angle = ref.angle
        self.cb_func = cb_func

    def anime_end_loop_hook(self):
        if self.cb_func:
            self.cb_func()
        self.kill()

    def update(self):
        self.anime()
        self.rect.center = self.ref.rect.center
        self.angle = self.ref.angle
