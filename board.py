import pygame
from colors import *
from settings import *

class Board:
    def __init__(self):
        self.start_x = (WIDTH - (COLS * TILE_SIZE)) // 2
        self.start_y = (HEIGHT - (ROWS * TILE_SIZE)) // 2

        # --- MODEL DANYCH (LOGIKA) ---
        # Tworzymy macierz 8 × 8 wypełnioną zerami.
        # 0 = puste pole, 1 = gracz czarny, 2 = gracz biały
        # To na tej strukturze będziemy opierać całą matematykę gry.
        self.board = [[0 for _ in range(COLS)] for _ in range(ROWS)]

        # Ustawiamy sytuację początkową
        self.setup_starting_position()

    def setup_starting_position(self):
        # Ustawienie "na sztywno" jest tylko dla startu gry.
        # W przyszłości każda inna zmiana na planszy będzie wynikała z akcji gracza,
        # ale technicznie będzie to dokładnie to samo: przypisanie liczby do komórki tablicy.

        # Środek planszy:
        # Zgodnie z zasadami:
        # Biały (2) na [3][3] i [4][4]
        # Czarny (1) na [3][4] i [4][3]
        self.board[3][3] = 2
        self.board[3][4] = 1
        self.board[4][3] = 1
        self.board[4][4] = 2

    def draw(self, window):
        # 1. Rysowanie tła
        pygame.draw.rect(window, GREEN, (self.start_x, self.start_y, COLS * TILE_SIZE, ROWS * TILE_SIZE))

        # 2. Rysowanie siatki
        self.draw_grid(window)

        # 3. Rysowanie pionków na podstawie macierzy
        self.draw_pieces(window)

    def draw_grid(self, window):
        for row in range(ROWS + 1):
            pygame.draw.line(window, BLACK,
                             (self.start_x, self.start_y + row * TILE_SIZE),
                             (self.start_x + COLS * TILE_SIZE, self.start_y + row * TILE_SIZE))

        for col in range(COLS + 1):
            pygame.draw.line(window, BLACK,
                             (self.start_x + col * TILE_SIZE, self.start_y),
                             (self.start_x + col * TILE_SIZE, self.start_y + ROWS * TILE_SIZE))

    def draw_pieces(self, window):
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]

                if piece != 0:
                    center_x = self.start_x + col * TILE_SIZE + TILE_SIZE // 2
                    center_y = self.start_y + row * TILE_SIZE + TILE_SIZE // 2
                    radius = TILE_SIZE // 2 - 5  # -5 żeby pionek nie stykał się z linią

                    if piece == 1:
                        pygame.draw.circle(window, BLACK, (center_x, center_y), radius)
                    elif piece == 2:
                        pygame.draw.circle(window, WHITE, (center_x, center_y), radius)