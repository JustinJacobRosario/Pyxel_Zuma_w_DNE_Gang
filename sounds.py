import pyxel

def shoot_sound():
    pyxel.play(0, 0)

def shot_enemy_sound():
    pyxel.play(0,1)

def play_music():
    pyxel.playm(0,0, loop=True)

def stop_music():
    pyxel.stop()