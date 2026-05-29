from model import (Phase1Model, Phase2Model)
from player import Dir
from dataclasses import dataclass
from towers import Tower, RainbowTower
from view import View
import pyxel
import sounds

AVAILABLE_TOWERS = [RainbowTower]

@dataclass
class PlacementState:
    selected_tower: type[Tower] | None = None
    def select(self, tower_class):
        if self.selected_tower == tower_class:
            self.selected_tower = None
        else:
            self.selected_tower = tower_class

    def reset(self):
        self.selected_tower = None

class Controller:
    def __init__(self, model: Phase2Model, view: View):
        self._model = model
        self._view = view
        self._tower_placement = PlacementState()

    def update(self):
        model = self._model
        view = self._view

        # Quits if 'q' is pressed
        model.will_quit()

        if model.waiting_for_start:
            if view.is_start_pressed(model.width, model.height):
                model.start_round()
                self._tower_placement.reset()
                return
            
            clicked_tower = view.get_tower_selection(model.width, model.height, AVAILABLE_TOWERS, model.cell_size)
            if clicked_tower:
                self._tower_placement.select(clicked_tower)
            else:
                cell = view.get_clicked_cell(model.height, model.total_grid_height, model.cell_size)
                if cell and self._tower_placement.selected_tower:
                    col, row = cell
                    model.place_tower(self._tower_placement.selected_tower, col, row)
                    self._tower_placement.reset()

            return # freezes rendering of enemies/bullets
        
        else:
            if not self._model.is_game_over:
                model.inc_tick()
                model.move_bullet()
                is_shot = model.process_shot()
                if is_shot:
                    sounds.shot_enemy_sound()


                for enemy in list(model.displayed_enemies):
                    model.move_enemy(enemy)

                model.display_next_enemy()
                wasd_val = view.is_gun_wasd_clicked()

                if wasd_val is not None:
                    sounds.shoot_sound()
                    model.shoot(wasd_val)

            model.delete_enemy_out_of_bounds()
            model.check_if_next_round()
            model.check_is_game_over()

    def draw(self):
        model = self._model
        view = self._view

        view.reset_screen()

        view.display_map(
            model.height, 
            model.total_grid_height, 
            model.dimensions[1], 
            model.dimensions[0], 
            model.cell_size)

        view.display_path(
            model.height, 
            model.total_grid_height, 
            model.dimensions[1], 
            model.dimensions[0], 
            model.cell_size, 
            model.path)
        
        view.draw_tilemap(model.height, model.total_grid_height, model.dimensions[1], model.dimensions[0], model.cell_size)

        view.display_border_panels(model.height, model.total_grid_height)

        view.display_enemies(
            model.height, 
            model.total_grid_height, 
            model.dimensions[1], 
            model.dimensions[0], 
            model.cell_size,
            model.displayed_enemies)

        view.display_gun(
            model.height, 
            model.total_grid_height, 
            model.cell_size, 
            model.gun_coords[0], 
            model.gun_coords[1])

        view.display_bullets(
            model.height, 
            model.total_grid_height, 
            model.dimensions[1], 
            model.dimensions[0], 
            model.cell_size, 
            model.displayed_bullets)


        view.display_text(
            model.current_round, 
            model.rounds, 
            model.hp, 
            model.exp, 
            "UbuntuMono-Regular.ttf", 
            25)
        
        view.display_cursor(model.next_color)

        if model.waiting_for_start:
            view.display_start_button(model.width, model.height, model.current_round)
            view.display_tower_selection(model.width, model.height, AVAILABLE_TOWERS, self._tower_placement.selected_tower, model.cell_size)
        # temp until model implemented
        # view.display_tower_selection(model.width, model.height, AVAILABLE_TOWERS, model.selected_tower, model.cell_size)

    def start_game(self):
        model = self._model
        view = self._view

        view.start_game(model.width, model.height)
        pyxel.run(self.update, self.draw)
