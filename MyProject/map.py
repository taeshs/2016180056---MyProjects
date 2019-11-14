from pico2d import *

windsizX = 320
windsizY = 480
nomsize = 16
fixsize = 32
tilecnt = windsizX // fixsize * windsizY // fixsize

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
         [0, 1, 1, 1, 1, 1, 1, 1, 1, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]


# #tilecnt = 10 * 20 = 200

class Map:
    def __init__(self):
        self.image = load_image('tiles0.png')
        self.hp = 99999

    def update(self):
        pass

    def draw(self):
        for n in range(tilecnt):
            if MapLi[n // (windsizX // fixsize)][(n % (windsizX // fixsize))] == 0:  # 벽 땅 공허 조건으로 바꾸자.
                self.image.clip_draw(0, 48, nomsize, nomsize,
                                     (fixsize / 2) + fixsize * (n % (windsizX / fixsize)),
                                     (fixsize / 2) + fixsize * (n // (windsizX / fixsize)),
                                     fixsize, fixsize)
            elif MapLi[n // (windsizX // fixsize)][(n % (windsizX // fixsize))] == 1:
                self.image.clip_draw(0, 32, nomsize, nomsize,
                                     (fixsize / 2) + fixsize * (n % (windsizX / fixsize)),
                                     (fixsize / 2) + fixsize * (n // (windsizX / fixsize)),
                                     fixsize, fixsize)
            elif MapLi[n // (windsizX // fixsize)][(n % (windsizX // fixsize))] == 2:
                self.image.clip_draw(16, 16, nomsize, nomsize,
                                     (fixsize / 2) + fixsize * (n % (windsizX / fixsize)),
                                     (fixsize / 2) + fixsize * (n // (windsizX / fixsize)),
                                     fixsize, fixsize)

    def return_obj_type(self):
        return 'map'
