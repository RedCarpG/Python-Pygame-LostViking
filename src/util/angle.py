import math
from unittest import result

from pygame import Vector2

from src.util.type import Pos


def cal_angle(base_point: Pos, target_point: Pos) -> int:
    """ Calculate angle between two points
    :param base_point
    :param target_point
    :return int angle degree value
    """
    vec = Vector2(0, 1)

    if base_point.y == target_point.y:
        if target_point.x > base_point.x:
            angle = 90
        else:
            angle = -90
    elif base_point.x == target_point.x:
        if target_point.y > base_point.y:
            angle = 0
        else:
            angle = 180
    else:
        angle = math.atan(
            (target_point.y - base_point.y) / (target_point.x - base_point.x))
        angle = 90 - angle * 360 / 2 / math.pi
        if base_point.x > target_point.x:
            angle -= 180

    return angle


def follow_angle(base_point: Pos, target_point: Pos, current_angle, rotation_speed) -> int:

    angle = cal_angle(base_point, target_point)

    direction = 0
    if current_angle > angle:
        direction = -1
    elif current_angle < angle:
        direction = 1

    diff = abs(current_angle - angle)
    if diff > 180:
        direction = - direction

    result = current_angle + direction * rotation_speed
    if result < -180:
        result = 180
    elif result > 180:
        result = -180
    return result

    if base_point.x > target_point.x and current_angle > 90:
        current_angle += rotation_speed
    elif base_point.x < target_point.x and current_angle < -90:
        current_angle -= rotation_speed
    elif self.angle > angle:
        self.angle -= 2
    elif self.angle < angle:
        self.angle += 2

    if self.angle < -180:
        self.angle = 180
    if self.angle > 180:
        self.angle = -180
