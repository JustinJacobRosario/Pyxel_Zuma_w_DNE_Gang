from collections.abc import Sequence
from typing import Protocol
import pyxel
from random import randint
from enum import Enum
from enemies import Color, Enemy, OrangeEnemy, RedEnemy, BlueEnemy
from bullets import Bullet
from model import Dir
from towers import Tower

class View:
    def start_game(self, width, height) -> None:
        pyxel.init(width, height, title="zuma", fps=30)
        pyxel.mouse(False)
        #pyxel.load("...")

    # ? Can we reduce the parameters here
    def display_map(self, height, total_grid_height, row_count, 
                    col_count, cell_size):
        # para centered
        vert_offset = (height - total_grid_height) // 2

        for r in range(row_count):
            for c in range(col_count):
                # grid coor to pixel
                x = c * cell_size
                y = vert_offset + (r * cell_size)
                
                color = 10 if (r + c) % 2 == 0 else 11
                pyxel.rect(x, y, cell_size, cell_size, color)

    # ? Can we reduce the parameters here
    def display_path(self, height, total_grid_height, row_count, 
                     col_count, cell_size, path_cells):
        # para centered
        vert_offset = (height - total_grid_height) // 2

        for r, c in path_cells:
            x = c * cell_size
            y = vert_offset + (r * cell_size)
            
            pyxel.rect(x, y, cell_size, cell_size, 7)

    # ? Can we reduce the parameters here
    def display_enemies(self, height, total_grid_height, row_count, 
                        col_count, cell_size, enemies: list[Enemy]):
        # para centered
        vert_offset = (height - total_grid_height) // 2

        if enemies:
            for enemy in enemies:
                if enemy.current_health > 0:
                    x = enemy.col * cell_size
                    y = vert_offset + (enemy.row * cell_size)

                    mid_x = x + (cell_size//2)
                    mid_y = y + (cell_size//2)
                    pyxel.circ(mid_x, mid_y, cell_size // 3, enemy.color.value)

    def is_left_clicked(self):
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            return Dir.UP
        return None

    def is_gun_wasd_clicked(self):
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) or pyxel.btnp(pyxel.KEY_W):
            return Dir.UP
        elif pyxel.btnp(pyxel.KEY_S):
            return Dir.DOWN
        elif pyxel.btnp(pyxel.KEY_A):
            return Dir.LEFT
        elif pyxel.btnp(pyxel.KEY_D):
            return Dir.RIGHT
        
        return None

    def display_bullets(self, height, total_grid_height, row_count, 
                        col_count, cell_size, bullets: list[Bullet]):
        # para centered
        vert_offset = (height - total_grid_height) // 2

        for bullet in bullets:
            if not bullet.is_used:
                x = bullet.col * cell_size
                y = vert_offset + (bullet.row * cell_size)

                mid_x = x + (cell_size//2)
                mid_y = y + (cell_size//2)

                pyxel.circ(mid_x, mid_y, cell_size // 5, bullet.color.value)

    def display_gun(self, height, total_grid_height, cell_size, gun_col, gun_row):
        vert_offset = (height - total_grid_height) // 2

        x = gun_col * cell_size
        y = vert_offset + (gun_row * cell_size)

        mid_x = x + (cell_size//2)
        mid_y = y + (cell_size//2)

        pyxel.circ(mid_x, mid_y, cell_size // 4, 0)

    def display_text(self, current_round, rounds, hp, exp, font_addrss, size):
        font = pyxel.Font(font_addrss, size)
        pyxel.text(50, 20, f"ROUND: {current_round}/{rounds}", 7, font)
        pyxel.text(250, 20, f"Health: {hp}", 7, font)
        pyxel.text(450, 20, f"EXP: {exp}", 7, font)

    def display_start_button(self, width, height, current_round):
        btn_w, btn_h = 150, 50
        x = width - btn_w - 25
        y = height - btn_h - 40

        pyxel.rect(x, y, btn_w, btn_h, 7)
        pyxel.text(x + 15, y + 11, f"PRESS SPACE TO START ROUND {current_round}", 0)

    def display_placed_towers(self, height, total_grid_height, cell_size, towers: list[Tower]):
        vert_offset = (height - total_grid_height) // 2

        for tower in towers:
            x = tower.col * cell_size
            y = vert_offset + (tower.row * cell_size)

            mid_x = x + (cell_size//2)
            mid_y = y + (cell_size//2)

            pyxel.circ(mid_x, mid_y, cell_size // 4, 12)

    def get_clicked_cell(self, height, total_grid_height, cell_size):
        # use for placing down towers
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            vert_offset = (height - total_grid_height) // 2
            mouse_x, mouse_y = pyxel.mouse_x, pyxel.mouse_y
            col = mouse_x // cell_size
            row = (mouse_y - vert_offset) // cell_size
            return col, row
        return None

    def is_start_pressed(self, width, height):
        return pyxel.btnp(pyxel.KEY_SPACE)

    def display_cursor(self, next_color):
        x = pyxel.mouse_x
        y = pyxel.mouse_y

        pyxel.circ(x, y, 5, next_color)
        pyxel.circb(x, y, 5, 7)

    def reset_screen(self) -> None:
        pyxel.cls(pyxel.COLOR_BLACK)

