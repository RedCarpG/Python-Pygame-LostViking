from .Effect import AttachEffect
from src.util.type import Pos, Size


class AttackEffect(AttachEffect):
    def __init__(self, ref, frames, frame_size: Size, cb_func) -> None:
        super().__init__(ref, frames, frame_size)
        self.cb_func = cb_func
    # ---------- Override

    def anime_end_loop_hook(self):
        self.cb_func()
        self.kill()
