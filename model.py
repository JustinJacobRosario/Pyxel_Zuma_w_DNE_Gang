from __future__ import annotations
from abc import ABC, abstractmethod
from collections.abc import Sequence
from random import Random, choice
from typing import Protocol
from enum import Enum, auto
import pyxel
from enemies import Enemy, OrangeEnemy, RedEnemy, BlueEnemy
from bullets import Bullet, OrangeBullet, RedBullet, BlueBullet


class Phase1Model:
    def __init__(self, width: int = 1080, height: int = 720):
        self._width: int = width
        self._height: int = height
        self._is_game_over = False
        self._dimensions = (15, 7) # num of cols and rows
        cols,rows  = self._dimensions
        self._grid_size = self._width // cols
        self._total_grid_height = self._dimensions[1] * self._grid_size
        self._path = [
            (3, 0), 
            (3, 1), 
            (3, 2), 
            (3, 3), 
            (3, 4), 
            (3, 5), 
            (3, 6), 
            (3, 7), 
            (3, 8), 
            (3, 9), 
            (3, 10), 
            (3, 11), 
            (3, 12), 
            (3, 13)]
        self._start_row = self._path[0][0]
        self._start_col = self._path[0][1]
        self._enemies = [
            OrangeEnemy(self._start_col, self._start_row, self._grid_size//3),
            RedEnemy(self._start_col, self._start_row, self._grid_size//3), 
            BlueEnemy(self._start_col, self._start_row, self._grid_size//3)]
        self._displayed_enemies = [
            OrangeEnemy(self._start_col, self._start_row, self._grid_size//3)]
        self._tick = 0
        self._gun_coords = (7, 5)
        self._pending_bullets = [
            OrangeBullet(self._gun_coords[0], self._gun_coords[1], self._grid_size//5),
            OrangeBullet(self._gun_coords[0], self._gun_coords[1], self._grid_size//5),
            RedBullet(self._gun_coords[0], self._gun_coords[1], self._grid_size//5),
            BlueBullet(self._gun_coords[0], self._gun_coords[1], self._grid_size//5)]
        self._displayed_bullets = []
        self._next_color = 7
        self._exp = 0
        self._hp = 2
        

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
    def grid_size(self):
        return self._grid_size

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
    


    def inc_tick(self):
        self._tick += 1

    def will_quit(self):
        if pyxel.btn(pyxel.KEY_Q):
            pyxel.quit()

    def check_is_game_over(self):
        if self._hp <= 0:
            self._is_game_over = True

    def display_next_enemy(self):
        if (self._tick%50 == 0) and (len(self._enemies) != 0):
            self._displayed_enemies.append(self._enemies.pop())

    def move_enemy(self, enemy: Enemy):
        path = self._path

        enemy.progress += enemy.walk_speed

        current_path_idx = int(enemy.progress)
        next_path_idx = current_path_idx + 1

        if next_path_idx >= len(path):
            if enemy.current_health > 0:
                enemy.current_health = 0
                self._hp -= 1
            return

        # percent until next path (ex. from idx 0 to 1, 0.5 yung progress, so meaning halfway pa lang sya to the next)
        percent = enemy.progress - current_path_idx

        p1 = path[current_path_idx]
        p2 = path[next_path_idx]

        enemy.y = p1[0] + (p2[0] - p1[0]) * percent
        enemy.x = p1[1] + (p2[1] - p1[1]) * percent

    def process_shot(self):
        self._next_color = self.pending_bullets[-1].color.value


        for bullet in self._displayed_bullets:
            x = bullet.x
            y = bullet.y
            r1 = bullet.radius / self.grid_size

            for enemy in self._displayed_enemies:
                target_x = enemy.x
                target_y = enemy.y
                r2 = enemy.radius / self.grid_size
                
                if (((x-target_x)**2 + (y-target_y)**2) <= (r1 + r2)**2) and (bullet.color == enemy.color):
                    bullet.is_used = True
                    enemy.current_health -= 1
                    
                    self._exp += 1

    def shoot(self):
        if self._pending_bullets:
            self._displayed_bullets.append(self._pending_bullets.pop())

    def move_bullet(self):
        for bullet in self._displayed_bullets:
            if not bullet.is_used:
                bullet.y -= 0.2

                if bullet.y < -1:
                    bullet.is_used = True



