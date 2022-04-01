
from typing import Sequence


class Size:
    def __init__(self, width, height) -> None:
        self._width = width
        self._height = height

    def __init__(self, size: list[int, int]) -> None:
        self._width = size[0]
        self._height = size[1]

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height


class Pos:
    def __init__(self, x: int, y: int) -> None:
        self._x = x
        self._y = y

    def __init__(self, pos: list[int, int]) -> None:
        self._x = pos[0]
        self._y = pos[1]

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    def move_x(self, x):
        return Pos([self._x + x, self._y])

    def move_y(self, y):
        return Pos([self._x, self._y + y])

    def move(self, x, y):
        return Pos([self._x + x, self._y + y])

    def move(self, pos: list[int, int]):
        return Pos([self._x + pos[0], self._y + pos[1]])

    def to_list(self):
        return self._x, self._y
