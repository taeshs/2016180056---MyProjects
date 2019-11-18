import game_framework
import pico2d

import title_state
import main_state
import map

pico2d.open_canvas(map.windsizX, map.windsizY, sync=True)
game_framework.run(title_state)
pico2d.close_canvas()