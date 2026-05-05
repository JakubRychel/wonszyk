import pygame
from settings import *

class Food:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def draw(self, screen):
        x = self.x * TILE
        y = self.y * TILE

        cell_size = (TILE - 4) // 3

        for i in (1, 3, 5, 7):
            pygame.draw.rect(
                screen,
                COLOR_EL,
                (x + i % 3 * (cell_size + 1) + 1, y + i // 3 * (cell_size + 1) + 1, cell_size, cell_size)
            )