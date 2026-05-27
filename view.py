from collections.abc import Sequence
from typing import Protocol
import pyxel
from random import randint
from enum import Enum
from enemies import Color, Enemy, OrangeEnemy, RedEnemy, BlueEnemy
from bullets import Bullet
from model import Dir

class View:
    def start_game(self, width, height) -> None:
        pyxel.init(width, height, title="zuma")
        pyxel.mouse(False)
        #pyxel.load("...")

    def display_map(self, height, total_grid_height, row_count, col_count, grid_size):
        # para centered
        vert_offset = (height - total_grid_height) // 2

        for r in range(row_count):
            for c in range(col_count):
                # grid coor to pixel
                x = c * grid_size
                y = vert_offset + (r * grid_size)
                
                color = 10 if (r + c) % 2 == 0 else 11
                pyxel.rect(x, y, grid_size, grid_size, color)

    def display_path(self, height, total_grid_height, row_count, col_count, grid_size, path_cells):
        # para centered
        vert_offset = (height - total_grid_height) // 2

        for r, c in path_cells:
            x = c * grid_size
            y = vert_offset + (r * grid_size)
            
            pyxel.rect(x, y, grid_size, grid_size, 7)

    def display_enemies(self, height, total_grid_height, row_count, col_count, grid_size, enemies: list[Enemy]):
        # para centered
        vert_offset = (height - total_grid_height) // 2

        if enemies:
            for enemy in enemies:
                if enemy.current_health > 0:
                    x = enemy.col * grid_size
                    y = vert_offset + (enemy.row * grid_size)

                    mid_x = x + (grid_size//2)
                    mid_y = y + (grid_size//2)
                    pyxel.circ(mid_x, mid_y, grid_size // 3, enemy.color.value)

    def is_left_clicked(self):
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            return Dir.UP
        return None

    def is_gun_wasd_clicked(self, allowed_dirs):
        if (Dir.UP in allowed_dirs) and (pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) or pyxel.btnp(pyxel.KEY_W)):
            return Dir.UP
        if (Dir.DOWN in allowed_dirs) and pyxel.btnp(pyxel.KEY_S):
            return Dir.DOWN
        if (Dir.LEFT in allowed_dirs) and pyxel.btnp(pyxel.KEY_A):
            return Dir.LEFT
        if (Dir.RIGHT in allowed_dirs) and pyxel.btnp(pyxel.KEY_D):
            return Dir.RIGHT
        
        return None

    def display_bullets(self, height, total_grid_height, row_count, 
                        col_count, grid_size, bullets: list[Bullet]):
        # para centered
        vert_offset = (height - total_grid_height) // 2

        for bullet in bullets:
            if not bullet.is_used:
                x = bullet.col * grid_size
                y = vert_offset + (bullet.row * grid_size)

                mid_x = x + (grid_size//2)
                mid_y = y + (grid_size//2)

                pyxel.circ(mid_x, mid_y, grid_size // 5, bullet.color.value)

    def display_gun(self, height, total_grid_height, grid_size, gun_col, gun_row):
        vert_offset = (height - total_grid_height) // 2

        x = gun_col * grid_size
        y = vert_offset + (gun_row * grid_size)

        mid_x = x + (grid_size//2)
        mid_y = y + (grid_size//2)

        pyxel.circ(mid_x, mid_y, grid_size // 4, 0)

    def display_text(self, current_round, rounds, hp, exp, font_addrss, size):
        font = pyxel.Font(font_addrss, size)
        pyxel.text(50, 20, f"ROUND: {current_round}/{rounds}", 7, font)
        pyxel.text(250, 20, f"Health: {hp}", 7, font)
        pyxel.text(450, 20, f"EXP: {exp}", 7, font)

    def display_cursor(self, next_color):
        x = pyxel.mouse_x
        y = pyxel.mouse_y

        pyxel.circ(x, y, 5, next_color)
        pyxel.circb(x, y, 5, 7)

    def reset_screen(self) -> None:
        pyxel.cls(pyxel.COLOR_BLACK)

