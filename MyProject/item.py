from pico2d import *


class Item:
    image = None

    def __init__(self, x, y):
        if Item.image == None:
            Item.image = load_image('items.png')

        self.hp = 999
        self.type = 'itm'
        self.x, self.y = x, y
        self.tileX, self.tileY = (self.x - 16) // 32, (self.y - 16) // 32

    def update(self):
        pass

    def draw(self):
        self.image.clip_draw(16, 16, 16, 16, self.x, self.y, 32, 32)
        draw_rectangle(*self.get_bb())

    def get_bb(self):
        return self.x - 15, self.y - 15, self.x + 15, self.y + 15
