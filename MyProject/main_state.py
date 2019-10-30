import random
import json
import os

from pico2d import *

import game_framework
import title_state
from warrior import Warrior

name = "MainState"

warrior = None
font = None


def enter():
    global warrior
    global tile
    tile = load_image('tiles0.png')
    warrior = Warrior()


def exit():
    global warrior
    del warrior
    global tile
    del tile


def pause():
    pass


def resume():
    # draw()
    pass


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.change_state(title_state)
        else:
            warrior.handle_event(event)

def update():
    warrior.update()


def draw():
    clear_canvas()
    for n in range(600):
        tile.clip_draw(16, 48, 16, 16, 20 + 40 * (n % 10), 20 + 40 * (n // 10), 40, 40)
    warrior.draw()
    update_canvas()
