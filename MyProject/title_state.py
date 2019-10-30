import random
import json
import os

from pico2d import *

import game_framework
import main_state


name = "TiltleState"
banner = None


def enter():
    global banner
    global tile
    banner = load_image('banners.png')
    tile = load_image('tiles0.png')


def exit():
    global banner
    del banner
    global tile
    del tile


def pause():
    pass


def resume():
    pass


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        else:
            if (event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
                print("종료")
                game_framework.quit()
            elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_SPACE):
                print("변경")
                game_framework.change_state(main_state)


def update():
    pass


def draw():
    global banner
    global tile
    clear_canvas()
    for n in range(600):
        tile.clip_draw(16, 48, 16, 16, 20 + 40 * (n % 10), 20 + 40 * (n // 10), 40, 40)
    banner.clip_draw(0, 192, 128, 64, 200, 400, 256, 128)

    update_canvas()

# 16 * (n % 10) , 16 * (n / 10)



# 10 * 15
