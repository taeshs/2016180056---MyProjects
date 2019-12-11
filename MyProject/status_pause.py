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
    image = load_image('chrome.png')
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
            elif event.type == SDL_KEYDOWN and event.key == SDLK_p:
                game_framework.pop_state()


def draw():
    clear_canvas()
    for game_objects in game_world.all_objects():
        game_objects.draw()
    image.clip_draw_to_origin(30, 0, 34, 32, 0, 150, 300, 300)
    font.draw(80, 350, 'HP : %3d' % main_state.warrior.hp, (0, 0, 0))
    font.draw(80, 330, 'MAXHP : %3d' % main_state.warrior.maxHp, (0, 0, 0))
    font.draw(80, 310, 'DAMAGE : %3d' % main_state.warrior.atkDamage, (0, 0, 0))
    update_canvas()


def update():
    pass


def pause():
    pass


def resume():
    pass
