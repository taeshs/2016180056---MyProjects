from pico2d import *
import map
import main_state
import game_world
import game_framework
from BehaviorTree import BehaviorTree, SelectorNode, SequenceNode, LeafNode

TILE_SIZE = 32

TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 8

# bt 행동우선순위  - attack - move - idle

class Scorpio:
    image = None

    def __init__(self, x, y):
        if Scorpio.image is None:
            Scorpio.image = load_image('Images//scorpio.png')
        self.hp = 15
        self.atkDamage = 6
        self.atkPose = 0
        self.dx, self.dy = 18, 17
        self.x, self.y = x, y
        self.tileX, self.tileY = (self.x - 16) // 32, (self.y - 16) // 32
        self.dir = 1
        self.moveDir = 5
        self.frame = 0
        self.timer = 0
        self.type = 'mon'
        self.isDead = False
        self.deadTimer = 0
        self.atkTimer = 0
        self.turn = 0  # turn == 1 : movable
        self.cnt = 0
        self.xy = 0
        self.moving = 0
        self.idl = 0
        self.state = 0  # 0 idle 1 dead
        self.build_behavior_tree()

    def idle_status(self):
        self.state = 0
        return BehaviorTree.SUCCESS

    def dead_status(self):
        self.state = 1
        return BehaviorTree.SUCCESS

    def is_dead(self):
        if self.isDead:
            return BehaviorTree.SUCCESS
        elif not self.isDead:
            return BehaviorTree.FAIL

    def is_nearing(self):
        warrior = main_state.get_warrior()
        distance = (warrior.tileX - self.tileX) ** 2 + (warrior.tileY - self.tileY) ** 2
        if distance == 1 and self.moving == 0:
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.FAIL

    def attack_warrior(self):
        warrior = main_state.get_warrior()
        warrior.get_damage(self.atkDamage)
        self.state = 2
        self.turn = 0
        return BehaviorTree.SUCCESS

    def find_warrior(self):
        disrupt = 0
        warrior = main_state.get_warrior()
        distance = (warrior.tileX - self.tileX) ** 2 + (warrior.tileY - self.tileY) ** 2
        if distance < 9:
            if warrior.tileX < self.tileX:
                self.dir = 0
            elif warrior.tileX > self.tileX:
                self.dir = 1
            if self.moving == 0:
                if ((warrior.tileX - self.tileX) ** 2) > ((warrior.tileY - self.tileY) ** 2):
                    if warrior.tileX < self.tileX and self.bg.mapli[self.tileY][self.tileX - 1] == 2:
                        for game_object in game_world.all_objects():
                            if game_object.type == 'mon':
                                check_monster_tileX, check_monster_tileY = game_object.return_loc()
                                if self.tileX - 1 == check_monster_tileX and self.tileY == check_monster_tileY:
                                    disrupt = 1
                        if disrupt == 0:
                            self.moveDir = 1  # -x
                            self.cnt = 0
                    elif warrior.tileX > self.tileX and self.bg.mapli[self.tileY][self.tileX + 1] == 2:
                        for game_object in game_world.all_objects():
                            if game_object.type == 'mon':
                                check_monster_tileX, check_monster_tileY = game_object.return_loc()
                                if self.tileX + 1 == check_monster_tileX and self.tileY == check_monster_tileY:
                                    disrupt = 1
                        if disrupt == 0:
                            self.moveDir = 0  # +x
                            self.cnt = 0
                elif ((warrior.tileX - self.tileX) ** 2) == ((warrior.tileY - self.tileY) ** 2):  # =
                    if warrior.tileX < self.tileX:
                        if self.bg.mapli[self.tileY][self.tileX - 1] == 2:
                            for game_object in game_world.all_objects():
                                if game_object.type == 'mon':
                                    check_monster_tileX, check_monster_tileY = game_object.return_loc()
                                    if self.tileX - 1 == check_monster_tileX and self.tileY == check_monster_tileY:
                                        disrupt = 1
                            if disrupt == 0:
                                self.moveDir = 1  # -x
                                self.cnt = 0
                        else:
                            disrupt = 1
                    elif warrior.tileX > self.tileX:
                        if self.bg.mapli[self.tileY][self.tileX + 1] == 2:
                            for game_object in game_world.all_objects():
                                if game_object.type == 'mon':
                                    check_monster_tileX, check_monster_tileY = game_object.return_loc()
                                    if self.tileX + 1 == check_monster_tileX and self.tileY == check_monster_tileY:
                                        disrupt = 1
                            if disrupt == 0:
                                self.moveDir = 0  # +x
                                self.cnt = 0
                        else:
                            disrupt = 1
                    if disrupt == 1:
                        disrupt = 0
                        if warrior.tileY < self.tileY and self.bg.mapli[self.tileY - 1][self.tileX] == 2:
                            for game_object in game_world.all_objects():
                                if game_object.type == 'mon':
                                    check_monster_tileX, check_monster_tileY = game_object.return_loc()
                                    if self.tileX == check_monster_tileX and self.tileY - 1 == check_monster_tileY:
                                        disrupt = 1
                            if disrupt == 0:
                                self.moveDir = 3  # -y
                                self.cnt = 0
                        elif warrior.tileY > self.tileY and self.bg.mapli[self.tileY + 1][self.tileX] == 2:
                            for game_object in game_world.all_objects():
                                if game_object.type == 'mon':
                                    check_monster_tileX, check_monster_tileY = game_object.return_loc()
                                    if self.tileX == check_monster_tileX and self.tileY + 1 == check_monster_tileY:
                                        disrupt = 1
                            if disrupt == 0:
                                self.moveDir = 2  # +y
                                self.cnt = 0
                else:
                    if warrior.tileY < self.tileY and self.bg.mapli[self.tileY - 1][self.tileX] == 2:
                        for game_object in game_world.all_objects():
                            if game_object.type == 'mon':
                                check_monster_tileX, check_monster_tileY = game_object.return_loc()
                                if self.tileX == check_monster_tileX and self.tileY - 1 == check_monster_tileY:
                                    disrupt = 1
                        if disrupt == 0:
                            self.moveDir = 3  # -y
                            self.cnt = 0
                    elif warrior.tileY > self.tileY and self.bg.mapli[self.tileY + 1][self.tileX] == 2:
                        for game_object in game_world.all_objects():
                            if game_object.type == 'mon':
                                check_monster_tileX, check_monster_tileY = game_object.return_loc()
                                if self.tileX == check_monster_tileX and self.tileY + 1 == check_monster_tileY:
                                    disrupt = 1
                        if disrupt == 0:
                            self.moveDir = 2  # +y
                            self.cnt = 0
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.FAIL
        pass

    def move_to_warrior(self):
        self.state = 3
        if self.cnt < TILE_SIZE:
            if self.moveDir == 0:
                self.x += 1
                self.cnt += 1
            elif self.moveDir == 1:
                self.x -= 1
                self.cnt += 1
            elif self.moveDir == 2:
                self.y += 1
                self.cnt += 1
            elif self.moveDir == 3:
                self.y -= 1
                self.cnt += 1
            if self.moveDir == 5:
                self.cnt += 32
            self.moving = 1
        else:
            self.moving = 0
            self.turn = 0
            self.frame = 0
            self.state = 0
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time)
        if self.frame > 4:  # 조정해.
            self.frame = 1
        return BehaviorTree.SUCCESS

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
        self.cx, self.cy = self.x - (self.bg.window_left * 32), self.y - (self.bg.window_bottom * 32)
        self.tileX, self.tileY = (self.x - 16) // 32, (self.y - 16) // 32
        if self.turn == 1:
            self.bt.run()
        # print("monster : ", (self.y - 16) // 32, (self.x - 16) // 32, map.MapLi[self.tileY][self.tileX])
        if self.state == 0:
            self.timer = (self.timer + 1) % 1000
            if self.timer > 800:
                self.idl = 1
            else:
                self.idl = 0
        if self.state == 1:
            self.deadTimer += 1
            if self.deadTimer == 96:
                main_state.make_item(self.x, self.y)
                main_state.lvl_up()
                game_world.remove_object(self)
        if self.state == 2:
            self.atkTimer = (self.atkTimer + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time)
            if self.atkTimer < 5:  # 조정해.
                if self.atkTimer < 3:
                    self.atkPose = 1
                else:
                    self.atkPose = 2
            else:
                self.atkTimer = 0
                self.atkPose = 0
                self.state = 0

    def draw(self):
        if self.state == 0:  # 7 8 9 10  monster.timer // 250
            self.image.clip_draw(self.idl * self.dx, self.dir * self.dy, self.dx, self.dy, self.cx, self.cy, 32, 32)
        if self.state == 1:
            self.image.clip_draw((((self.deadTimer // 16) % 6) + 7) * self.dx, self.dir * self.dy, self.dx, self.dy, self.cx,
                                 self.cy, 32, 32)
        if self.state == 2:
            self.image.clip_draw((self.atkPose + 1) * self.dx, self.dir * self.dy, self.dx, self.dy, self.cx,
                                 self.cy, 32, 32)
        if self.state == 3:
            self.image.clip_draw((int(self.frame) + 3) * self.dx, self.dir * self.dy, self.dx, self.dy, self.cx,
                                 self.cy, 32, 32)

    def return_loc(self):
        return self.tileX, self.tileY

    def get_damage(self, damage):
        self.hp -= damage
        print("monster's HP:", self.hp)

    def dead(self):
        self.isDead = True

    def set_background(self, maps):
        self.bg = maps
