from pico2d import *


class Item:
    image = None

    def __init__(self, x, y, var):
        if Item.image == None:
            Item.image = load_image('Images//items.png')

        self.hp = 999
        self.type = 'itm'
        self.x, self.y = x, y
        self.var = var
        self.tileX, self.tileY = (self.x - 16) // 32, (self.y - 16) // 32

    def update(self):
        self.cx, self.cy = self.x - (self.bg.window_left * 32), self.y - (self.bg.window_bottom * 32)

    def draw(self):
        if self.var == 1:
            self.image.clip_draw(16, 128, 16, 16, self.cx, self.cy, 32, 32)
        if self.var == 2:
            self.image.clip_draw(96, 208, 16, 16, self.cx, self.cy, 32, 32)
        if self.var == 3:
            self.image.clip_draw(64, 192, 16, 16, self.cx, self.cy, 32, 32)
        #draw_rectangle(*self.get_bb())

    def get_bb(self):
        return self.cx - 15, self.cy - 15, self.cx + 15, self.cy + 15

    def set_background(self, maps):
        self.bg = maps
