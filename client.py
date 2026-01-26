import socket
import threading

class NetworkClient:
    def __init__(self, host='127.0.0.1', port=5001):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = host
        self.port = port
        self.connected = False

        self.my_id = 0  # 1 (Czarny) lub 2 (Biały)
        self.board_str = "0" * 64  # Stan planszy w formie ciągu 64 znaków. Na starcie są same 0.
        self.turn = 1  # Oznaczenie, kto ma ruch (1 lub 2). 0 oznacza koniec gry. Zaczyna gracz 1.

    def connect(self):
        try:
            self.client.connect((self.host, self.port))     # Połączenie z serwerem
            self.connected = True
            # Wątek odbierający dane w tle
            threading.Thread(target=self.receive_messages, daemon=True).start()
            return True
        except Exception as e:
            print(f"Błąd połączenia: {e}")
            return False

    def receive_messages(self):
        while self.connected:
            try:
                data = self.client.recv(2048).decode('utf-8')
                if not data:
                    break

                msg = data.strip()
                parts = msg.split()

                if len(parts) > 0:
                    command = parts[0]

                    if command == "WELCOME":
                        # Format: WELCOME <id>
                        self.my_id = int(parts[1])
                        print(f"--- Połączono! Grasz jako gracz {self.my_id} ---")

                    elif command == "BOARD":
                        # Format: BOARD <64_znaki> <czyja_tura>
                        self.board_str = parts[1]
                        self.turn = int(parts[2])

            except Exception as e:
                print(f"Rozłączono: {e}")
                self.connected = False
                break

    def send_move(self, row, col):
        if self.connected:
            msg = f"MOVE {row} {col}"
            try:
                self.client.send(msg.encode('utf-8'))
            except Exception as e:
                print(f"Błąd wysyłania: {e}")

    def close(self):
        self.connected = False
        self.client.close()