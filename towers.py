from abc import ABC, abstractmethod
from bullets import Bullet
from enemies import Color
from player import Dir
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
        self._fire_cooldown: float = 0.0 # time since last shot
        self._col: float = float(pos_col) # defined per instance
        self._row: float = float(pos_row) # defined per instance
        self._upgraded: bool = False
        self._direction: Dir = Dir.UP
	
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
    def fire_cooldown(self) -> float: # req for shooting cooldown
        return self._fire_cooldown
    
    @fire_cooldown.setter
    def fire_cooldown(self, value: float):
        self._fire_cooldown = value

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
    
    @property
    def direction(self) -> Dir:
        return self._direction
    
    @direction.setter
    def direction(self, value: Dir):
        self._direction = value
    
    # --

    def pick_bullet_color(self) -> list[Color]:
        return [random.choice(self._bullet_colors)]
    
    def on_upgrade(self):
        pass

    #def shoot(self, target) -> list[Bullet]: 
    #    if self.upgraded:
    #        colors = random.sample(self._bullet_colors, 2)
    #    else:
    #        colors = [self.pick_bullet_color()]
#
    #    bullets = []
    #    for color in colors:
    #        bullet = BULLET_MAP[color](x=self._col, y=self._row, target=target)
    #        bullet.is_used = False
    #        bullets.append(bullet)
#
    #    return bullets
    
    def upgrade(self):
        if not self._upgraded:
            self._upgraded = True
            self.on_upgrade()
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

    def pick_bullet_color(self) -> list[Color]:
        if self._upgraded:
            return random.sample(self._bullet_colors, 2)  # 2 bullets only when upgraded
        return [random.choice(self._bullet_colors)]

class SniperTower(Tower):
    _exp_cost = 1 # !TESTING COST ONLY
    _upgrade_cost = 8
    _range = 10.0
    _bullet_colors = [Color.Orange, Color.Red, Color.Blue]

    def __init__(self, pos_col, pos_row):
        super().__init__(pos_col, pos_row)
        self._fire_rate = 0.2


class SplitterTower(Tower):
    _exp_cost = 1 # !TESTING COST ONLY
    _upgrade_cost = 6
    _range = 3.0
    _bullet_colors = [Color.Orange, Color.Red, Color.Blue]

    def __init__(self, pos_col, pos_row):
        super().__init__(pos_col, pos_row)
        self._fire_rate = 0.2

class MedicTower(Tower):
    _exp_cost = 1 # !TESTING COST ONLY
    _upgrade_cost = 10
    _range = 0
    _bullet_colors = []

    def __init__(self, pos_col, pos_row):
        super().__init__(pos_col, pos_row)
        self._fire_rate = 0.0
        self._heal_amount = 1

    @property
    def heal_amount(self):
        return self._heal_amount
    
    def on_upgrade(self):
        self._heal_amount = 2