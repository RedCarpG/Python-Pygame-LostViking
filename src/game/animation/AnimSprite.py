from pygame import Rect
from pygame.sprite import Sprite
from src.util.type import Size


class AnimSprite(Sprite):
    def __init__(self, frames: dict, frame_size: Size = None):
        # Init Sprite
        Sprite.__init__(self)

        # Set Image properties
        self.frames = frames
        self.current_state = None
        self.current_frame = None

        self._max_frame_index = 0
        self._max_frame_width = None
        self._current_frame_index = 0
        self._anime_interval = 0

        if frame_size:
            self._img_w = frame_size.width
            self._img_h = frame_size.height
            self._chop_rect = Rect(0, 0, self._img_w, self._img_h)
        else:
            rect = self.frames["BASE"].get_rect()
            self._img_w = rect.width
            self._img_h = rect.height
            self._chop_rect = Rect(0, 0, self._img_w, self._img_h)

        self.set_anime_state("IDLE")
        self.image = self.image.subsurface(self._chop_rect)
        self.rect = Rect(0, 0, self._img_w, self._img_h)

    def anime_end_loop_hook(self):
        pass

    def anime(self, anime_freq=5):
        """
        Switch image function should be called per frame
        :param switch_rate: switch rate between each change
        :return: True if loop finished, False if loop not finished
        """
        if self._anime_interval >= anime_freq:
            self._next_image()
            self._anime_interval = 0
        else:
            self._anime_interval += 1

    def _next_image(self) -> None:
        self._current_frame_index = (
            self._current_frame_index + 1) % self._max_frame_index
        self.image = self.frames[self.current_state].subsurface(
            self._chop_rect.move(self._current_frame_index * self._img_w, 0))
        if self._current_frame_index == 0:
            self.anime_end_loop_hook()

    @property
    def frame_size(self):
        return Size([self._img_w, self._img_h])

    def set_anime_state(self, state) -> None:
        """
        Change main loop image
        :param image_type: Name of the type of image to put into loop
        """
        self._current_frame_index = 0
        self._anime_interval = 0
        self.current_state = state
        self.current_frame = self.frames[state]
        self._max_frame_width = self.current_frame.get_width()
        self._max_frame_index = int(self._max_frame_width / self._img_w)

        self.image = self.current_frame.subsurface(self._chop_rect)
