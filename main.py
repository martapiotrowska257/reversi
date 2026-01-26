import pygame
import sys
from colors import *
from settings import *
from board import Board
from client import NetworkClient

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(TITLE)
        self.running = True
        self.clock = pygame.time.Clock()

        self.board = Board()

        self.network = NetworkClient()
        if not self.network.connect():
            print("Nie udało się połączyć z serwerem! Upewnij się, że server.py jest uruchomiony.")
            sys.exit()

    def run(self):  # Game loop
        while self.running:
            self.clock.tick(FPS)
            self.input()
            self.update()
            self.draw()

        self.network.close()
        pygame.quit()
        sys.exit()

    def input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                # Warunek bezpieczeństwa:
                # 1. Gra trwa (turn != 0)
                # 2. Jest TURA TEGO GRACZA (my_id == turn)
                if self.network.turn != 0 and self.network.my_id == self.network.turn:
                    mx, my = pygame.mouse.get_pos()
                    # przeliczamy kliknięcie na indeksy macierzy
                    col = (mx - self.board.start_x) // TILE_SIZE
                    row = (my - self.board.start_y) // TILE_SIZE

                    # sprawdzamy, czy kliknięcie jest wewnątrz planszy
                    if 0 <= row < ROWS and 0 <= col < COLS:
                        self.network.send_move(row, col)
                else:
                    if self.network.turn == 0:
                        print("Gra zakończona.")
                    elif self.network.my_id != self.network.turn:
                        print("Czekaj na swoją kolej!")

    def update(self):
        # 1. pobieramy stan planszy z sieci i aktualizujemy grafikę
        if self.network.board_str:
            self.board.update_from_string(self.network.board_str)

        # 2. Aktualizujemy tytuł okna (informacja dla gracza)
        turn = self.network.turn
        my_id = self.network.my_id

        if turn == 0:
            status = "KONIEC GRY"
        elif my_id == turn:
            status = "TWÓJ RUCH!"
        else:
            status = "Ruch przeciwnika..."

        color_name = "CZARNY" if my_id == 1 else "BIAŁY"
        pygame.display.set_caption(f"Reversi | Jesteś: {color_name} ({my_id}) | {status}")

    def draw(self):
        self.screen.fill(PINK)
        self.board.draw(self.screen)    # drawing the board
        pygame.display.flip()           # updating the screen

if __name__ == "__main__":
    game = Game()
    game.run()