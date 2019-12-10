from pico2d import *

nomsize = 16
fixsize = 32
windsizX = 320
windsizY = 576
canvasTileSizeX, canvasTileSizeY = windsizX // fixsize, windsizY // fixsize
tileX, tileY = 10, 24
tilecnt = tileX * tileY
# windsizX // fixsize * windsizY // fixsize

# 상하반전
MapLi = [[0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 1, 1, 1, 1, 1, 1, 1, 1, 0],
         [0, 1, 2, 2, 2, 2, 2, 2, 1, 0],
         [0, 1, 2, 2, 2, 2, 2, 2, 1, 0],
         [0, 1, 2, 2, 2, 1, 2, 2, 1, 0],
         [0, 1, 2, 2, 2, 2, 2, 2, 1, 0],
         [0, 1, 2, 2, 2, 2, 2, 2, 1, 0],
         [0, 1, 2, 2, 2, 2, 2, 2, 1, 0],
         [0, 1, 2, 2, 2, 2, 2, 2, 1, 0],
         [0, 1, 2, 2, 2, 2, 2, 2, 1, 0],
         [0, 1, 2, 2, 2, 2, 2, 2, 1, 0],
         [0, 1, 2, 2, 2, 2, 2, 2, 1, 0],
         [0, 1, 1, 1, 1, 1, 2, 1, 1, 0],
         [0, 0, 0, 0, 0, 1, 2, 1, 0, 0],
         [0, 0, 1, 1, 1, 1, 2, 1, 1, 0],
         [0, 0, 1, 2, 2, 2, 2, 2, 1, 0],
         [0, 0, 1, 2, 2, 2, 2, 2, 1, 0],
         [0, 0, 1, 2, 2, 2, 2, 2, 1, 0],
         [0, 0, 1, 2, 2, 2, 2, 2, 1, 0],
         [0, 0, 1, 1, 1, 1, 1, 1, 1, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]


# #tilecnt = 10 * 20 = 200

class Map:
    def __init__(self):
        self.image = load_image('tiles0.png')
        self.w, self.h = tileX, tileY
        self.hp = 99999
        self.type = 'map'

    def update(self):
        self.window_left = clamp(0,
                                 int(self.center_object.tileX) - tileX // 2,
                                 self.w - canvasTileSizeX)
        self.window_bottom = clamp(0,
                                   int(self.center_object.tileY) - tileY // 2,
                                   self.h - canvasTileSizeY)

    def draw(self):
        for n in range(tilecnt):
            x, y = n % tileX, n // tileX
            self.center_object.get_correction_value(x - self.window_left, y - self.window_bottom) # 스크롤링시 이동 이상 방지
            if self.window_left + canvasTileSizeX > x >= self.window_left and \
                    self.window_bottom + canvasTileSizeY > y >= self.window_bottom:
                if MapLi[y][x] == 0:  # 벽 땅 공허 조건으로 바꾸자.
                    self.image.clip_draw_to_origin(0, 48, nomsize, nomsize,
                                                   fixsize * (x - self.window_left),
                                                   fixsize * (y - self.window_bottom),
                                                   fixsize, fixsize)
                elif MapLi[y][x] == 1:
                    self.image.clip_draw_to_origin(0, 32, nomsize, nomsize,
                                                   fixsize * (x - self.window_left),
                                                   fixsize * (y - self.window_bottom),
                                                   fixsize, fixsize)
                elif MapLi[y][x] == 2:
                    self.image.clip_draw_to_origin(16, 16, nomsize, nomsize,
                                                   fixsize * (x - self.window_left),
                                                   fixsize * (y - self.window_bottom),
                                                   fixsize, fixsize)

    # self.image.clip_draw_to_origin(self.window_left, self.window_bottom,self.canvas_width, self.canvas_height,0, 0)

    def set_center_object(self, warrior):
        self.center_object = warrior
