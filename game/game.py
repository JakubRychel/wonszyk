import pygame
import random
from settings import *
from .snake import Snake
from .food import Food

class Game:
    def __init__(self):
        pygame.init()

        pygame.display.set_caption("Wonsz żeczny")

        self.font = pygame.font.SysFont('consolas', TILE)
        self.small_font = pygame.font.SysFont('consolas', TILE // 2)

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT + HUD_HEIGHT))
        self.clock = pygame.time.Clock()

        self.game_surface = pygame.Surface((WIDTH, HEIGHT))

        self.last_tick = pygame.time.get_ticks()
        self.tick_time = TICK_TIME

        self.state = 0 # 0 - gra, -1 - przegrana, 1 - wygrana

        self.snake = Snake()
        self.food = Food(*self.get_free_position())

    def run(self):
        running = True
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False

                    if event.key == pygame.K_r and self.state:
                        self.restart()

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
        if self.state:
            return

        self.snake.move()

        if self.snake.check_wall_collision():
            print('Wonszyk użarł ścianę')
            self.state = -1

        if self.snake.check_self_collision():
            print('Wonszyk sam się użarł')
            self.state = -1

        if len(self.snake.body) == GRID_W * GRID_H:
            print('🏆 TUDUDU TUDUDU (Wonszykowi dupa urosła duża)')
            self.state = 1

        head = self.snake.body[0]

        if head.x == self.food.x and head.y == self.food.y:
            self.food.x, self.food.y = self.get_free_position()

            return
        
        self.snake.pop()

    def restart(self):
        self.snake = Snake()
        self.food = Food(*self.get_free_position())

        self.state = 0
        self.last_tick = pygame.time.get_ticks()

    def draw(self):
        self.screen.fill(COLOR_EL)
        self.game_surface.fill(COLOR_BG)

        if self.state == 0:
            self.snake.draw(self.game_surface)
            self.food.draw(self.game_surface)

        else:
            text = self.small_font.render(
                'Naciśnij "R" aby zagrać ponownie',
                True,
                COLOR_EL
            )

            title = self.small_font.render(
                'wygrana' if self.state > 0 else 'przegrana',
                True,
                COLOR_EL
            )

            self.game_surface.blit(title, (WIDTH//2 - title.get_width()//2, HEIGHT//2 - 40))
            self.game_surface.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2))

        self.screen.blit(self.game_surface, (0, HUD_HEIGHT))

        length_text = self.font.render(
            f'Długość wonsza: {len(self.snake.body)}',
            True,
            COLOR_BG
        )

        self.screen.blit(length_text, (TILE * 0.25, TILE * 0.25))

        pygame.display.flip()

    def get_free_position(self):
        all_positions = [(i % GRID_W, i // GRID_W) for i in range(GRID_W * GRID_H)]
        snake_positions = [(segment.x, segment.y) for segment in self.snake.body]

        free_positions = [position for position in all_positions if position not in snake_positions]

        return random.choice(free_positions)