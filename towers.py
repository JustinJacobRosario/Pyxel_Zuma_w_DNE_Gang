from abc import ABC, abstractmethod
from bullets import Bullet, OrangeBullet, RedBullet, BlueBullet
from enemies import Color
import random

class Tower(ABC):
    _exp_cost: int = 0
    _range: float = 0.0
    _bullet_colors: list[Color] = []

    def __init__(self, pos_col, pos_row, bullet_type):
        self._fire_rate: float = 0.5 # bullets / second
        self._bullet: Bullet = bullet_type # should control bullet speed and hits
        self._col: float = float(pos_col) # defined per instance
        self._row: float = float(pos_row) # defined per instance
        self._upgraded: bool = False
	
    @property
    def col(self) -> float: # req for pos drawing and range checking
        return self._col
    
    @property
    def row(self) -> float: # req for pos drawing and range checking
        return self._row
    
    @property
    def fire_rate(self) -> float: # req for shooting cooldown
        return self._fire_rate
    
    @property
    def bullet(self) -> Bullet: # req for shooting and drawing
        return self._bullet
    
    @property
    def exp_cost(self) -> int: # req for placing
        return self._exp_cost
    
    # --

    def pick_bullet_color(self) -> Color:
        return random.choice(self._bullet_colors)

    def can_shoot(self, target) -> bool:
        d_col = target.col - self._col
        d_row = target.row - self._row
        distance = (d_col ** 2 + d_row ** 2) ** 0.5
        return distance <= self._range

    def shoot(self, target) -> Bullet:
        color = self.pick_bullet_color()
        bullet = self._bullet(color)
        bullet.x = self._col
        bullet.y = self._row
        bullet.is_used = False
        return bullet
		
class RainbowTower(Tower): # this is the basic tower i just couldnt think of a better name
	_exp_cost = 5
    _range = 5.0
    _bullet_colors = [Color.Orange, Color.Red, Color.Blue]

    def __init__(self, pos_col, pos_row):
        super().__init__(pos_col, pos_row)