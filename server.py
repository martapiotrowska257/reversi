import socket
import threading
from logic import ReversiLogic

HOST = '127.0.0.1'
PORT = 5001
BUFSIZE = 1024

game = ReversiLogic()
clients = []

def broadcast_game_state():
    """Wysyła stan do wszystkich: BOARD <string> <czyja_tura>"""
    msg = f"BOARD {game.get_board_string()} {game.turn}"

    if game.turn == 0:
        winner_msg = game.check_winner()
        print(f"Koniec gry: {winner_msg}")

    for client in clients:
        try:
            client.send(msg.encode('utf-8'))
        except:
            clients.remove(client)


def handle_client(conn, addr, player_id):
    print(f"Nowy gracz {player_id} połączony: {addr}")

    # Protokół: WELCOME <id>
    conn.send(f"WELCOME {player_id}".encode('utf-8'))
    # Wyślij aktualny stan
    conn.send(f"BOARD {game.get_board_string()} {game.turn}".encode('utf-8'))

    while True:
        try:
            data = conn.recv(BUFSIZE)
            if not data:
                break

            msg = data.decode('utf-8').strip()

            if msg.startswith("MOVE"):
                parts = msg.split()
                if len(parts) == 3:
                    r, c = int(parts[1]), int(parts[2])

                    # sprawdzenie, czy to tura tego gracza
                    if game.turn == player_id:
                        if game.apply_move(r, c, player_id):
                            print(f"Ruch gracza {player_id}: {r},{c}")
                            game.handle_turn_change()  # Zmiana tury (lub pass)
                            broadcast_game_state()
                        else:
                            print(f"Niepoprawny ruch gracza {player_id} na {r},{c}")
                    else:
                        print(f"Gracz {player_id} próbował ruszyć poza kolejką.")

        except ConnectionResetError:
            break
        except Exception as e:
            print(f"Błąd gracza {player_id}: {e}")
            break

    print(f"Gracz {player_id} rozłączony.")
    if conn in clients:
        clients.remove(conn)
    conn.close()


def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(2)    # Nie może być więcej niż 2 graczy (2 to długość kolejki)
    server.settimeout(1.0)  # Ustawienie timeoutu: accept() będzie rzucać wyjątek co sekundę, jeśli nikt się nie połączy
    print("Serwer Reversi (z Logic) wystartował... (Naciśnij Ctrl+C aby zatrzymać)")

    player_count = 0

    try:
        while True:
            try:
                conn, addr = server.accept()
            except socket.timeout:
                # Upłynęła sekunda, nikt się nie połączył. Pętla wraca na początek,
                # dzięki czemu Python może sprawdzić, czy nie naciśnięto Ctrl+C.
                continue
            except OSError:
                # Obsługa sytuacji, gdy socket zostanie nagle zamknięty
                break

            player_count += 1
            if player_count <= 2:
                clients.append(conn)
                thread = threading.Thread(target=handle_client, args=(conn, addr, player_count))
                # Ważne: daemon threads zginą, gdy główny program się zakończy
                thread.daemon = True
                thread.start()
            else:
                conn.send("FULL".encode('utf-8'))
                conn.close()

    except KeyboardInterrupt:
        print("\nZatrzymywanie serwera...")
    finally:
        server.close()
        print("Serwer zamknięty.")


if __name__ == "__main__":
    main()