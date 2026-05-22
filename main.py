from model import (Phase1Model)
from view import View
from controller import Controller
import pyxel

if __name__ == '__main__':
    model = Phase1Model()
    view = View()


    controller = Controller(model, view) 

    controller.start_game()