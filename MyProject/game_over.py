import game_framework
from pico2d import *
import main_state
import title_state
import game_world

name = "status scene"
image = None


def enter():
    global image
    global font
    global skull
    image = load_image('chrome.png')
    skull = load_image('warriorLR.png')
    font = load_font('fonts.ttf')


def exit():
    global image
    del (image)


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        else:
            if event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
                game_framework.change_state(title_state)



def draw():
    clear_canvas()
    for game_objects in game_world.all_objects():
        game_objects.draw()
    image.clip_draw_to_origin(30, 0, 34, 32, 0, 150, 300, 300)
    skull.clip_draw_to_origin(96, 15, 60, 15, 90, 330, 150, 37)
    font.draw(80, 405, 'YOU ARE DEAD!', (0, 0, 0))
    font.draw(80, 310, 'Level : %3d' % main_state.warrior.lvl, (0, 0, 0))
    font.draw(80, 290, 'SCORE : %3d' % main_state.warrior.score, (0, 0, 0))
    font.draw(75, 250, '    ESC TO TITLE', (0, 0, 0))
    update_canvas()


def update():
    pass


def pause():
    pass


def resume():
    pass
