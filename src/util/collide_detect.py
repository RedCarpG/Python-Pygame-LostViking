from pygame.sprite import collide_rect_ratio, collide_rect


def collide_detect(a, b):
    if collide_rect(a, b):
        if collide_rect_ratio(0.5)(a, b):
            return True
    return False
