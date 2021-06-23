

def accelerate(speed, max_speed, direction, acc):
    if direction == 1:
        if speed < max_speed:
            speed += acc
        else:
            speed = max_speed
    else:
        if speed > -max_speed:
            speed -= acc
        else:
            speed = -max_speed
    return speed


def decelerate(speed, acc):
    if speed > 0:  # If it is moving down, decelerate by _ACC_UP
        speed -= acc
        if speed <= 0:
            speed = 0
    elif speed < 0:  # If it is moving up, decelerate by _ACC_DOWN
        speed += acc
        if speed >= 0:
            speed = 0
    return speed
