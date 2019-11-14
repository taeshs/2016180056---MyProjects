from pico2d import *
import map
import main_state

TILE_SIZE = 32


class IdleState:
    @staticmethod
    def enter(monster, event):
        print("idlestate")
        monster.tileX, monster.tileY = (monster.x - 16) // 32, (monster.y - 16) // 32
        print("monster : ", (monster.y - 16) // 32, (monster.x - 16) // 32, map.MapLi[monster.tileY][monster.tileX])
        monster.timer = 0

    @staticmethod
    def exit(monster, event):
        pass

    @staticmethod
    def do(monster):
        monster.timer = (monster.timer + 1) % 1000
        if monster.timer > 800:
            monster.idl = 1
        else:
            monster.idl = 0
        # warrior가 인식범위에 들어왔나? : event 줘서 그 이벤트 동안은 movestate로,
        # movestate 동안 warrior 쪽으로 이동 ( move event )
        # 바로 옆칸에 warrior 존재 시 공격. (공격 이동 모두 move 내에서 실행.) ( attack event )

    @staticmethod
    def draw(monster):
        monster.image.clip_draw(monster.idl * 12, monster.dir * 16, 12, 16, monster.x, monster.y, 24, 32)


class MoveState:
    @staticmethod
    def enter(monster, event):
        pass

    @staticmethod
    def exit(monster, event):
        pass

    @staticmethod
    def do(monster):
        pass

    @staticmethod
    def draw(monster):
        pass


next_state_table = {
    IdleState: {

    },
    MoveState: {

    }
}


class Monster:

    def __init__(self, x, y):
        self.hp = 20
        self.x, self.y = x, y
        self.tileX, self.tileY = (self.x - 16) // 32, (self.y - 16) // 32
        self.image = load_image('gnoll.png')
        self.dir = 1
        self.frame = 0
        self.timer = 0
        self.event_que = []
        self.cnt = 0
        self.xy = 0
        self.moving = 0
        self.idl = 0
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

    def return_obj_type(self):
        return 'mon'

    def return_loc(self):
        return self.tileX, self.tileY

    def get_damage(self, damage):
        self.hp -= damage
        print(self.hp)
