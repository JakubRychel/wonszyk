import pygame
import random
from settings import *
from .snake import Snake
from .food import Food

class Game:
    def __init__(self):
        pygame.init()

        pygame.display.set_caption("Wonsz żeczny")

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()

        self.last_tick = pygame.time.get_ticks()
        self.tick_time = TICK_TIME

        self.running = True

        self.snake = Snake()
        self.food = Food(*self.get_free_position())

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                elif event.type == pygame.KEYDOWN:
                    if event.key in (pygame.K_UP, pygame.K_w):
                        self.snake.set_direction((0, -1))

                    elif event.key in (pygame.K_DOWN, pygame.K_s):
                        self.snake.set_direction((0, 1))

                    elif event.key in (pygame.K_LEFT, pygame.K_a):
                        self.snake.set_direction((-1, 0))

                    elif event.key in (pygame.K_RIGHT, pygame.K_d):
                        self.snake.set_direction((1, 0))

            now = pygame.time.get_ticks()
            
            if now - self.last_tick >= self.tick_time:
                self.update()
                self.last_tick = now

            self.draw()

            self.clock.tick(FPS)

        pygame.quit()

    def update(self):
        self.snake.move()

        if self.snake.check_wall_collision():
            print('Wonszyk użarł ścianę')
            self.running = False

        if self.snake.check_self_collision():
            print('Wonszyk sam się użarł')
            self.running = False

        head = self.snake.body[0]

        if head.x == self.food.x and head.y == self.food.y:
            self.food.x, self.food.y = self.get_free_position()

            return
        
        self.snake.pop()

    def draw(self):
        self.screen.fill(COLOR_BG)

        self.snake.draw(self.screen)
        self.food.draw(self.screen)

        pygame.display.flip()

    def get_free_position(self):
        all_positions = [(i % GRID_W, i // GRID_W) for i in range(GRID_W * GRID_H)]
        snake_positions = [(segment.x, segment.y) for segment in self.snake.body]

        free_positions = [position for position in all_positions if position not in snake_positions]

        return random.choice(free_positions)