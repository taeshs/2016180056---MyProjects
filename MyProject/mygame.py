import game_framework
import pico2d

import title_state
import main_state

pico2d.open_canvas(400, 600)
game_framework.run(title_state)
pico2d.close_canvas()