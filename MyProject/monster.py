from pico2d import *
import map
import main_state
import game_world

TILE_SIZE = 32


# bt 에서 idle 일시 monster.timer = 0 , timer 로 idle animation 나오게.
# bt 에서 dead 일시 monster.deadtimer = 0 , dead일때, dead animation 재생,


class Monster:

    def __init__(self, x, y):
        self.hp = 20
        self.x, self.y = x, y
        self.tileX, self.tileY = (self.x - 16) // 32, (self.y - 16) // 32
        self.image = load_image('gnoll.png')
        self.dir = 1
        self.frame = 0
        self.timer = 0
        self.deadtimer = 0
        self.cnt = 0
        self.xy = 0
        self.moving = 0
        self.idl = 0
        self.isdead = False


    def update(self):
        self.tileX, self.tileY = (self.x - 16) // 32, (self.y - 16) // 32
        print("monster : ", (self.y - 16) // 32, (self.x - 16) // 32, map.MapLi[self.tileY][self.tileX])
        if not self.isdead:
            self.timer = (self.timer + 1) % 1000
            if self.timer > 800:
                self.idl = 1
            else:
                self.idl = 0
        if self.isdead:
            self.deadtimer += 1
            if self.deadtimer == 96:
                game_world.remove_object(self)

    def draw(self):
        if not self.isdead:  # 7 8 9 10  monster.timer // 250
            self.image.clip_draw(self.idl * 12, self.dir * 16, 12, 16, self.x, self.y, 24, 32)
        if self.isdead:
            self.image.clip_draw((((self.deadtimer // 16) % 6) + 7) * 12, self.dir * 16, 12, 16, self.x,
                                    self.y, 24, 32)

    def return_obj_type(self):
        return 'mon'

    def return_loc(self):
        return self.tileX, self.tileY

    def get_damage(self, damage):
        self.hp -= damage
        print(self.hp)

    def dead(self):
        self.isdead = True
