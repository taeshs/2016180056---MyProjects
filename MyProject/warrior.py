from pico2d import *
import map
import main_state
# Boy Event
UP_DOWN, DOWN_DOWN, RIGHT_DOWN, LEFT_DOWN, UP_UP, DOWN_UP, RIGHT_UP, LEFT_UP, M_STOP = range(9)

key_event_table = {
    (SDL_KEYDOWN, SDLK_UP): UP_DOWN,
    (SDL_KEYDOWN, SDLK_DOWN): DOWN_DOWN,
    (SDL_KEYDOWN, SDLK_RIGHT): RIGHT_DOWN,
    (SDL_KEYDOWN, SDLK_LEFT): LEFT_DOWN,
    (SDL_KEYUP, SDLK_UP): UP_UP,
    (SDL_KEYUP, SDLK_DOWN): DOWN_UP,
    (SDL_KEYUP, SDLK_RIGHT): RIGHT_UP,
    (SDL_KEYUP, SDLK_LEFT): LEFT_UP
}

DISPLAY_SIZE_X = 400
DISPLAY_SIZE_Y = 600


# Boy States

class IdleState:
    @staticmethod
    def enter(warrior, event):
        print("idlestate")
        warrior.tx, warrior.ty = (warrior.x - 16) // 32, (warrior.y - 16) // 32
        print("warrior : ", (warrior.y - 16) // 32, (warrior.x - 16) // 32, map.MapLi[warrior.ty][warrior.tx])
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
            if event == RIGHT_DOWN:
                if warrior.tx + 1 == main_state.monster.tx and warrior.ty == main_state.monster.ty:
                    warrior.atkSt = 1
                    pass # attack
                elif map.MapLi[warrior.ty][warrior.tx + 1] == 2:
                    warrior.xy = 1
                    warrior.dir = 1
                    warrior.cnt = 0
            elif event == LEFT_DOWN:
                if map.MapLi[warrior.ty][warrior.tx - 1] == 2:
                    warrior.xy = 2
                    warrior.dir = 0
                    warrior.cnt = 0
            elif event == UP_DOWN:
                if map.MapLi[warrior.ty + 1][warrior.tx] == 2:
                    warrior.xy = 3
                    warrior.cnt = 0
            elif event == DOWN_DOWN:
                if map.MapLi[warrior.ty - 1][warrior.tx] == 2:
                    warrior.xy = 4
                    warrior.cnt = 0

    @staticmethod
    def exit(warrior, event):
        pass

    @staticmethod
    def do(warrior):
        if warrior.cnt < 32:
            if warrior.xy == 1:
                warrior.x += 1
                warrior.cnt += 1
            elif warrior.xy == 2:
                warrior.x -= 1
                warrior.cnt += 1
            elif warrior.xy == 3:
                warrior.y += 1
                warrior.cnt += 1
            elif warrior.xy == 4:
                warrior.y -= 1
                warrior.cnt += 1
                #else:
                 #   warrior.cnt = 32
            warrior.moving = 1
        else:
            warrior.moving = 0
            warrior.add_event(M_STOP)
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



next_state_table = {
    IdleState: {RIGHT_DOWN: RunState, LEFT_DOWN: RunState,
                UP_DOWN: RunState, DOWN_DOWN: RunState,
                RIGHT_UP: 999, LEFT_UP: 999,
                UP_UP: 999, DOWN_UP: 999,
                M_STOP: 999
                },
    RunState: {RIGHT_UP: 999, LEFT_UP: 999,
               UP_UP: 999, DOWN_UP: 999,
               RIGHT_DOWN: 999, LEFT_DOWN: 999,
               UP_DOWN: 999, DOWN_DOWN: 999,
               M_STOP: IdleState
               }
}


class Warrior:

    def __init__(self):
        self.x, self.y = 16 + 64 + 32, 16 + 128 + 32
        self.tx, self.ty = (self.x - 16)//32, (self.y - 16)//32
        self.image = load_image('warriorLR.png')
        self.dir = 1
        self.frame = 0
        self.timer = 0
        self.event_que = []
        self.cnt = 0
        self.xy = 0
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
                if next_state_table[self.cur_state][event] != 999:
                    self.cur_state.exit(self, event)
                    self.cur_state = next_state_table[self.cur_state][event]
                    self.cur_state.enter(self, event)

    def draw(self):
        self.cur_state.draw(self)

    def handle_event(self, event):
        if (event.type, event.key) in key_event_table:
            key_event = key_event_table[(event.type, event.key)]
            self.add_event(key_event)
