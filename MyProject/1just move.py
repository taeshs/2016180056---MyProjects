from pico2d import *


def handle_events():
    global running
    global dir
    global stat
    global cnt
    global tx, ty

    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN:
            cnt = 0
            if event.key == SDLK_ESCAPE:
                running = False
            elif event.key == SDLK_LEFT:
                if tx > 0:
                    tx -= 50
                dir = 0
                stat = 0
            elif event.key == SDLK_RIGHT:
                if tx < 800:
                    tx += 50
                dir = 1
                stat = 1
            elif event.key == SDLK_UP:
                if ty < 600:
                    ty += 50
                stat = 2
            elif event.key == SDLK_DOWN:
                if ty > 0:
                    ty -= 50
                stat = 3
            elif event.key == SDLK_SPACE:
                stat = 4


open_canvas(400, 600)
character = load_image('warriorLR.png')
map = load_image('tiles0.png')

running = True
tx, x = 0, 0
ty, y = 0, 0
cnt = 0
frame = 2
stat = 0
dir = 0
pos = 0
poz = 0

while running:
    clear_canvas()
    map.clip_draw(16, 16, 16, 16, tx, ty, 48, 48)
    character.clip_draw(poz, pos, 12, 15, x, y, 36, 45)
    update_canvas()
    frame = (frame + 1)
    if frame == 8:
        frame = 2
    handle_events()
    if stat == 1:
        if x < 800:
            pos = dir * 15
            poz = frame * 12
            if cnt < 10:
                x += 5
                cnt += 1
            else:
                stat = 4
        elif x == 800:
            poz = 0
    elif stat == 0:
        if x > 0:
            pos = dir * 15
            poz = frame * 12
            if cnt < 10:
                x -= 5
                cnt += 1
            else:
                stat = 4
        elif x == 0:
            poz = 0
    elif stat == 3:
        if y > 0:
            pos = dir * 15
            poz = frame * 12
            if cnt < 10:
                y -= 5
                cnt += 1
            else:
                stat = 4
        elif y == 0:
            poz = 0
    elif stat == 2:
        if y < 600:
            pos = dir * 15
            poz = frame * 12
            if cnt < 10:
                y += 5
                cnt += 1
            else:
                stat = 4
        elif y == 600:
            poz = 0
    elif stat == 4:
        poz = 0
    delay(0.02)

close_canvas()
