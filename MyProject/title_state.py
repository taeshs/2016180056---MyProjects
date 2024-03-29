import random
import json
import os

from pico2d import *

import game_framework
import main_state
import map
import how_to_play


name = "TiltleState"
banner = None
titlecnt = (map.windsizX // (map.fixsize * 2)) * (map.windsizY / (map.fixsize * 2))

def enter():
    global banner
    global tile
    global play
    global font
    banner = load_image('Images//banners.png')
    tile = load_image('Images//tiles0.png')
    play = load_image('Images//play.png')
    font = load_font('fonts.ttf')


def exit():
    global banner
    del banner
    global tile
    del tile
    global play
    del play


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
            elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_h):
                print("변경")
                game_framework.push_state(how_to_play)


def update():
    pass


def draw():
    global banner
    global tile
    global play
    clear_canvas()
    for n in range(50):
        if n % 2 == 0 :
            tile.clip_draw(16, 48, 16, 16,
                           map.fixsize + (map.fixsize * 2) * (n % (map.windsizX / (map.fixsize * 2))),
                           map.fixsize + (map.fixsize * 2) * (n // (map.windsizX / (map.fixsize * 2))),
                           map.fixsize * 2, map.fixsize * 2)
        else :
            tile.clip_draw(144, 16, 16, 16,
                           map.fixsize + (map.fixsize * 2) * (n % (map.windsizX / (map.fixsize * 2))),
                           map.fixsize + (map.fixsize * 2) * (n // (map.windsizX / (map.fixsize * 2))),
                           map.fixsize * 2, map.fixsize * 2)
    banner.clip_draw(0, 192, 128, 64, map.windsizX / 2, map.windsizY / 3 * 2, 256, 128)
    play.clip_draw(0, 0, 107, 133, map.windsizX / 2, map.windsizY / 3 * 1, 107, 133)
    font.draw(130, 180, 'SPACE', (255, 255, 255))
    font.draw(100, 90, 'HOW TO PLAY : H', (255, 255, 255))
    update_canvas()

# 16 * (n % 10) , 16 * (n / 10)



# 10 * 15
