from pico2d import *
import map
import main_state
import game_world
from BehaviorTree import BehaviorTree, SelectorNode, SequenceNode, LeafNode

TILE_SIZE = 32


# bt 행동우선순위  - attack - move - idle

class Monster:
    image = None
    def __init__(self, x, y):
        if Monster.image is None:
            Monster.image = load_image('gnoll.png')
        self.hp = 20
        self.atkDamage = 4
        self.x, self.y = x, y
        self.tileX, self.tileY = (self.x - 16) // 32, (self.y - 16) // 32
        self.dir = 1
        self.frame = 0
        self.timer = 0
        self.type = 'mon'
        self.isdead = False
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

    def is_dead(self):
        if self.isdead:
            return BehaviorTree.SUCCESS
        elif not self.isdead:
            return BehaviorTree.FAIL

    def is_nearing(self):
        warrior = main_state.get_warrior()
        distance = (warrior.tileX - self.tileX) ** 2 + (warrior.tileY - self.tileY) ** 2
        if distance == 1:
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.FAIL

    def attack_warrior(self):
        warrior = main_state.get_warrior()
        warrior.hp -= self.atkDamage
        self.state = 2
        return BehaviorTree.SUCCESS

    def find_warrior(self):
        warrior = main_state.get_warrior()
        distance = (warrior.tileX - self.tileX) ** 2 + (warrior.tileY - self.tileY) ** 2
        if distance < 9:
            if warrior.tileX < self.tileX:
                self.dir = 0
            elif warrior.tileX > self.tileX:
                self.dir = 1
            if ((warrior.tileX - self.tileX) ** 2) > ((warrior.tileY - self.tileY) ** 2):
                if warrior.tileX < self.tileX:
                    self.dir = 0
                elif warrior.tileX > self.tileX:
                    self.dir = 1
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.FAIL
        pass

    def move_to_warrior(self):
        self.state = 3
        pass

    def build_behavior_tree(self):
        is_dead_node = LeafNode("is dead?", self.is_dead)
        dead_node = LeafNode("dead", self.dead_status)
        dead_stat_node = SequenceNode("dead")
        dead_stat_node.add_children(is_dead_node, dead_node)

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

        idle_node = LeafNode("idle", self.idle_status)

        monster_status = SelectorNode("monster status")
        monster_status.add_children(dead_stat_node, monster_moves_node, idle_node)

        self.bt = BehaviorTree(monster_status)

    def update(self):
        self.bt.run()
        self.tileX, self.tileY = (self.x - 16) // 32, (self.y - 16) // 32
        # print("monster : ", (self.y - 16) // 32, (self.x - 16) // 32, map.MapLi[self.tileY][self.tileX])
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
        if self.state == 2:
            self.image.clip_draw(3 * 12, self.dir * 16, 12, 16, self.x,
                                 self.y, 24, 32)
            # 3, 4
        if self.state == 3:
            self.image.clip_draw(6 * 12, self.dir * 16, 12, 16, self.x,
                                 self.y, 24, 32)

    def return_obj_type(self):
        return self.type

    def return_loc(self):
        return self.tileX, self.tileY

    def get_damage(self, damage):
        self.hp -= damage
        print(self.hp)

    def dead(self):
        self.isdead = True
