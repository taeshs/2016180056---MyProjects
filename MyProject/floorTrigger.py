from pico2d import *


class FloorTrigger:
    image = None

    def __init__(self, x, y):
        if FloorTrigger.image == None:
            FloorTrigger.image = load_image('tiles0.png')
        self.hp = 999
        self.type = 'map'
        self.x, self.y = x+16, y+16
        self.tileX, self.tileY = (self.x - 16) // 32, (self.y - 16) // 32

    def update(self):
        self.cx, self.cy = self.x - (self.bg.window_left * 32), self.y - (self.bg.window_bottom * 32)

    def draw(self):
        self.image.clip_draw(128, 48, 16, 16, self.cx, self.cy, 32, 32)
        draw_rectangle(*self.get_bb())

    def get_bb(self):
        return self.cx - 15, self.cy - 15, self.cx + 15, self.cy + 15

    def set_background(self, maps):
        self.bg = maps
