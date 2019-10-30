from pico2d import *

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


class RunState:
    @staticmethod
    def enter(warrior, event):
        print("runstate")
        if warrior.moving == 0:
            warrior.cnt = 0
            if event == RIGHT_DOWN:
                warrior.xy = 1
                warrior.dir = 1
            elif event == LEFT_DOWN:
                warrior.xy = 2
                warrior.dir = 0
            elif event == UP_DOWN:
                warrior.xy = 3
            elif event == DOWN_DOWN:
                warrior.xy = 4

    @staticmethod
    def exit(warrior, event):
        pass

    @staticmethod
    def do(warrior):
        if warrior.cnt < 50:
            if warrior.xy == 1:
                if warrior.x < DISPLAY_SIZE_X:
                    warrior.x += 1
                    warrior.cnt += 1
                else:
                    warrior.cnt = 50
            elif warrior.xy == 2:
                if warrior.x > 0:
                    warrior.x -= 1
                    warrior.cnt += 1
                else:
                    warrior.cnt = 50
            elif warrior.xy == 3:
                if warrior.y < DISPLAY_SIZE_Y:
                    warrior.y += 1
                    warrior.cnt += 1
                else:
                    warrior.cnt = 50
            elif warrior.xy == 4:
                if warrior.y > 0:
                    warrior.y -= 1
                    warrior.cnt += 1
                else:
                    warrior.cnt = 50
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
        warrior.image.clip_draw(warrior.frame * 12, warrior.dir * 15, 12, 15, warrior.x, warrior.y, 24, 30)


next_state_table = {  # 이벤트 테이블에 관한 고찰, Runstate를 과연 쓸것인가?(움직임의 함수화)
    IdleState: {RIGHT_DOWN: RunState, LEFT_DOWN: RunState,
                UP_DOWN: RunState, DOWN_DOWN: RunState,
                RIGHT_UP: IdleState, LEFT_UP: IdleState,
                UP_UP: IdleState, DOWN_UP: IdleState,
                },
    RunState: {RIGHT_UP: RunState, LEFT_UP: RunState,
               UP_UP: RunState, DOWN_UP: RunState,
               RIGHT_DOWN: RunState, LEFT_DOWN: RunState,
               UP_DOWN: RunState, DOWN_DOWN: RunState,
               M_STOP: IdleState
               }
}


class Warrior:

    def __init__(self):
        self.x, self.y = 0, 0
        self.image = load_image('warriorLR.png')
        self.dir = 1
        self.velocity = 0
        self.frame = 0
        self.timer = 0
        self.event_que = []
        self.cnt = 0
        self.xy = 0
        self.moving = 0
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
            self.cur_state.exit(self, event)
            self.cur_state = next_state_table[self.cur_state][event]
            self.cur_state.enter(self, event)

    def draw(self):
        self.cur_state.draw(self)

    def handle_event(self, event):
        if (event.type, event.key) in key_event_table:
            key_event = key_event_table[(event.type, event.key)]
            self.add_event(key_event)

    def move(self, direc, plmi):  # move 는 정상동작함.
        cnt = 0
        # direc 1 = x, 0 = y
        # plmi 1 = +, 0 = -
        if direc == 1:
            if plmi == 1:
                if self.x < DISPLAY_SIZE_X:
                    while cnt < 5:
                        self.x += 1
                        cnt += 1
            elif plmi == 0:
                if self.x > 0:
                    while cnt < 5:
                        self.x -= 1
                        cnt += 1
        elif direc == 0:
            if plmi == 1:
                if self.y < DISPLAY_SIZE_Y:
                    while cnt < 5:
                        self.y += 1
                        cnt += 1
            elif plmi == 0:
                if self.y > 0:
                    while cnt < 5:
                        self.y -= 1
                        cnt += 1
