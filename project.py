from pyfiglet import Figlet
import os
import shutil
import random
import time
import msvcrt
import copy
import winsound

HEIGHT_SEPARATION = 3
DIRECTIONS = {
    b'w': (0, -1),
    b's': (0, 1),
    b'a': (-1, 0),
    b'd': (1, 0),
}
STATE_MENU      = "menu"
STATE_PLAY      = "play"
STATE_GAME_OVER = "game_over"
STATE_EXIT      = "exit"
AUDIO = {
    "Explosion": "Audio/Explosion.wav",
    "Pickup_Coin": "Audio/Pickup_Coin.wav",
    "Blip_Select": "Audio/Blip_Select.wav"
}

class Snake():
    def __init__(self, pos: list[int, int], board: "Board"):
        self.dead: bool = False
        self.score: int = 0
        self.size: int = 3
        self.movements: list = []
        self.c_pos: list[int, int] = pos
        self.set_pos(board)

    def set_pos(self, board: "Board") -> None:
        for pos in self.movements:
            board.set_cell(pos[0], pos[1], "▓")

    def add_movement(self, n_pos: tuple[int, int]) -> None:
        self.movements.append(copy.deepcopy(n_pos))

    def remove_movement(self, n_pos: tuple[int, int]) -> None:
        try:
            self.movements.remove(n_pos)
        except ValueError:
            raise ValueError("No se encontró movimiento en la cola")

    def handle_movement(self, board: "Board", fruit: "Fruit", direction: tuple[int, int]) -> None:
        self.c_pos[0] += direction[0] 
        self.c_pos[1] += direction[1]
        
        if self.c_pos == list(fruit.pos):
            fruit.set_fruit(board, self)
            fruit.eat_fruit(self)
        
        if self.c_pos in self.movements or board.get_cell(self.c_pos) == " ":
            self.dead = True
            return

        self.move(board)

    def is_dead(self):
        if self.dead:
            return True
        return False

    def move(self, board: "Board") -> None:
        s = len(self.movements)
        if s <= self.size:
            self.add_movement(self.c_pos)
        if s == self.size:
            self.remove_movement(self.movements[0])
        self.set_pos(board)
        

class Fruit():
    def __init__(self, board: "Board", snake: "Snake"):
        self.pos: tuple[int, int] = (0, 0)
        self.points = 100
        self.just_eated: bool = False
        self.set_fruit(board, snake)

    def update_pos(self, board: "Board") -> None:
        board.set_cell(self.pos[0], self.pos[1], "#")

    def set_fruit(self, board: "Board", snake: "Snake") -> None:
        pos = self.choose_pos(board, snake)
        board.set_cell(pos[0], pos[1], "#")
        self.pos = pos

    def eat_fruit(self, snake: "Snake") -> None:
        winsound.PlaySound(AUDIO["Pickup_Coin"], winsound.SND_FILENAME | winsound.SND_ASYNC)
        snake.score += self.points
        snake.size += 1
        self.just_eated = True

    def choose_pos(self, board: "Board", snake: "Snake") -> tuple[int, int]:
        x, y = (random.randint(0, board.width - 1), random.randint(0, board.height - 1))
        if [x, y] in snake.movements:
            return self.choose_pos(board, snake)
        return (x, y)

class Board():
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.grid = [["░" for _ in range(width)] for _ in range(height)]

    def __str__(self) -> str:
        return "\n".join("".join(row) for row in self.grid)

    def set_cell(self, x: int, y: int, type: str):
        if not (-1 < x < self.width and -1 < y < self.height):
            raise ValueError(f"Se intento entrar a una casilla a fuera del tablero ({y, x})")
        self.grid[y][x] = type

    def get_cell(self, pos: tuple[int, int]) -> str:
        if not (-1 < pos[0] < self.width and -1 < pos[1] < self.height):
            return " "
        return self.grid[pos[1]][pos[0]]

    def clear(self):
        for i in range(self.height):
            for j in range(self.width):
                self.grid[i][j] = "░"


def center_output(output: str) -> str:
    terminal_size = shutil.get_terminal_size(fallback=(80, 24))

    lines = output.splitlines()
    max_width = max(len(line) for line in lines)

    left_padding = max((terminal_size.columns - max_width) // 2, 0)

    centered_lines = [(" " * left_padding) + line for line in lines]
    return "\n".join(centered_lines)

def set_text(text: str) -> str:
    figlet = Figlet()
    figlet.setFont(font="doom")
    return figlet.renderText(text)

def set_title(text: str) -> str:
    return center_output(set_text(text))

def clear_screen():
    os.system('cls')

def main():
    state = STATE_MENU

    while state != STATE_EXIT:
        if state == STATE_MENU:
            state = menu_principal()

        elif state == STATE_PLAY:
            state = play_loop()

        elif state == STATE_GAME_OVER:
            state = menu_game_over()

    print(center_output("¡Gracias por jugar!"))

def menu_principal() -> str:
    """
    Esta función se encarga de dibujar tu menú principal
    y devolver el siguiente estado:
      - STATE_PLAY para empezar a jugar
      - STATE_EXIT para salir de la app
    """
    clear_screen()
    print(set_title("SNAKE") , end="\n")
    print(center_output(("[S] Iniciar juego")) , end="\n")
    print(center_output(("[Q] Salir")) , end="\n")

    while True:
        if msvcrt.kbhit():
            key = msvcrt.getch().lower()
            winsound.PlaySound(AUDIO["Blip_Select"], winsound.SND_FILENAME | winsound.SND_ASYNC)
            if key == b's':
                return STATE_PLAY
            elif key == b'q':
                return STATE_EXIT
        time.sleep(0.05)

def menu_game_over() -> str:
    """
    Animación o texto de Game Over + opciones:
      - Volver a jugar (STATE_PLAY)
      - Volver al menú principal (STATE_MENU)
      - Salir (STATE_EXIT)
    """
    winsound.PlaySound(AUDIO["Explosion"],winsound.SND_FILENAME | winsound.SND_ASYNC)

    clear_screen()
    print(set_title("GAME OVER") , end="\n")
    print(center_output(("[R] Reintentar")) , end="\n")
    print(center_output(("[M] Menú principal")) , end="\n")
    print(center_output(("[Q] Salir")) , end="\n")

    while True:
        if msvcrt.kbhit():
            key = msvcrt.getch().lower()
            winsound.PlaySound(AUDIO["Blip_Select"], winsound.SND_FILENAME | winsound.SND_ASYNC)
            if key == b'r':
                return STATE_PLAY
            elif key == b'm':
                return STATE_MENU
            elif key == b'q' or key == b'\x1b':
                return STATE_EXIT
        time.sleep(0.05)

def play_loop():
    board = Board(16, 8)
    snake = Snake([8, 4], board)
    fruit = Fruit(board, snake)

    direction = (1, 0)
    tick_rate = 0.25
    last_time = time.time()


    while True:
        now = time.time()
        delta = now - last_time

        if delta >= tick_rate:
            last_time = now

            # Dibujar
            clear_screen()
            board.clear()
            snake.handle_movement(board, fruit, direction)
            fruit.update_pos(board)
            print(center_output(f"Score: { snake.score }"), end="\n")
            print(center_output(str(board)), end="\n")
            if fruit.just_eated:
                print(center_output(f"+ {fruit.points}"), end="\n")
                fruit.just_eated = False

            if snake.is_dead():
                return STATE_GAME_OVER

        if msvcrt.kbhit():
            key = msvcrt.getch().lower()
            if key in DIRECTIONS:
                direction = DIRECTIONS[key]
            elif key == b'\x1b':  # ESC 
                return STATE_EXIT

        tick_rate = 0.15 if (direction == (-1, 0)) or (direction == (1, 0)) else 0.25
        time.sleep(0.01)
    

if __name__ == "__main__":
    main()