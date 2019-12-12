import random
import json
import os

from pico2d import *

import random

import floorTrigger
import game_world
import game_framework
import title_state
import status_pause
from warrior import Warrior
import map
from monster import Monster
from boss import BossMonster
from item import Item
from floorTrigger import FloorTrigger

name = "MainState"

TILE_SIZE = 32

maps = None
warrior = None
monsters = None
font = None
UI = None
HP_BAR = None
hpPercent = None
once = None
charImage = None
bgm = None
font = None
items = None
floorTriggers = None


def collide(a, b):
    left_a, bottom_a, right_a, top_a = a.get_bb()
    left_b, bottom_b, right_b, top_b = b.get_bb()

    if left_a > right_b: return False
    if right_a < left_b: return False
    if top_a < bottom_b: return False
    if bottom_a > top_b: return False

    return True


# 6, 18

def enter():
    game_world.clear()
    global UI
    global HP_BAR
    UI = load_image('Images//status_pane.png')
    HP_BAR = load_image('Images//hp_bar.png')
    global charImage
    charImage = load_image('Images//warriorLR.png')
    global font
    font = load_image('Images//font2x.png')

    global eatSound
    eatSound = load_wav('Sounds//snd_item.wav')
    global lvlUpSound
    lvlUpSound = load_wav('Sounds//snd_levelup.wav')
    lvlUpSound.set_volume(64)
    global bgm
    bgm = load_music('Sounds//game.mp3')
    bgm.set_volume(128)
    bgm.repeat_play()

    global maps
    maps = map.Map(1)
    game_world.add_object(maps, 0)
    global floorTriggers
    floorTriggers = floorTrigger.FloorTrigger(18 * 32, 6 * 32)
    floorTriggers.set_background(maps)
    game_world.add_object(floorTriggers, 1)

    global monsters
    monsters = []
    # monster = Monster(176, 240)
    # monster2 = Monster(240, 240)  # spawn in 240, 240
    n = 0
    while n < 12:
        t = random.randint(0, 1)
        mx = random.randint(0, map.tileX - 1)
        my = random.randint(0, map.tileY - 1)
        if map.map1[my][mx] == 2:
            n += 1
            if t == 0:
                monsters.append(Monster(mx * 32 + 16, my * 32 + 16))
    game_world.add_objects(monsters, 1)

    global items
    items = []
    game_world.add_objects(items, 1)

    # game_world.add_object(monster, 1)
    # game_world.add_object(monster2, 1)

    global warrior
    warrior = Warrior()
    game_world.add_object(warrior, 1)

    global once
    once = Once()

    maps.set_center_object(warrior)
    warrior.set_background(maps)
    for monster in monsters:
        monster.set_background(maps)


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
        elif event.type == SDL_KEYDOWN and event.key == SDLK_p:
            game_framework.push_state(status_pause)
        else:
            warrior.handle_event(event)


def update():
    for game_objects in game_world.all_objects():
        game_objects.update()

    global floorTriggers
    if floorTriggers is not None:
        if collide(floorTriggers, warrior):
            print('go to next stage')
            global maps
            global items
            global monsters
            warrior.x, warrior.y = TILE_SIZE * 2, 16 + TILE_SIZE * 12
            game_world.remove_object(maps)
            maps = map.Map(2)
            game_world.add_object(maps, 0)
            maps.set_center_object(warrior)
            warrior.set_background(maps)
            boss = BossMonster(TILE_SIZE * 16, 16 + TILE_SIZE * 12)
            boss.set_background(maps)
            game_world.add_object(boss, 0)
            for item in items:
                game_world.remove_object(item)
            for monster in monsters:
                game_world.remove_object(monster)
            game_world.remove_object(floorTriggers)

    if items is not None:
        for item in items:
            if collide(item, warrior):
                eatSound.play(1)
                print("collide")
                game_world.remove_object(item)
                items.remove(item)
                if item.var == 1:
                    warrior.hp += clamp(10, warrior.maxHp // 5, 999)
                elif item.var == 2:
                    warrior.atkDamage += 5
                elif item.var == 3:
                    warrior.maxHp += 10
                    warrior.hp += 10

    for game_object in game_world.all_objects():
        if game_object.hp <= 0:
            game_object.isDead = True
            if once.call == 0:
                once.print(game_object.type)
                once.call = 1

    global hpPercent
    hpPercent = int(50 * warrior.hpPercent)


def get_warrior():
    return warrior


def draw():
    clear_canvas()
    for game_objects in game_world.all_objects():
        game_objects.draw()
    UI.clip_draw(0, 0, 128, 64, 160, 498, 320, 160)
    HP_BAR.clip_draw_to_origin(0, 0, hpPercent, 4, 75, 559, hpPercent * 2.5, 10)
    charImage.clip_draw(0, 15, 12, 15, 36, 540, 30, 37)

    if warrior.lvl == 1:
        font.clip_draw(117, 0, 6, 16, 69, 505)
    else:
        font.clip_draw(105 + (warrior.lvl * 9), 0, 9, 16, 69, 505)

    update_canvas()


def make_item(x, y):
    luck = random.randint(1, 15)
    if luck > 11:
        this_item = Item(x, y, 1)
        this_item.set_background(maps)
        items.append(this_item)
        game_world.add_object(this_item, 1)
    elif 0 < luck < 4:
        this_item = Item(x, y, 2)
        this_item.set_background(maps)
        items.append(this_item)
        game_world.add_object(this_item, 1)
    elif 4 < luck < 8:
        this_item = Item(x, y, 3)
        this_item.set_background(maps)
        items.append(this_item)
        game_world.add_object(this_item, 1)
    else:
        print("bad luck!")


def lvl_up():
    warrior.exp += 1
    warrior.score += 5
    if warrior.exp == warrior.lvl:
        lvlUpSound.play(1)
        warrior.lvl += 1
        warrior.maxHp += 10
        warrior.hp += 10
        warrior.exp = 0


class Once:
    def __init__(self):
        self.call = 0

    def print(self, atype):
        print(atype, 'is dead!')
