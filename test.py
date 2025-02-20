# -*- coding: utf-8 -*-
import sys

import pygame
import random


from pygame.locals import *


# ========== 常量定义 ==========
FPS = 30  # 帧率
WINDOW_WIDTH = 640  # 窗口宽度
WINDOW_HEIGHT = 480  # 窗口高度
FOOD_SIZE = 10 # 食物方块大小
SNAKE_SIZE = 14 # 蛇body方块大小
BLOCK_SIZE = 16 # 地图方块大小
# 颜色定义（RGB）
WHITE = (255, 255, 255)
NAVY_BLUE = (60, 60, 100)
BLUE = (0, 0, 255)
FOOD_COLOR = (123, 123, 123)
# ========== 初始化窗口 ==========
DISPLAY_SURF = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))



class Timer:
    def __init__(self):
        self.running = False
        self.time = 1000
        self.tick1 = pygame.time.get_ticks()
        self.tick2 = pygame.time.get_ticks()

    def is_out(self):
        if self.tick2 - self.tick1 > self.time:
            self.tick1 = self.tick2
            return True
        return False

    def update(self):
        if self.running:
            self.tick2 = pygame.time.get_ticks()

    def set_time(self, time, is_open):
        self.time = time
        self.running = is_open


class Food:
    def __init__(self):
        self.image = pygame.Surface((FOOD_SIZE, FOOD_SIZE))
        self.image.fill(FOOD_COLOR)
        self.rect = self.image.get_rect()
        self.x = random.randrange(1, WINDOW_WIDTH // (BLOCK_SIZE + 2) - 4)
        self.y = random.randrange(1, WINDOW_HEIGHT // (BLOCK_SIZE + 2))
        self.rect.top = self.y * (2 + 8) + (self.y - 1) * 8 - 5
        self.rect.left = self.x * (2 + 8) + (self.x - 1) * 8 - 5
        self.is_live = True
        print(self.x)
        print(self.y)

    def draw(self, food_screen):
        food_screen.blit(self.image, self.rect)
    def update(self):
        pass


class Snake:
    def __init__(self):
        self.is_live = True
        self.body = []
        self.head = [3, 3]
        self.speed = 1
        self.size = 1
        self.time = 500
        self.direction = 1
        self.image = pygame.Surface((SNAKE_SIZE, SNAKE_SIZE))
        self.rect = self.image.get_rect()
        self.image.fill(WHITE)
        self.body.append(self.head)
        self.timer = Timer()
        self.timer.set_time(self.time, True)
        self.score = 0

    def update(self, key, food):
        if self.is_live:
            self.head = self.body[self.size - 1]
            new_head = self.head[:]
            if key[K_LEFT] and self.direction != 1:
                self.direction = 0
            if key[K_RIGHT] and self.direction != 0:
                self.direction = 1
            if key[K_UP] and self.direction != 3:
                self.direction = 2
            if key[K_DOWN] and self.direction != 2:
                self.direction = 3

            if self.timer.is_out():
                if self.direction == 0:
                    new_head[0] -= self.speed
                elif self.direction == 1:
                    new_head[0] += self.speed
                elif self.direction == 2:
                    new_head[1] -= self.speed
                elif self.direction == 3:
                    new_head[1] += self.speed
                if self.head[0] == food.x and self.head[1] == food.y:
                    food.is_live = False
                    self.body.append([food.x, food.y])
                    self.size += 1
                    self.score += 1
                else:
                    self.body.append(new_head)
                    self.body.pop(0)
            if new_head[0] > WINDOW_WIDTH // (BLOCK_SIZE + 2) - 4 or new_head[0] <= 0 or new_head[1] > WINDOW_HEIGHT // (BLOCK_SIZE + 2) or new_head[1] <= 0:
                self.is_live = False

        print(self.is_live)
        print(self.body)


class Map:
    def __init__(self):
        self.gap = 2
        self.col = WINDOW_WIDTH // (BLOCK_SIZE + self.gap) - 4
        self.row = WINDOW_HEIGHT // (BLOCK_SIZE + self.gap)
        self.image = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
        self.image.fill((12, 25, 58))
        self.rect = self.image.get_rect()
        self.delta_block = BLOCK_SIZE // 2  # 8
        self.delta_snake = SNAKE_SIZE // 2  # 7

    def draw(self, screen, snake):
        # screen.blit(self.image, (2, 2))
        for i in range(self.col):
            for j in range(self.row):
                screen.blit(self.image,
                            (self.gap + (self.gap + BLOCK_SIZE) * i, self.gap + (self.gap + BLOCK_SIZE) * j))
        for k in snake.body:
            screen.blit(snake.image,
                        (k[0] * (self.gap + self.delta_block) + (k[0] - 1) * self.delta_block - self.delta_snake,
                         k[1] * (self.gap + self.delta_block) + (k[1] - 1) * self.delta_block - self.delta_snake))


class Ui:
    def __init__(self, fnot):
        self.info = 'Ui'
        self.font = fnot
    def ui(self, num):
        text = f"score:{num}"
        DISPLAY_SURF.blit(self.font.render(text, True, WHITE), (10, 10))


class Game:
    def __init__(self):
        # 初始化Pygame库
        pygame.init()
        self.snake = Snake()
        self.my_map = Map()
        self.food = Food()
        self.font = pygame.font.SysFont("comicsans", 30)
        self.text = self.font.render("GAME OVER", True, WHITE)
        self.ui = Ui(self.font)
        pygame.display.set_caption('贪吃蛇呢')
        self.clock = pygame.time.Clock()
    def run(self):
        while True:
            DISPLAY_SURF.fill(NAVY_BLUE)

            for event in pygame.event.get():
                if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                    pygame.quit()
                    sys.exit()

            if self.food.is_live is False:
                food = Food()

            if self.snake.is_live:
                self.snake.timer.update()
                self.snake.update(pygame.key.get_pressed(), self.food)
                self.my_map.draw(DISPLAY_SURF, self.snake)
                self.food.draw(DISPLAY_SURF)
                self.ui.ui(self.snake.score)
            else:
                DISPLAY_SURF.fill(BLUE)
                DISPLAY_SURF.blit(self.text, (200, 200))
            pygame.display.update()  # 更新屏幕显示
            self.clock.tick(FPS)  # 控制帧率


if __name__ == '__main__':
    game = Game()
    game.run()
