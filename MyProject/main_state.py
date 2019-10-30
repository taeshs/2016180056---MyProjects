import random
import json
import os

from pico2d import *

import game_framework
import title_state
from warrior import Warrior
from map import Map
from monster import Monster

name = "MainState"

map = None
warrior = None
monster = None
font = None


def enter():
    global warrior
    global map
    global monster
    monster = Monster()
    map = Map()
    warrior = Warrior()


def exit():
    global warrior
    del warrior
    global monster
    del monster
    global map
    del map


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
    monster.update()


def draw():
    clear_canvas()
    map.draw()
    monster.draw()
    warrior.draw()
    update_canvas()
