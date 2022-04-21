from pygame.sprite import collide_rect_ratio, collide_rect


def collide_detect(ratio=0.8):
    def collide_func(a, b):
        if collide_rect(a, b):
            if collide_rect_ratio(ratio)(a, b):
                return True
        return False
    return collide_func
