from pico2d import *
import map
import main_state
import game_world

# Boy Event
UP_KEYDOWN, DOWN_KEYDOWN, RIGHT_KEYDOWN, LEFT_KEYDOWN, \
UP_KEYUP, DOWN_KEYUP, RIGHT_KEYUP, LEFT_KEYUP, STOP_MOVING = range(9)

key_event_table = {
    (SDL_KEYDOWN, SDLK_UP): UP_KEYDOWN,
    (SDL_KEYDOWN, SDLK_DOWN): DOWN_KEYDOWN,
    (SDL_KEYDOWN, SDLK_RIGHT): RIGHT_KEYDOWN,
    (SDL_KEYDOWN, SDLK_LEFT): LEFT_KEYDOWN,
    (SDL_KEYUP, SDLK_UP): UP_KEYUP,
    (SDL_KEYUP, SDLK_DOWN): DOWN_KEYUP,
    (SDL_KEYUP, SDLK_RIGHT): RIGHT_KEYUP,
    (SDL_KEYUP, SDLK_LEFT): LEFT_KEYUP
}

TILE_SIZE = 32


# Boy States

class IdleState:
    @staticmethod
    def enter(warrior, event):
        print("idlestate")
        warrior.tileX, warrior.tileY = (warrior.x - 16) // TILE_SIZE, (warrior.y - 16) // TILE_SIZE
        print("warrior : ", (warrior.y - 16) // TILE_SIZE, (warrior.x - 16) // TILE_SIZE,
              map.MapLi[warrior.tileY][warrior.tileX])
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
        warrior.image.clip_draw(warrior.idl * 12, warrior.dir * 15, 12, 15, warrior.x, warrior.y, 24, 30)
        # character.clip_draw(poz, pos, 12, 15, x, y, 36, 45)


class RunState:  # 공격 추가 : 바로 옆칸에 monster 존재 시 and 그쪽 방향키 누를시 move 대신 attack
    @staticmethod
    def enter(warrior, event):
        if warrior.moving == 0:
            print("runstate")
            if event == RIGHT_KEYDOWN:
                for game_object in game_world.all_objects():
                    if game_object.return_obj_type() == 'mon':
                        check_monster_tileX, check_monster_tileY = game_object.return_loc()
                        if warrior.tileX + 1 == check_monster_tileX and warrior.tileY == check_monster_tileY:
                            warrior.atkSt = 1
                if warrior.atkSt != 1 and map.MapLi[warrior.tileY][warrior.tileX + 1] == 2:
                    warrior.moveto = 'RIGHT'
                    warrior.dir = 1
                    warrior.cnt = 0
            elif event == LEFT_KEYDOWN:
                for game_object in game_world.all_objects():
                    if game_object.return_obj_type() == 'mon':
                        check_monster_tileX, check_monster_tileY = game_object.return_loc()
                        if warrior.tileX - 1 == check_monster_tileX and warrior.tileY == check_monster_tileY:
                            warrior.atkSt = 1
                if warrior.atkSt != 1 and map.MapLi[warrior.tileY][warrior.tileX - 1] == 2:
                    warrior.moveto = 'LEFT'
                    warrior.dir = 0
                    warrior.cnt = 0
            elif event == UP_KEYDOWN:
                for game_object in game_world.all_objects():
                    if game_object.return_obj_type() == 'mon':
                        check_monster_tileX, check_monster_tileY = game_object.return_loc()
                        if warrior.tileX == check_monster_tileX and warrior.tileY + 1 == check_monster_tileY:
                            warrior.atkSt = 1
                if warrior.atkSt != 1 and map.MapLi[warrior.tileY + 1][warrior.tileX] == 2:
                    warrior.moveto = 'UP'
                    warrior.cnt = 0
            elif event == DOWN_KEYDOWN:
                for game_object in game_world.all_objects():
                    if game_object.return_obj_type() == 'mon':
                        check_monster_tileX, check_monster_tileY = game_object.return_loc()
                        if warrior.tileX == check_monster_tileX and warrior.tileY - 1 == check_monster_tileY:
                            warrior.atkSt = 1
                if warrior.atkSt != 1 and map.MapLi[warrior.tileY - 1][warrior.tileX] == 2:
                    warrior.moveto = 'DOWN'
                    warrior.cnt = 0

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
            warrior.add_event(STOP_MOVING)
        warrior.frame = warrior.frame + 1
        if warrior.frame == 8:
            warrior.frame = 2
        # warrior.x = clamp(25, warrior.x, DISPLAY_SIZE_X - 25)
        # warrior.y = clamp(25, warrior.y, DISPLAY_SIZE_Y - 25)

    @staticmethod
    def draw(warrior):
        if warrior.atkSt == 1:
            print("attack")
            warrior.atkSt = 0
        else:
            warrior.image.clip_draw(warrior.frame * 12, warrior.dir * 15, 12, 15, warrior.x, warrior.y, 24, 30)


next_state_table = {  # 999 -> IGNORE EVENT
    IdleState: {RIGHT_KEYDOWN: RunState, LEFT_KEYDOWN: RunState,
                UP_KEYDOWN: RunState, DOWN_KEYDOWN: RunState,
                RIGHT_KEYUP: 999, LEFT_KEYUP: 999,
                UP_KEYUP: 999, DOWN_KEYUP: 999,
                STOP_MOVING: 999
                },
    RunState: {RIGHT_KEYUP: 999, LEFT_KEYUP: 999,
               UP_KEYUP: 999, DOWN_KEYUP: 999,
               RIGHT_KEYDOWN: 999, LEFT_KEYDOWN: 999,
               UP_KEYDOWN: 999, DOWN_KEYDOWN: 999,
               STOP_MOVING: IdleState
               }
}


class Warrior:

    def __init__(self):
        self.x, self.y = 16 + TILE_SIZE * 3, 16 + TILE_SIZE * 5
        self.tileX, self.tileY = (self.x - 16) // TILE_SIZE, (self.y - 16) // TILE_SIZE
        self.image = load_image('warriorLR.png')
        self.dir = 1  # 1 = R , 0 = L
        self.frame = 0
        self.timer = 0
        self.event_que = []
        self.cnt = 0
        self.moveto = 0
        self.moving = 0
        self.idl = 0
        self.atkSt = 0
        self.cur_state = IdleState
        self.cur_state.enter(self, None)

    def change_state(self, state):
        if len(self.event_que) > 0:
            event = self.event_que.pop()
            self.cur_state.exit(self, event)
            self.cur_state = next_state_table[self.cur_state][event]
            self.cur_state.enter(self, event)

    def add_event(self, event):
        self.event_que.insert(0, event)

    def update(self):
        self.cur_state.do(self)
        if len(self.event_que) > 0:
            event = self.event_que.pop()
            if next_state_table[self.cur_state][event] != 999:  # 999 -> IGNORE EVENT
                self.cur_state.exit(self, event)
                self.cur_state = next_state_table[self.cur_state][event]
                self.cur_state.enter(self, event)

    def draw(self):
        self.cur_state.draw(self)

    def handle_event(self, event):
        if (event.type, event.key) in key_event_table:
            key_event = key_event_table[(event.type, event.key)]
            self.add_event(key_event)

    def return_obj_type(self):
        return 'war'
