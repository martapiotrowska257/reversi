# Reversi - Gra Sieciowa (Programowanie Współbieżne)

**Autor:** Marta Piotrowska  
**Przedmiot:** Programowanie Współbieżne  
**Temat:** Zadanie 11 - Gra Reversi w architekturze klient-serwer.

---

## 1. Treść Zadania (Opis Wariantu)

Projekt realizuje grę strategiczną **Reversi** dla dwóch osób rozgrywaną na planszy o wymiarach 8x8.

### Zasady gry:
* **Początek:** Na środku planszy znajdują się dwa białe i dwa czarne pionki w układzie diagonalnym.
* **Przebieg:** Gracze na zmianę stawiają pionki swojego koloru (Czarny lub Biały). Ruch jest dozwolony tylko wtedy, gdy otacza (w poziomie, pionie lub po skosie) co najmniej jeden pionek przeciwnika.
* **Przejmowanie:** Otoczone pionki przeciwnika zmieniają kolor na kolor gracza wykonującego ruch.
* **Brak ruchu:** Jeśli gracz nie może wykonać ruchu, traci kolejkę.
* **Koniec gry:** Gra kończy się, gdy plansza zostanie zapełniona lub żaden z graczy nie może wykonać ruchu. Wygrywa osoba z większą liczbą pionków na planszy.

---

## 2. Instrukcja Uruchomienia

Projekt został napisany w języku **Python**. Do obsługi interfejsu graficznego wykorzystano bibliotekę **Pygame**, a do komunikacji sieciowej standardową bibliotekę **socket**.

### Wymagania
* Python 3.x
* Biblioteka Pygame

### Instalacja zależności
Przed uruchomieniem upewnij się, że masz zainstalowaną bibliotekę `pygame`. Możesz to zrobić komendą:

```bash
pip install pygame
```

### Uruchamienie gry

Gra działa w architekturze klient-serwer. Należy uruchomić procesy w następującej kolejności:

1. **Uruchom serwer:**
   ```bash
   python server.py
   ```
   
   Serwer nasłuchuje na `localhost` (127.0.0.1) na porcie `5001`.


2. **Uruchom pierwszego klienta (Gracz 1 - Czarny):**
   ```bash
   python main.py
   ```

3. **Uruchom drugiego klienta (Gracz 2 - Biały):**
   ```bash
   python main.py
   ```
   
##  3. Sterowanie
* Użyj myszy, aby kliknąć na pole, na którym chcesz postawić pionek.
* Gra automatycznie przełącza się między graczami po każdym ruchu.
* Wynik jest wyświetlany w konsoli po zakończeniu gry.