from src.setting import COLOR
from src.helper.font import FontEntity, load_font, get_font
from src.util.type import Pos


class FPSCounter:

    def __init__(self, surface, clock, pos):

        self.surface = surface
        self.clock = clock
        self.fps_text = FontEntity(surface, get_font("Scoreboard"),
                                   ("FPS: " + str(int(self.clock.get_fps()))), (10, 30), color=COLOR.WHITE)
        self.fps_text.move_center(pos)

    def blit(self):
        self.fps_text.blit()

    def update(self):
        self.fps_text.change_text("FPS: " + str(int(self.clock.get_fps())))
