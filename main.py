import pygame
import sys
from colors import *
from settings import *
from board import Board

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(TITLE)
        self.running = True
        self.board = Board()

    def run(self):  # Game loop
        while self.running:
            self.input()
            self.update()
            self.draw()
        pygame.quit()
        sys.exit()

    def input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def update(self):
        pass

    def draw(self):
        self.screen.fill(DARK_GREY)
        self.board.draw(self.screen)    # drawing the board
        pygame.display.flip()           # updating the screen

if __name__ == "__main__":
    game = Game()
    game.run()