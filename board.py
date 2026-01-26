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
        self.board = [[0 for _ in range(COLS)] for _ in range(ROWS)]
        self.setup_starting_position()
        self.font = pygame.font.SysFont('Arial', 24, bold=True)

    def setup_starting_position(self):
        # Zgodnie z zasadami: Biały (2) na [3][3] i [4][4], Czarny (1) na [3][4] i [4][3]
        self.board[3][3] = 2
        self.board[3][4] = 1
        self.board[4][3] = 1
        self.board[4][4] = 2

    def draw(self, window):
        pygame.draw.rect(window, GREEN, (self.start_x, self.start_y, COLS * TILE_SIZE, ROWS * TILE_SIZE))
        self.draw_grid(window)
        self.draw_labels(window)
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

    def draw_labels(self, window):
        # Litery A-H (kolumny)
        letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
        for col in range(COLS):
            text = self.font.render(letters[col], True, BLACK)
            # Pozycja nad planszą
            window.blit(text,
                        (self.start_x + col * TILE_SIZE + TILE_SIZE // 2 - text.get_width() // 2,
                         self.start_y - 30))
            # Pozycja pod planszą
            window.blit(text, (self.start_x + col * TILE_SIZE + TILE_SIZE // 2 - text.get_width() // 2,
                               self.start_y + ROWS * TILE_SIZE + 10))

        # Cyfry 1-8 (wiersze)
        for row in range(ROWS):
            text = self.font.render(str(row + 1), True, BLACK)
            # Pozycja z lewej strony
            window.blit(text,
                        (self.start_x - 30,
                         self.start_y + row * TILE_SIZE + TILE_SIZE // 2 - text.get_height() // 2))
            # Pozycja z prawej strony
            window.blit(text,
                        (self.start_x + COLS * TILE_SIZE + 30 - text.get_width(),
                         self.start_y + row * TILE_SIZE + TILE_SIZE // 2 - text.get_height() // 2))

    def draw_pieces(self, window):
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]

                if piece != 0:
                    center_x = self.start_x + col * TILE_SIZE + TILE_SIZE // 2
                    center_y = self.start_y + row * TILE_SIZE + TILE_SIZE // 2
                    radius = TILE_SIZE // 2 - 5  # -5, żeby pionek nie stykał się z linią

                    if piece == 1:
                        pygame.draw.circle(window, BLACK, (center_x, center_y), radius)
                    elif piece == 2:
                        pygame.draw.circle(window, WHITE, (center_x, center_y), radius)