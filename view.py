from collections.abc import Sequence
from typing import Protocol
import pyxel
from random import randint
from enum import Enum
from enemies import Color, Enemy, OrangeEnemy, RedEnemy, BlueEnemy


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

        for enemy in enemies:

            if enemy.current_health > 0:
                x = enemy.x * grid_size
                y = vert_offset + (enemy.y * grid_size)

                mid_x = x + (grid_size//2)
                mid_y = y + (grid_size//2)
                pyxel.circ(mid_x, mid_y, grid_size // 3, enemy.color.value)

    def is_gun_clicked(self):
        return pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT)

    def display_bullets(self, height, total_grid_height, row_count, col_count, grid_size, bullets: list[Bullet]):
        
        # para centered
        vert_offset = (height - total_grid_height) // 2

        for bullet in bullets:

            if not bullet.is_used:
                x = bullet.x * grid_size
                y = vert_offset + (bullet.y * grid_size)

                mid_x = x + (grid_size//2)
                mid_y = y + (grid_size//2)
                pyxel.circ(mid_x, mid_y, grid_size // 5, bullet.color.value)
    def display_gun(self, height, total_grid_height, grid_size, x, y):
        vert_offset = (height - total_grid_height) // 2

        x = x * grid_size
        y = vert_offset + (y * grid_size)

        mid_x = x + (grid_size//2)
        mid_y = y + (grid_size//2)

        pyxel.circ(mid_x, mid_y, grid_size // 4, 0)

    def display_text(self, hp, exp, font_addrss, size):
        font = pyxel.Font(font_addrss, size)
        pyxel.text(10, 10, f"Health: {hp}", 7, font)
        pyxel.text(10, 35, f"EXP: {exp}", 7, font)


    def display_cursor(self, next_color):
        x = pyxel.mouse_x
        y = pyxel.mouse_y

        pyxel.circ(x, y, 5, next_color)
        pyxel.circb(x, y, 5, 7)

    def reset_screen(self) -> None:
        pyxel.cls(pyxel.COLOR_BLACK)

