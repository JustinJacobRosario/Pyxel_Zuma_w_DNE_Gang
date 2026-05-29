from abc import ABC, abstractmethod
from bullets import Bullet
from enemies import Color
import random

# BULLET_MAP = {
#     Color.Orange: OrangeBullet,
#     Color.Red: RedBullet,
#     Color.Blue: BlueBullet
# }

class Tower(ABC):
    _exp_cost: int = 0
    _upgrade_cost: int = 0
    _range: float = 0.0
    _bullet_colors: list[Color] = []

    def __init__(self, pos_col, pos_row):
        self._fire_rate: float = 0.5 # bullets / second
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
    def exp_cost(self) -> int: # req for placing and upgrading
        return self._exp_cost
    
    @property
    def bullet(self) -> Bullet: # req for shooting and drawing
        return self._bullet
    
    @property
    def exp_cost(self) -> int: # req for placing
        return self._exp_cost
    
    @property
    def upgraded(self) -> bool: # req for upgrading and drawing
        return self._upgraded
    
    # --

    def pick_bullet_color(self) -> Color:
        return random.choice(self._bullet_colors)

    def can_shoot(self, target) -> bool:
        d_col = target.col - self._col
        d_row = target.row - self._row
        distance = (d_col ** 2 + d_row ** 2) ** 0.5
        return distance <= self._range

    def shoot(self, target) -> list[Bullet]: 
        if self.upgraded:
            colors = random.sample(self._bullet_colors, 2)
        else:
            colors = [self.pick_bullet_color()]

        bullets = []
        for color in colors:
            bullet = BULLET_MAP[color](x=self._col, y=self._row, target=target)
            bullet.is_used = False
            bullets.append(bullet)

        return bullets
    
    def upgrade(self):
        if not self._upgraded:
            self._upgraded = True
            return True
        return False

# phase 2 tower: shoots upwards, cost 5	
class RainbowTower(Tower): 
    _exp_cost = 5
    _upgrade_cost = 5
    _range = 5.0
    _bullet_colors = [Color.Orange, Color.Red, Color.Blue]

    def __init__(self, pos_col, pos_row):
        super().__init__(pos_col, pos_row)