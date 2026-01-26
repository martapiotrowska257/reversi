class ReversiLogic:
    def __init__(self):
        self.rows = 8
        self.cols = 8
        # 0 = puste, 1 = czarny, 2 = biały
        self.board = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
        self.turn = 1  # 1 zaczyna (czarny)
        self.setup_board()

    def setup_board(self):
        # Ustawienie początkowe
        # Biały (2) na [3][3] i [4][4], Czarny (1) na [3][4] i [4][3]
        self.board[3][3], self.board[3][4] = 2, 1
        self.board[4][3], self.board[4][4] = 1, 2

    def get_board_string(self):
        """Zamienia planszę na ciąg znaków dla sieci (np. '00012...')"""
        s = ""
        for r in range(self.rows):
            for c in range(self.cols):
                s += str(self.board[r][c])
        return s

    def is_on_board(self, r, c):
        return 0 <= r < self.rows and 0 <= c < self.cols

    def get_valid_moves(self, player):
        """Zwraca listę (row, col) poprawnych ruchów dla danego gracza"""
        moves = []
        enemy = 2 if player == 1 else 1
        directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1),
                      (0, 1), (1, -1), (1, 0), (1, 1)]

        for r in range(self.rows):
            for c in range(self.cols):
                if self.board[r][c] != 0:
                    continue

                # sprawdzamy, czy ruch otoczy wroga w którymś z kierunków
                for dr, dc in directions:
                    nr, nc = r + dr, c + dc
                    if self.is_on_board(nr, nc) and self.board[nr][nc] == enemy:
                        while self.is_on_board(nr, nc) and self.board[nr][nc] == enemy:
                            nr += dr
                            nc += dc
                        if self.is_on_board(nr, nc) and self.board[nr][nc] == player:
                            moves.append((r, c))
                            break  # Wystarczy jeden ważny kierunek
        return moves

    def apply_move(self, r, c, player):
        """Stawia pionek i odwraca kolory przejętych pionków"""
        if (r, c) not in self.get_valid_moves(player):
            return False

        self.board[r][c] = player
        enemy = 2 if player == 1 else 1
        directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1),
                      (0, 1), (1, -1), (1, 0), (1, 1)]

        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            pieces_to_flip = []
            while self.is_on_board(nr, nc) and self.board[nr][nc] == enemy:
                pieces_to_flip.append((nr, nc))
                nr += dr
                nc += dc

            if self.is_on_board(nr, nc) and self.board[nr][nc] == player:
                for fr, fc in pieces_to_flip:
                    self.board[fr][fc] = player
        return True

    def handle_turn_change(self):
        """Zmienia turę, uwzględniając brak ruchów (pass)"""
        next_player = 2 if self.turn == 1 else 1

        # Sprawdzamy, czy następny gracz ma ruchy
        if self.get_valid_moves(next_player):
            self.turn = next_player
        else:
            # Jeśli nie ma ruchu, kolejka wraca do obecnego gracza (chyba że też nie ma ruchu, wtedy jest koniec gry)
            #  "traci kolejkę i wykonuje go drugi gracz"
            if not self.get_valid_moves(self.turn):
                self.turn = 0  # 0 oznacza koniec gry
            else:
                print(f"Gracz {next_player} nie ma ruchu. Tura zostaje u {self.turn}.")

    def check_winner(self):
        """Liczy punkty i zwraca wynik"""
        p1 = sum(row.count(1) for row in self.board)
        p2 = sum(row.count(2) for row in self.board)

        if p1 > p2:
            return f"Wygrał CZARNY: ${p1} do {p2}"
        elif p2 > p1:
            return f"Wygrał BIAŁY : ${p2} do {p1}"
        else:
            return "REMIS"