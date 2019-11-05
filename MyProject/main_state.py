import random
import json
import os

from pico2d import *

import game_world
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
    game_world.add_object(monster, 1)
    map = Map()
    game_world.add_object(map, 0)
    warrior = Warrior()
    game_world.add_object(warrior, 1)


def exit():
    game_world.clear()


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
    for game_objects in game_world.all_objects():
        game_objects.update()


def draw():
    clear_canvas()
    for game_objects in game_world.all_objects():
        game_objects.draw()
    update_canvas()
