from __future__ import annotations
from enum import Enum, auto
import pyxel 

class Msg(Enum):
    SHOOT = auto()
    SHIFTMODE = auto()
    CONTINUE = auto()
    QUIT = auto()


class Player:
    def __init__(self):
        self.keys_map: dict[Msg, int] = {
            Msg.SHOOT: pyxel.MOUSE_BUTTON_LEFT,
            Msg.SHIFTMODE: pyxel.KEY_SHIFT,
            Msg.CONTINUE: pyxel.KEY_SPACE,
            Msg.CONTINUE: pyxel.KEY_Q
        }