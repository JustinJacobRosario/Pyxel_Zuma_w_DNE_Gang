from abc import ABC, abstractmethod
from bullets import * # temp, wildcard import bad
# from enemies import Color
import random

class Tower(ABC):
    def __init__(self, pos_col, pos_row, color_type, bullet_type):
        self._fire_rate: float = 0.5 # bullets / second
        self._color: Color = color_type
        self._bullet: Bullet = bullet_type # should control bullet speed and hits
        self._col: float = float(pos_col) # defined per instance
        self._row: float = float(pos_row) # defined per instance
        self._upgraded: bool = False
        self._exp_cost: int = 0
        self._range: int = 0
		
    def get_exp_cost(self) -> int:
        return self._exp_cost

    def get_range(self) -> int:
        return self._range

    def pick_bullet_color(self) -> Color:
        return random.choice(self._bullet_colors)

    def can_shoot(self, target) -> bool:
        d_col = target.col - self._col
        d_row = target.row - self._row
        distance = (d_col ** 2 + d_row ** 2) ** 0.5
        return distance <= self._range

    def shoot(self, target) -> Bullet:
        color = self.pick_bullet_color()
		
class RainbowTower(Tower): # this is the basic tower i just couldnt think of a better name
	...