from pico2d import *

windsizX = 320
windsizY = 480
nomsize = 16
fixsize = 32
tilecnt = windsizX // fixsize * windsizY // fixsize


# #tilecnt = 10 * 20 = 200

class Map:
    def __init__(self):
        self.image = load_image('tiles0.png')

    def draw(self):
        for n in range(tilecnt):
            if True:  # 벽 땅 공허 조건으로 바꾸자.
                self.image.clip_draw(48, 16, nomsize, nomsize,
                                     (fixsize / 2) + fixsize * (n % (windsizX / fixsize)),
                                     (fixsize / 2) + fixsize * (n // (windsizX / fixsize)),
                                     fixsize, fixsize)
