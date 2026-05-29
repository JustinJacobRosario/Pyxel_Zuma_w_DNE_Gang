from collections.abc import Sequence
from typing import List, Protocol
import pyxel
from random import randint
from enum import Enum

from enemies import Color, Enemy, OrangeEnemy, RedEnemy, BlueEnemy
from bullets import Bullet
from towers import Tower
from player import Dir
import sounds

class View:
    def __init__(self) -> None:
        ...
        
    def start_game(self, width, height) -> None:
        pyxel.init(width, height, title="zuma", fps=30)
        pyxel.mouse(False)
        pyxel.load("tilemap_sprites.pyxres")
        sounds.play_music()

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
            x = int(tower.col * cell_size)
            y = vert_offset + int(tower.row * cell_size)

            pyxel.rect(x, y, cell_size, cell_size, 10) # temp while we dont have tower sprites

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

        pyxel.circ(x, y, 10, next_color)
        pyxel.circb(x, y, 10, 7)

    def reset_screen(self) -> None:
        pyxel.cls(pyxel.COLOR_BLACK)

    def draw_tilemap(self, height, total_grid_height, row_count, col_count, cell_size):
            # same vert_offset
            vert_offset = (height - total_grid_height) // 2
    
            tile_side_length = 16          # tile pixel side length
            tile_scale = cell_size // tile_side_length + 1  # since cell_size is 72 and tile_side_length is 16, it will be 5x bigger
    
            # Calculate the offset to counteract the center-based scaling of blt()
            offset = (cell_size - tile_side_length) // 2
    
            for r in range(row_count):
                for c in range(col_count):
                    # Topleft corner of each cell
                    tl_x = c * cell_size
                    tl_y = vert_offset + (r * cell_size)
    
                    # tile_coord from pyxel editor
                    tile_x, tile_y = pyxel.tilemap(0).pget(c * 2, r * 2)
    
                    # convert to pixel coords in the image bank
                    u = tile_x * 8
                    v = tile_y * 8
    
                    pyxel.blt(tl_x + offset, tl_y + offset, 0, u, v, tile_side_length, tile_side_length, scale=tile_scale)

    def display_border_panels(self, height, total_grid_height):
        vert_offset = (height - total_grid_height) // 2  + 45
        tile_side = 16
        scale = 7  # bigger tiless

        u, v = 32, 48  # sprite coords

        tiles_needed = (1080 // (tile_side * scale)) + 2

        for i in range(tiles_needed):
            x = i * tile_side * scale

            # top line
            pyxel.blt(x, 0 + 45, 0, u, v, tile_side, tile_side, scale=scale)

            # bottom line
            pyxel.blt(x, vert_offset + total_grid_height, 0, u, v, tile_side, tile_side, scale=scale)