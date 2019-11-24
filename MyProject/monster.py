from pico2d import *
import map
import main_state
import game_world
from BehaviorTree import BehaviorTree, SelectorNode, SequenceNode, LeafNode

TILE_SIZE = 32


# bt 에서 idle 일시 monster.timer = 0 , timer 로 idle animation 나오게.
# bt 에서 dead 일시 monster.deadtimer = 0 , dead일때, dead animation 재생, // ?
# bt 행동우선순위  - attack - move - idle

class Monster:
    image = None
    def __init__(self, x, y):
        if Monster.image is None:
            Monster.image = load_image('gnoll.png')
        self.hp = 20
        self.x, self.y = x, y
        self.tileX, self.tileY = (self.x - 16) // 32, (self.y - 16) // 32
        self.dir = 1
        self.frame = 0
        self.timer = 0
        self.deadtimer = 0
        self.cnt = 0
        self.xy = 0
        self.moving = 0
        self.idl = 0
        self.state = 0    # 0 idle 1 dead
        self.build_behavior_tree()

    def idle_status(self):
        self.state = 0
        return BehaviorTree.SUCCESS

    def dead_status(self):
        self.state = 1
        return BehaviorTree.SUCCESS

    def is_nearing(self):
        pass

    def attack_warrior(self):
        pass

    def find_warrior(self):
        pass

    def move_to_warrior(self):
        pass

    def build_behavior_tree(self):
        idle_node = LeafNode("idle", self.idle_status)

        dead_node = LeafNode("dead", self.dead_status)      # is_dead 랑 dead로 나눠야 됨.

        is_nearing_node = LeafNode("is nearing?", self.is_nearing)
        attack_warrior_node = LeafNode("attack node", self.attack_warrior)
        attack_node = SequenceNode("attack")
        attack_node.add_children(is_nearing_node, attack_warrior_node)

        find_warrior_node = LeafNode("find warrior", self.find_warrior)
        move_to_warrior_node = LeafNode("move to warrior", self.move_to_warrior)
        chase_node = SequenceNode("move to")
        chase_node.add_children(find_warrior_node, move_to_warrior_node)

        monster_moves_node = SelectorNode("moves")
        monster_moves_node.add_children(attack_node, chase_node)

        monster_status = SelectorNode("monster status")
        monster_status.add_children(dead_node, monster_moves_node, idle_node)

        self.bt = monster_status

    def update(self):
        self.tileX, self.tileY = (self.x - 16) // 32, (self.y - 16) // 32
        print("monster : ", (self.y - 16) // 32, (self.x - 16) // 32, map.MapLi[self.tileY][self.tileX])
        if self.state == 0:
            self.timer = (self.timer + 1) % 1000
            if self.timer > 800:
                self.idl = 1
            else:
                self.idl = 0
        if self.state == 1:
            self.deadtimer += 1
            if self.deadtimer == 96:
                game_world.remove_object(self)

    def draw(self):
        if self.state == 0:  # 7 8 9 10  monster.timer // 250
            self.image.clip_draw(self.idl * 12, self.dir * 16, 12, 16, self.x, self.y, 24, 32)
        if self.state == 1:
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
