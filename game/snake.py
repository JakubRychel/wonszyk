import pygame
from settings import *

class Segment:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def draw(self, screen):
        x = self.x * TILE
        y = self.y * TILE

        cell_size = (TILE - 4) // 3

        for i in range(9):
            pygame.draw.rect(
                screen,
                COLOR_EL,
                (x + i % 3 * (cell_size + 1), y + i // 3 * (cell_size + 1), cell_size, cell_size)
            )

class Snake:
    def __init__(self):
        self.body = [
            Segment(15, 10)
        ]
        self.direction = (0, -1)
        self.next_direction = self.direction

    def draw(self, screen):
        for tile in self.body:
            tile.draw(screen)

    def move(self):
        self.direction = self.next_direction

        head = self.body[0]

        new_head = Segment(
            head.x + self.direction[0],
            head.y + self.direction[1]
        )

        self.body.insert(0, new_head)

    def pop(self):
            self.body.pop()

    def set_direction(self, new_direction):
        if new_direction == (-self.direction[0], -self.direction[1]):
            return

        self.next_direction = new_direction

    def check_wall_collision(self):
        head = self.body[0]

        return (
            head.x < 0 or
            head.x >= GRID_W or
            head.y < 0 or
            head.y >= GRID_H
        )
    
    def check_self_collision(self):
        head = self.body[0]

        return any(
            segment.x == head.x and segment.y == head.y
            for segment in self.body[1:]
        )