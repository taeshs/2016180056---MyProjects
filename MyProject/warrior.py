from pico2d import *
import map
import main_state
import title_state
import game_framework
import game_world

canvasTileSizeX, canvasTileSizeY = map.canvasTileSizeX, map.canvasTileSizeY
# Boy Event
UP_KEYDOWN, DOWN_KEYDOWN, RIGHT_KEYDOWN, LEFT_KEYDOWN, \
UP_KEYUP, DOWN_KEYUP, RIGHT_KEYUP, LEFT_KEYUP, STOP_MOVING, \
ATK_UP, ATK_DOWN, ATK_RIGHT, ATK_LEFT, ATK_END, SKIP_DOWN, SKIP_UP = range(16)

key_event_table = {
    (SDL_KEYDOWN, SDLK_UP): UP_KEYDOWN,
    (SDL_KEYDOWN, SDLK_DOWN): DOWN_KEYDOWN,
    (SDL_KEYDOWN, SDLK_RIGHT): RIGHT_KEYDOWN,
    (SDL_KEYDOWN, SDLK_LEFT): LEFT_KEYDOWN,
    (SDL_KEYUP, SDLK_UP): UP_KEYUP,
    (SDL_KEYUP, SDLK_DOWN): DOWN_KEYUP,
    (SDL_KEYUP, SDLK_RIGHT): RIGHT_KEYUP,
    (SDL_KEYUP, SDLK_LEFT): LEFT_KEYUP,
    (SDL_KEYDOWN, SDLK_k): SKIP_DOWN,
    (SDL_KEYUP, SDLK_k): SKIP_UP
}

TILE_SIZE = 32

TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 8


# Boy States

class IdleState:
    @staticmethod
    def enter(warrior, event):
        print("idlestate")

        print("warrior : ", (warrior.y - 16) // TILE_SIZE, (warrior.x - 16) // TILE_SIZE,
              warrior.bg.mapli[warrior.tileY][warrior.tileX])
        warrior.timer = 0

    @staticmethod
    def exit(warrior, event):
        pass

    @staticmethod
    def do(warrior):

        warrior.timer = (warrior.timer + 1) % 1000
        if warrior.timer > 800:
            warrior.idl = 1
        else:
            warrior.idl = 0

    @staticmethod
    def draw(warrior):
        warrior.image.clip_draw(warrior.idl * 12, warrior.dir * 15, 12, 15, warrior.cx, warrior.cy, 24, 30)
        # character.clip_draw(poz, pos, 12, 15, x, y, 36, 45)


class MoveState:  # 공격 추가 : 바로 옆칸에 monster 존재 시 and 그쪽 방향키 누를시 move 대신 attack
    @staticmethod
    def enter(warrior, event):
        for game_object in game_world.all_objects():
            if game_object.type == 'mon':
                game_object.turn = 0
        if warrior.moving == 0:
            print("runstate")
            if event == RIGHT_KEYDOWN:
                warrior.dir = 1
                for game_object in game_world.all_objects():
                    if game_object.type == 'mon':
                        check_monster_tileX, check_monster_tileY = game_object.return_loc()
                        if warrior.tileX + 1 == check_monster_tileX and warrior.tileY == check_monster_tileY \
                                and game_object.hp > 0:
                            warrior.atkSt = 1
                            game_object.get_damage(warrior.atkDamage)
                            warrior.add_event(ATK_RIGHT)
                if warrior.atkSt != 1 and warrior.bg.mapli[warrior.tileY][warrior.tileX + 1] == 2:
                    warrior.moveto = 'RIGHT'
                    warrior.cnt = 0
            elif event == LEFT_KEYDOWN:
                warrior.dir = 0
                for game_object in game_world.all_objects():
                    if game_object.type == 'mon':
                        check_monster_tileX, check_monster_tileY = game_object.return_loc()
                        if warrior.tileX - 1 == check_monster_tileX and warrior.tileY == check_monster_tileY \
                                and game_object.hp > 0:
                            warrior.atkSt = 1
                            game_object.get_damage(warrior.atkDamage)
                            warrior.add_event(ATK_LEFT)
                if warrior.atkSt != 1 and warrior.bg.mapli[warrior.tileY][warrior.tileX - 1] == 2:
                    warrior.moveto = 'LEFT'
                    warrior.cnt = 0
            elif event == UP_KEYDOWN:
                for game_object in game_world.all_objects():
                    if game_object.type == 'mon':
                        check_monster_tileX, check_monster_tileY = game_object.return_loc()
                        if warrior.tileX == check_monster_tileX and warrior.tileY + 1 == check_monster_tileY \
                                and game_object.hp > 0:
                            warrior.atkSt = 1
                            game_object.get_damage(warrior.atkDamage)
                            warrior.add_event(ATK_UP)
                if warrior.atkSt != 1 and warrior.bg.mapli[warrior.tileY + 1][warrior.tileX] == 2:
                    warrior.moveto = 'UP'
                    warrior.cnt = 0
            elif event == DOWN_KEYDOWN:
                for game_object in game_world.all_objects():
                    if game_object.type == 'mon':
                        check_monster_tileX, check_monster_tileY = game_object.return_loc()
                        if warrior.tileX == check_monster_tileX and warrior.tileY - 1 == check_monster_tileY \
                                and game_object.hp > 0:
                            warrior.atkSt = 1
                            game_object.get_damage(warrior.atkDamage)
                            warrior.add_event(ATK_DOWN)
                if warrior.atkSt != 1 and warrior.bg.mapli[warrior.tileY - 1][warrior.tileX] == 2:
                    warrior.moveto = 'DOWN'
                    warrior.cnt = 0
            elif event == SKIP_DOWN:
                warrior.add_event(STOP_MOVING)

    @staticmethod
    def exit(warrior, event):
        pass

    @staticmethod
    def do(warrior):
        if warrior.cnt < TILE_SIZE:
            if warrior.moveto == 'RIGHT':
                warrior.x += 1
                warrior.cnt += 1
            elif warrior.moveto == 'LEFT':
                warrior.x -= 1
                warrior.cnt += 1
            elif warrior.moveto == 'UP':
                warrior.y += 1
                warrior.cnt += 1
            elif warrior.moveto == 'DOWN':
                warrior.y -= 1
                warrior.cnt += 1
                # else:
                #   warrior.cnt = 32
            warrior.moving = 1
        else:
            warrior.moving = 0
            for game_object in game_world.all_objects():
                if game_object.type == 'mon':
                    game_object.turn = 1
            warrior.add_event(STOP_MOVING)
        warrior.frame = (warrior.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time)
        if warrior.frame > 8:
            warrior.frame = 2
        # boy.frame = (boy.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % FRAMES_PER_ACTION
        # warrior.x = clamp(25, warrior.x, DISPLAY_SIZE_X - 25)
        # warrior.y = clamp(25, warrior.y, DISPLAY_SIZE_Y - 25)

    @staticmethod
    def draw(warrior):
        if warrior.atkSt == 1:
            print("attack")
            warrior.atkSt = 0
        else:
            warrior.image.clip_draw(int(warrior.frame) * 12, warrior.dir * 15, 12, 15, warrior.cx, warrior.cy, 24, 30)


class AttackState:
    @staticmethod
    def enter(warrior, event):
        warrior.timer = 0
        warrior.frame = 0
        # if event == ATK_UP:

        # if event == ATK_DOWN:

        # if event == ATK_RIGHT:

        # if event == ATK_LEFT:

    @staticmethod
    def exit(warrior, event):
        warrior.atkSt = 0
        warrior.idl = 0
        warrior.frame = 2

    @staticmethod
    def do(warrior):
        if warrior.timer < 30:
            warrior.frame += 1
            warrior.timer += 1
            if warrior.frame < 10:
                warrior.idl = 0
            elif warrior.frame < 20:
                warrior.idl = 1
            else:
                warrior.idl = 2
        else:

            warrior.add_event(ATK_END)

    @staticmethod
    def draw(warrior):  # 13, 14, 15
        warrior.image.clip_draw((warrior.idl + 13) * 12, warrior.dir * 15, 12, 15, warrior.cx, warrior.cy, 24, 30)


next_state_table = {  # 999 -> IGNORE EVENT
    IdleState: {RIGHT_KEYDOWN: MoveState, LEFT_KEYDOWN: MoveState,
                UP_KEYDOWN: MoveState, DOWN_KEYDOWN: MoveState,
                SKIP_UP: 999, SKIP_DOWN: MoveState,
                RIGHT_KEYUP: 999, LEFT_KEYUP: 999,
                UP_KEYUP: 999, DOWN_KEYUP: 999,
                STOP_MOVING: 999, ATK_END: 999
                },
    MoveState: {RIGHT_KEYUP: 999, LEFT_KEYUP: 999,
                UP_KEYUP: 999, DOWN_KEYUP: 999,
                RIGHT_KEYDOWN: 999, LEFT_KEYDOWN: 999,
                UP_KEYDOWN: 999, DOWN_KEYDOWN: 999,
                STOP_MOVING: IdleState,
                ATK_UP: AttackState, ATK_DOWN: AttackState, ATK_RIGHT: AttackState, ATK_LEFT: AttackState,
                ATK_END: 999, SKIP_UP: 999, SKIP_DOWN: 999
                },
    AttackState: {RIGHT_KEYUP: 999, LEFT_KEYUP: 999,
                  UP_KEYUP: 999, DOWN_KEYUP: 999,
                  RIGHT_KEYDOWN: 999, LEFT_KEYDOWN: 999,
                  UP_KEYDOWN: 999, DOWN_KEYDOWN: 999,
                  STOP_MOVING: 999, ATK_END: IdleState,
                  ATK_UP: AttackState, ATK_DOWN: AttackState, ATK_RIGHT: AttackState, ATK_LEFT: AttackState,
                  SKIP_UP: 999, SKIP_DOWN: 999
                  }
}


class Warrior:

    def __init__(self):
        self.bg = main_state.maps
        self.lvl = 1
        self.exp = 0
        self.maxHp = 50
        self.hp = 50
        self.hpPercent = 1
        self.atkDamage = 8
        self.x, self.y = 16 + TILE_SIZE * 17, 16 + TILE_SIZE * 6
        self.tileX, self.tileY = (self.x - 16) // TILE_SIZE, (self.y - 16) // TILE_SIZE
        self.image = load_image('warriorLR.png')
        self.dir = 1  # 1 = R , 0 = L
        self.frame = 0
        self.timer = 0
        self.isDead = False
        self.event_que = []
        self.cnt = 0
        self.type = 'war'
        self.moveto = 0
        self.moving = 0
        self.idl = 0
        self.atkSt = 0
        self.cur_state = IdleState
        self.cur_state.enter(self, None)
        self.xCV, self.yCV = 0, 0

    def change_state(self, state):
        if len(self.event_que) > 0:
            event = self.event_que.pop()
            self.cur_state.exit(self, event)
            self.cur_state = next_state_table[self.cur_state][event]
            self.cur_state.enter(self, event)

    def add_event(self, event):
        self.event_que.insert(0, event)

    def update(self):
        self.tileX, self.tileY = (self.x - 16) // TILE_SIZE, (self.y - 16) // TILE_SIZE
        self.x = clamp(0, self.x, self.bg.w * 32)
        self.y = clamp(0, self.y, self.bg.h * 32)
        self.cx, self.cy = self.x - (self.bg.window_left * 32), self.y - (self.bg.window_bottom * 32)

        if self.hp > self.maxHp:
            self.hp = self.maxHp

        self.hpPercent = self.hp / self.maxHp
        self.cur_state.do(self)
        if len(self.event_que) > 0:
            event = self.event_que.pop()
            if next_state_table[self.cur_state][event] != 999:  # 999 -> IGNORE EVENT
                self.cur_state.exit(self, event)
                self.cur_state = next_state_table[self.cur_state][event]
                self.cur_state.enter(self, event)
        if self.isDead:
            self.dead()

    def draw(self):
        self.cur_state.draw(self)
        draw_rectangle(*self.get_bb())

    def handle_event(self, event):
        if (event.type, event.key) in key_event_table:
            key_event = key_event_table[(event.type, event.key)]
            self.add_event(key_event)

    def get_damage(self, damage):
        self.hp -= damage
        print("warrior's HP: ", self.hp)

    def dead(self):
        game_framework.change_state(title_state)  # dying animation , change_state( push_state ? ) to game_over.py

    def get_bb(self):
        return self.cx - 13, self.cy - 13, self.cx + 13, self.cy + 13

    def set_background(self, maps):
        self.bg = maps

    def get_correction_value(self, tx, ty):  # ?
        self.xCV = tx * 32
        self.yCV = ty * 32
