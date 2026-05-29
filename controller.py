from model import (Phase1Model, Phase2Model)
from player import Dir
from view import View
import pyxel
import sounds

class Controller:
    def __init__(self, model: Phase1Model, view: View):
        self._model = model
        self._view = view

    def update(self):
        model = self._model
        view = self._view

        # Quits if 'q' is pressed
        model.will_quit()
        if model.waiting_for_start:
            if view.is_start_pressed(model.width, model.height):
                model.start_round()
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

        if model.waiting_for_start:
            view.display_start_button(model.width, model.height, model.current_round)

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

        view.display_bullets(
            model.height, 
            model.total_grid_height, 
            model.dimensions[1], 
            model.dimensions[0], 
            model.cell_size, 
            model.displayed_bullets)

        view.display_gun(
            model.height, 
            model.total_grid_height, 
            model.cell_size, 
            model.gun_coords[0], 
            model.gun_coords[1])

        view.display_text(
            model.current_round, 
            model.rounds, 
            model.hp, 
            model.exp, 
            "UbuntuMono-Regular.ttf", 
            25)
        
        view.display_cursor(model.next_color)

    def start_game(self):
        model = self._model
        view = self._view

        view.start_game(model.width, model.height)
        pyxel.run(self.update, self.draw)
