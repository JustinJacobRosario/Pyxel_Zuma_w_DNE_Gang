from __future__ import annotations
from enum import Enum, auto
import pyxel 



# directions for the wasd directions of the bullet
class Dir(Enum):
    UP = auto()
    DOWN = auto()
    LEFT = auto()
    RIGHT = auto()

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

