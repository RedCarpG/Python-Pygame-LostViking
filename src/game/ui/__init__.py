from .Scoreboard import Scoreboard
from .BossUI import BossUI
from .FPSCounter import FPSCounter
from .UI import UI


def load_asset_ui():
    from src.helper.image import load_image
    from src.helper.font import load_font
    load_font("arialbd.ttf", 15, "HealthBar")
    load_image("UI/HealthBar.png")
    load_image("UI/Heart.png")
    load_image("UI/HeartBlink.png")
    load_image("UI/BottomLeft.png")
    load_image("UI/MidTop.png")
    load_image("UI/MidTop_HealthBar.png")
    load_image("UI/Viking.png")
