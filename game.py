from game_res_load import *
import pygame



POWER = -15
G = 0.7
FLOOR = 330 #暂时替代地面的y值，后面用碰撞来实现地面
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.jump_h = None
        self.image = pygame.image.load('data/images/player.png')
        self.rect = self.image.get_rect()
        self.rect.top = y
        self.rect.left = x
        self.speedx = 0
        self.speedy = 0
        self.on_floor = True

    def _l_r_move(self):
        """
        左右移动
        :return:
        """
        self.rect.x += self.speedx
        self.speedx = 0

    def _jump(self):
        """
        跳跃
        :return:
        """
        if self.on_floor:
            self.speedy = POWER
            self.on_floor = False

    def _g_move(self, scene):
        """
        重力作用下移动，平台鹏碰撞检测
        :return:
        """
        self.rect.y += self.speedy
        self.speedy += G
        for collision in pygame.sprite.spritecollide(self, scene.platforms, False):
            # print(collision)
            if self.speedy > 0:
                self.rect.bottom = collision.rect.top
                self.on_floor = True
                self.speedy = 0

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def update(self, key, scene):
        if key[pygame.K_LEFT]:
            self.speedx = -5
        if key[pygame.K_RIGHT]:
            self.speedx = 5
        if key[pygame.K_SPACE]:
            self._jump()

        self._g_move(scene)
        self._l_r_move()

PLATFORM_RGB = (12, 23, 200)

class Platform(pygame.sprite.Sprite):
    def __init__(self,x, y, width, height):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((width, height))
        self.image.fill(PLATFORM_RGB)
        self.rect = self.image.get_rect()
        self.rect.left = x
        self.rect.top = y

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def update(self):
        pass

MOVE_PLATFORM_RGB = (56, 45, 99)
class MovePlatform(Platform):
    def __init__(self, x, y, width, height, speed, move_range):
        Platform.__init__(self, x, y, width, height)
        self.image.fill(MOVE_PLATFORM_RGB)
        self.speed = speed
        self.move_range = move_range

    def update(self):
        self._move()

    def _move(self):
        self.rect.x += self.speed
        if self.rect.left < self.move_range[0] or self.rect.right > self.move_range[1]:
            self.speed = -self.speed

GOAL_RGB = (12, 215, 65)
class Goal(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((64, 64))
        self.image.fill(GOAL_RGB)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.live = True
        self.timer = Timer()
        self.timer.set_time(50, True)
        self.color = [0, 0, 0]

    def draw(self, screen):
        if self.timer.is_time_out():
            self.color[0] = (self.color[0] + 10) % 256
            self.color[1] = (self.color[1] + 1) % 256
            self.color[2] = (self.color[2] + 5) % 256
            self.image.fill((self.color[0], self.color[1], self.color[2]))
        screen.blit(self.image, self.rect)
    def update(self, key, scene):
        self.timer.update()
        pass

ITEM_RGB = (2, 12, 250)
class Item(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((64, 64))
        self.image.fill(ITEM_RGB)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def update(self):
        pass

HEALTH_RGB = (66, 66, 66)
class HealthItem(Item):
    def __init__(self, x, y):
        Item.__init__(self, x, y)
        self.health = 20
        self.image = pygame.Surface((64, 64))
        self.image.fill(HEALTH_RGB)
ENEMY_RGB = (66, 77, 88)
class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, enemy_range):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((32, 64))
        self.image.fill(ENEMY_RGB)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 1
        self.enemy_range = enemy_range

    def update(self):
        pass
    def draw(self, screen):
        screen.blit(self.image, self.rect)

PatrolEnemy_RGB = (12, 88, 99)
class PatrolEnemy(Enemy):
    def __init__(self, x, y, enemy_range):
        super().__init__(x, y, enemy_range)
        self.image.fill(PatrolEnemy_RGB)

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def update(self):
        self.rect.x += self.speed
        if self.rect.left < self.enemy_range[0] or self.rect.right > self.enemy_range[1]:
            self.speed = -self.speed
            pass
class Timer:
    def __init__(self):
        self.time_on = False
        self.tick1 = pygame.time.get_ticks()
        self.tick2 = 0
        self.time = 1000
    def is_time_out(self):
        if self.tick2 - self.tick1 > self.time:
            self.tick1 = pygame.time.get_ticks()
            return True
        return False

    def update(self):
        if self.time_on:
            self.tick2 = pygame.time.get_ticks()

    def set_time(self, time, is_open):
        self.time = time
        self.time_on = is_open

# 定义不同状态的scene实例
class Scene:
    def __init__(self, data):
        self.all_sprites = pygame.sprite.Group()
        self.platforms = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.items = pygame.sprite.Group()
        self.set_up(data)
        self.player_pos = (data['player']['x'], data['player']['y'])
        self.goal_pos = (data['goal']['x'], data['goal']['y'])


    def set_up(self, data):
        for platform in data['platforms']:
            if platform['type'] == 'static_platform':
                self.add_in_platform(Platform(platform['x'], platform['y'], platform['width'], platform['height']))
                pass
            if platform['type'] == 'moving_platform':
                self.add_in_platform(MovePlatform(platform['x'], platform['y'], platform['width'], platform['height'], platform['speed'], platform['move_range']))
                pass
        for enemy in data['enemies']:
            if enemy['type'] == 'patrol':
                self.add_in_enemies(PatrolEnemy(enemy['x'], enemy['y'], enemy['move_range']))
                pass
            if enemy['type'] == 'shooter':
                pass
        for item in data['items']:
            if item['type'] == 'health':
                self.add_in_items(HealthItem(item['x'], item['y']))
                pass
            if item['type'] == 'gun':
                pass

    def update(self, player):
        self.all_sprites.update()
        # 玩家与敌人的碰撞检测
        for c in pygame.sprite.spritecollide(player, self.enemies, False):
            if player.rect.bottom < c.rect.bottom:
                print("上")
            elif player.rect.top > c.rect.top:
                print("下")

        # 玩家与item道具的碰撞检测
        if pygame.sprite.spritecollide(player, self.items, False):
            pass
        # 玩家与子弹的碰撞检测


    def draw(self, screen):
        self.all_sprites.draw(screen)

    def add_in_all_object(self, obj):
        self.all_sprites.add(obj)
    def add_in_platform(self, obj):
        self.platforms.add(obj)
        self.add_in_all_object(obj)
    def add_in_enemies(self, obj):
        self.enemies.add(obj)
        self.add_in_all_object(obj)
    def add_in_items(self, obj):
        self.items.add(obj)
        self.add_in_all_object(obj)


FONT_PATH = ''

# 定义game状态机
class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((800, 600))
        self.clock = pygame.time.Clock()
        self.scenes = []
        self.current_scene_state = 0
        self.key = pygame.key.get_pressed()
        self.player = Player(0, 0)
        self.goal = Goal(0, 0)
        self.last_time = 0
        self.timer = Timer()
        # 加载字体
        try:
            self.font = pygame.font.Font(FONT_PATH, 36)
            self.big_font = pygame.font.Font(FONT_PATH, 74)
        except FileNotFoundError:
            print("警告：字体文件未找到，使用默认字体")
            self.font = pygame.font.Font(None, 36)
            self.big_font = pygame.font.Font(None, 74)
        self._set_up()

    def _set_up(self):
        """
        初始化scenes属性，将json文件中的数据，实例化。
        :return:
        """
        scene_list = load_scenes(os.path.dirname(__file__))# 返回json数据格式
        for sc in scene_list:
            self.scenes.append(Scene(sc))
        self._set_position()
        self.timer.set_time(1000, True)

    def load_scene(self, scene_num):
        self.current_scene_state = scene_num - 1
        if self.current_scene_state > len(self.scenes) - 1:
            self.current_scene_state = 0
        self._set_position()

    def _set_position(self):
        self.player.rect.x = self.scenes[self.current_scene_state].player_pos[0]
        self.player.rect.y = self.scenes[self.current_scene_state].player_pos[1]
        self.goal.rect.x = self.scenes[self.current_scene_state].goal_pos[0]
        self.goal.rect.y = self.scenes[self.current_scene_state].goal_pos[1]

    # 游戏主循环
    def run(self):
        while True:
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_ESCAPE:
                        pygame.quit()
                        exit()

            self.key = pygame.key.get_pressed()
            self.update()
            self.draw()
            self.clock.tick(90)
            pygame.display.flip()

    # 更新所有,包括game逻辑
    def update(self):
        # 定时器更新
        self.timer.update()
        # 场景更新
        self.scenes[self.current_scene_state].update(self.player)
        # 玩家和通关标志更新
        self.player.update(self.key, self.scenes[self.current_scene_state])
        self.goal.update(self.key, self.scenes[self.current_scene_state])
        self.check_player_goal_coll() # 玩家与goal的碰撞检测
        #玩家与platform的碰撞检测卸载player的移动函数中
        #玩家与item等元素的碰撞检测，写在场景中


    # 检查player和goal是否碰撞，然后场景下一个
    def check_player_goal_coll(self):
        if pygame.sprite.collide_mask(self.player, self.goal):
            self.load_scene(self.current_scene_state + 2)

    # 绘制所有
    def draw(self):
        if self.timer.is_time_out():
            print("一秒时间到!")
        # 背景
        self.screen.fill((255, 255, 255))
        # 场景
        self.scenes[self.current_scene_state].draw(self.screen)
        # 玩家
        self.player.draw(self.screen)
        # goal
        self.goal.draw(self.screen)


if __name__ == '__main__':
    pygame.init()
    game = Game()
    game.run()
