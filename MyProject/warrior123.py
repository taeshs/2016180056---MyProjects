from pico2d import *

# Boy Event
RIGHT_DOWN, LEFT_DOWN, RIGHT_UP, LEFT_UP, DASH_DOWN, DASH_UP = range(6)

key_event_table = {
    (SDL_KEYDOWN, SDLK_RIGHT): RIGHT_DOWN,
    (SDL_KEYDOWN, SDLK_LEFT): LEFT_DOWN,
    (SDL_KEYDOWN, SDLK_LSHIFT): DASH_DOWN,
    (SDL_KEYUP, SDLK_RIGHT): RIGHT_UP,
    (SDL_KEYUP, SDLK_LEFT): LEFT_UP,
    (SDL_KEYUP, SDLK_LSHIFT): DASH_UP
}


# Boy States

class IdleState:
    @staticmethod
    def enter(warrior, event):
        if event == RIGHT_DOWN:
            warrior.velocity += 1
        elif event == LEFT_DOWN:
            warrior.velocity -= 1
        elif event == RIGHT_UP:
            warrior.velocity -= 1
        elif event == LEFT_UP:
            warrior.velocity += 1

    @staticmethod
    def exit(warrior, event):
        pass

    @staticmethod
    def do(warrior):
        warrior.frame = (warrior.frame + 1) % 8

    @staticmethod
    def draw(warrior):
        if warrior.dir == 1:
            warrior.image.clip_draw(warrior.frame * 100, 300, 100, 100, warrior.x, warrior.y)
        else:
            warrior.image.clip_draw(warrior.frame * 100, 200, 100, 100, warrior.x, warrior.y)


class RunState:
    @staticmethod
    def enter(warrior, event):
        if event == RIGHT_DOWN:
            warrior.velocity += 1
        elif event == LEFT_DOWN:
            warrior.velocity -= 1
        elif event == RIGHT_UP:
            warrior.velocity -= 1
        elif event == LEFT_UP:
            warrior.velocity += 1
        warrior.dir = warrior.velocity

    @staticmethod
    def exit(warrior, event):
        pass

    @staticmethod
    def do(warrior):
        warrior.frame = (warrior.frame + 1) % 8
        warrior.x += warrior.velocity
        warrior.x = clamp(25, warrior.x, 800 - 25)

    @staticmethod
    def draw(warrior):
        if warrior.dir == 1:
            warrior.image.clip_draw(warrior.frame * 100, 100, 100, 100, warrior.x, warrior.y)
        else:
            warrior.image.clip_draw(warrior.frame * 100, 0, 100, 100, warrior.x, warrior.y)


class DashState:
    @staticmethod
    def enter(warrior, event):
        warrior.timer = 100

    @staticmethod
    def exit(warrior, event):
        pass

    @staticmethod
    def do(warrior):
        warrior.frame = (warrior.frame + 1) % 8
        warrior.timer -= 1
        if warrior.timer == 0:
            warrior.add_event(DASH_UP)
        warrior.x += warrior.velocity * 2
        warrior.x = clamp(25, warrior.x, 800 - 25)

    @staticmethod
    def draw(warrior):
        if warrior.dir == 1:
            warrior.image.clip_draw(warrior.frame * 100, 100, 100, 100, warrior.x, warrior.y)
        else:
            warrior.image.clip_draw(warrior.frame * 100, 0, 100, 100, warrior.x, warrior.y)


next_state_table = {
    IdleState: {RIGHT_UP: RunState, LEFT_UP: RunState,
                RIGHT_DOWN: RunState, LEFT_DOWN: RunState,
                DASH_UP: IdleState, DASH_DOWN: IdleState},
    RunState: {RIGHT_UP: IdleState, LEFT_UP: IdleState,
               RIGHT_DOWN: IdleState, LEFT_DOWN: IdleState,
               DASH_UP: RunState, DASH_DOWN: DashState},
    DashState: {RIGHT_UP: IdleState, LEFT_UP: IdleState,
                RIGHT_DOWN: IdleState, LEFT_DOWN: IdleState,
                DASH_UP: RunState, DASH_DOWN: RunState}
}


class Warrior:

    def __init__(self):
        self.x, self.y = 800 // 2, 90
        self.image = load_image('warrior.png')
        self.dir = 1
        self.velocity = 0
        self.frame = 0
        self.timer = 0
        self.event_que = []
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
