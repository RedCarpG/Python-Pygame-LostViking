
from src.game.animation import AnimSprite
from src.util.type import Pos, Size
from src.game.groups import G_Effect


class Effect(AnimSprite):

    def __init__(self, pos: Pos, frames, frame_size: Size) -> None:
        AnimSprite.__init__(self, frames, frame_size)

        self.rect.center = pos.to_list()
        G_Effect.add(self)

    def anime_end_loop_hook(self):
        self.kill()
        del self

    def update(self):
        self.anime()


class AttachEffect(Effect):

    def __init__(self, rect, frames, frame_size: Size) -> None:
        Effect.__init__(self, Pos([rect.center[0], rect.center[1]]),
                        frames, frame_size)
        self.ref = rect

    def anime_end_loop_hook(self):
        self.kill()
        del self

    def update(self):
        self.anime()
        self.rect.center = self.ref.center
