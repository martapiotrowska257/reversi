import pygame
from colors import *
from settings import *

class Board:
    def __init__(self):
        self.start_x = (WIDTH - (COLS * TILE_SIZE)) // 2
        self.start_y = (HEIGHT - (ROWS * TILE_SIZE)) // 2

    def draw(self, window):
        pygame.draw.rect(window, WHITE, (self.start_x, self.start_y, COLS * TILE_SIZE, ROWS * TILE_SIZE))

        for row in range(ROWS + 1):
            pygame.draw.line(window, BLACK,
                             (self.start_x, self.start_y + row * TILE_SIZE),
                             (self.start_x + COLS * TILE_SIZE, self.start_y + row * TILE_SIZE))

        for col in range(COLS + 1):
            pygame.draw.line(window, BLACK,
                             (self.start_x + col * TILE_SIZE, self.start_y),
                             (self.start_x + col * TILE_SIZE, self.start_y + ROWS * TILE_SIZE))