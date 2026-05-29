from __future__ import annotations
from abc import ABC, abstractmethod
from collections.abc import Sequence
from random import Random, choice
import pyxel
from typing import Protocol
from enum import Enum, auto
from enemies import Color
from random import choice
import json

from towers import Tower
from enemies import Enemy, OrangeEnemy, RedEnemy, BlueEnemy
from bullets import Bullet, OrangeBullet, RedBullet, BlueBullet
from player import Dir

class Phase1Model(ABC):
    def __init__(self, width: int = 1080, height: int = 720):
        self._width: int = width
        self._height: int = height
        self._is_game_over = False
        self._dimensions = (15, 7) # (cols, rows)
        cols, rows  = self._dimensions
        self._cell_size = self._width // cols
        self._total_grid_height = rows * self._cell_size
        self._path = [(3, i) for i in range(14)]
        self._start_row = self._path[0][0]
        self._start_col = self._path[0][1]
        self._rounds = 2
        self._enemies = [[OrangeEnemy() for _ in range(5)] for _ in range(self._rounds)]
        self._current_round = 1
        self._waiting_for_start = True # start in waiting before round 1 starts

        self._displayed_enemies = []
        self._tick = 0
        self._gun_coords = (7, 5) # gun position (col, row)

        self._pending_bullets = [choice([OrangeBullet(), RedBullet(), BlueBullet()])] # always needs a bullet in the pending list to refer the next color sa cursor
        
        self._displayed_bullets = []
        self._next_color = 7
        self._exp = 0
        self._hp = 2

        self._data = self.fetch_json_data()

        self._tower_locs: list[Tower] = []
        
    @property
    def width(self):
        return self._width
    
    @property
    def height(self):
        return self._height
    
    @property
    def is_game_over(self) -> bool:
        return self._is_game_over

    @property
    def dimensions(self) -> bool:
        return self._dimensions

    @property
    def cell_size(self):
        return self._cell_size

    @property
    def total_grid_height(self):
        return self._total_grid_height
    
    @property
    def next_color(self):
        return self._next_color

    @property
    def path(self) -> bool:
        return self._path

    @property
    def enemies(self):
        return self._enemies

    @property
    def displayed_enemies(self):
        return self._displayed_enemies

    @property
    def gun_coords(self) -> bool:
        return self._gun_coords

    @property
    def tick(self):
        return self._tick
    
    @property
    def pending_bullets(self):
        return self._pending_bullets
    
    @property
    def displayed_bullets(self):
        return self._displayed_bullets

    @property
    def gun_coords(self):
        return self._gun_coords
    
    @property
    def exp(self):
        return self._exp
    
    @property
    def hp(self):
        return self._hp
    
    @property
    def allowed_dirs(self):
        return [Dir.UP]

    @property
    def current_round(self):
        return self._current_round
    
    @property
    def rounds(self):
        return self._rounds
    
    @property
    def waiting_for_start(self):
        return self._waiting_for_start
    
    @property 
    def towers_locs(self):
        return self._tower_locs
    
    def place_tower(self, tower: Tower, col, row):
        # 
        if (row, col) in self._path:
            # that location is the path
            return
        if any(tower.col == col and tower.row == row for tower in self._tower_locs):
            # tower already exists in that location
            return
        if self._exp < tower.exp_cost:
            self._exp -= tower.exp_cost
            self.towers_locs.append(tower)
    
    def start_round(self):
        self._waiting_for_start = False

    def inc_tick(self):
        self._tick += 1

    def will_quit(self):
        if pyxel.btn(pyxel.KEY_Q):
            pyxel.quit()

    def check_is_game_over(self):
        if self._hp <= 0:
            self._is_game_over = True

    def check_if_next_round(self):
        if (len(self._enemies[self._current_round - 1]) == 0) and (len(self._displayed_enemies) == 0) and ((self._current_round) < self._rounds):
                self._current_round += 1
                self._waiting_for_start = True # pause between rounds

    def display_next_enemy(self):
        if (self._tick%50 == 0) and (len(self._enemies[self._current_round - 1]) != 0):
            self._displayed_enemies.append(self._enemies[self._current_round - 1].pop())
            
    def move_enemy(self, enemy: Enemy):
        path = self._path

        enemy.progress += enemy.walk_speed 
            # progress : whole num is yung index ng current grid
            #            decimal num is yung percentage ng grid length to cover before going to the next grid
            #            e.g. lets say nasa 4th indexed grid coord na yung enemy, then nasa gitna sya ng grid, then progress = 4.5 since 50% pa need icover bago pumunta sa next grid
        
        current_path_idx = int(enemy.progress)
        next_path_idx = current_path_idx + 1

        if next_path_idx >= len(path): # if nakalagpas na yung enemy, -1 hp
            if enemy.current_health > 0:
                enemy.current_health = 0
                self._hp -= 1
            return

        # percent until next path (ex. from idx 0 to 1, 0.5 yung progress, so meaning halfway pa lang sya to the next)
        percent = enemy.progress - current_path_idx

        p1 = path[current_path_idx]
        p2 = path[next_path_idx]

        # update row and col
        enemy.row = p1[0] + (p2[0] - p1[0]) * percent
        enemy.col = p1[1] + (p2[1] - p1[1]) * percent

    def delete_enemy_out_of_bounds(self):
        self._displayed_enemies = [e for e in self._displayed_enemies if e.current_health > 0]
        self._displayed_bullets = [b for b in self._displayed_bullets if not b.is_used]
    
    # * Must check if a bug may occur in process_shot
    # Implement spatial hash
    def process_shot(self):
        """
        Checks the list of displayed bullets and displayed enemies if there exists
        a pair that intersects. If there is an intersection, it updates the attribute
        `is_used` of the bullet. And updates the `current_health` attribute of the enemy
        by decrementing it by 1. Finally, since it intersects it increases the `exp`
        attribute by 1.
        """
        if self._pending_bullets:
            self._next_color = self.pending_bullets[-1].color.value
        else:
            self._next_color = Color.Black.value

        for bullet in self._displayed_bullets:
            b_col = bullet.col
            b_row = bullet.row

            # bullet radius in pixels
            r1 = bullet.radius / self.cell_size 

            for enemy in self._displayed_enemies:
                e_col = enemy.col
                e_row = enemy.row

                # enemy radius in pixels
                r2 = enemy.radius / self.cell_size 
                
                if (((b_col - e_col)**2 + (b_row - e_row)**2) <= (r1 + r2)**2) and (bullet.color == enemy.color):
                    bullet.is_used = True
                    enemy.current_health -= 1
                    
                    self._exp += 1
                    return True
        return False

    def shoot(self, dir: Dir):
        """
        Shoots the first element in `_pending_bullets` and then appends a new 
        bullet to the list through `random.choice()`. The shot bullet's direction
        is updated through the input parameter `dir`. Afterwards, the bullet is
        appended to the `_displayed_bullets` list.
        """
        if self._pending_bullets:
            bullet = self._pending_bullets.pop()
            self._pending_bullets.append(choice([OrangeBullet(), RedBullet(), BlueBullet()]))
            bullet.direction = dir

            # ! Refactor this code and make it change thru `x` and `y` attribs
            bullet.col = self._gun_coords[0]
            bullet.row = self._gun_coords[1]
            self._displayed_bullets.append(bullet)

    def move_bullet(self):
        """
        Updates the coordinate of the bullet based on its coordinates.
        """
        for bullet in self._displayed_bullets:
            if not bullet.is_used:

                bullet.row -= 0.2
                if bullet.row < -1:
                    bullet.is_used = True

    def fetch_json_data(self):
        with open("settings.json", 'r') as file:
            data = json.load(file)

        return data


# TODO: Add tower feature and get details from setting.json
class Phase2Model(Phase1Model):
    def __init__(self):
        super().__init__()
        self._path = [
            (5, 0), (5, 1), (5, 2), (5, 3), (5, 4), (5, 5), (5, 6), (5, 7), (5, 8), (5, 9), (5, 10), (5, 11), (5, 12), (5, 13),
            (4, 13), (3, 13), (3, 12), (3, 11), (3, 10), (3, 9), (3, 8), (3, 7), (3, 6), (3, 5), (3, 4), (3, 3), (3, 2), (3, 1),
            (2, 1), (1, 1), (1, 2), (1, 3), (1, 4), (1, 5), (1, 6), (1, 7), (1, 8), (1, 9), (1, 10), (1, 11), (1, 12), (1, 13), (1, 14)]
        self._gun_coords = (7, 4)
        self._rounds = self._data["enemies"]
        self._enemies = [
            [(choice([OrangeEnemy(), RedEnemy()])) for _ in range(5)] for _ in range(self.rounds)]
        self._hp = self._data["lives"]

    @property
    def allowed_dirs(self):
        return [Dir.UP, Dir.DOWN, Dir.LEFT, Dir.RIGHT]

    def upgrade_tower(self, tower: Tower): # temp: until a phase 3 model is made since no tower upgrades in phase 2
        if self._exp >= tower._upgrade_cost and not tower.upgraded:
            self._exp -= tower._upgrade_cost
            tower.upgrade()

    def move_bullet(self):
        for bullet in self._displayed_bullets:
            if not bullet.is_used:

                match bullet.direction:
                    case Dir.UP:
                        bullet.row -= 0.2
                        if bullet.row < -1:
                            bullet.is_used = True
                    case Dir.DOWN:
                        bullet.row += 0.2
                        if self._dimensions[1] < bullet.row: # out-of-bounds
                            bullet.is_used = True
                    case Dir.LEFT:
                        bullet.col -= 0.2
                        if bullet.col < -1:
                            bullet.is_used = True
                    case Dir.RIGHT:
                        bullet.col += 0.2
                        if self._width < bullet.row:
                            bullet.is_used = True
