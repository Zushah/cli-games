import os
import time
import random

try:
    import msvcrt
    def get_key():
        if msvcrt.kbhit():
            key = msvcrt.getch()
            return key
        return None
except ImportError:
    try:
        import termios
        import sys, tty, select
        def get_key():
            if sys.stdin.isatty():
                fd = sys.stdin.fileno()
                old_settings = termios.tcgetattr(fd)
                try:
                    tty.setcbreak(fd)
                    if sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
                        return sys.stdin.read(1)
                finally:
                    termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
            return None
    except ImportError:
        def get_key():
            return None

WIDTH = 40
HEIGHT = 20
SNAKE_VER_CHAR = "█"
SNAKE_HOR_CHAR = "■"
HEAD_CHAR = "■"
FOOD_CHAR = "●"
BORDER_CHAR = "▓"
EMPTY_CHAR = " "
FPS = 10

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def title():
    clear()
    title = [
        " ███████╗███╗   ██╗ █████╗ ██╗  ██╗███████╗",
        " ██╔════╝████╗  ██║██╔══██╗██║ ██╔╝██╔════╝",
        " ███████╗██╔██╗ ██║███████║█████╔╝ █████╗  ",
        " ╚════██║██║╚██╗██║██╔══██║██╔═██╗ ██╔══╝  ",
        " ███████║██║ ╚████║██║  ██║██║  ██╗███████╗",
        " ╚══════╝╚═╝  ╚═══╝╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝"
    ]
    title_width = len(title[0])
    horizontal_padding = (WIDTH - title_width) // 2
    vertical_padding = (HEIGHT - len(title) - 6) // 2
    for _ in range(vertical_padding):
        print()
    for line in title:
        print(" " * horizontal_padding + line)
    src = "https://www.github.com/Zushah/cli-games"
    prompt = "Press ENTER to play"
    print("\n" + " " * ((WIDTH - len(src)) // 2) + src)
    print("\n" + " " * ((WIDTH - len(prompt)) // 2) + prompt)
    while True:
        key = get_key()
        if key in [b'\r', b'\n', 13, b'\r\n']:
            break
        time.sleep(0.1)

def spawn_food(snake):
    while True:
        x = random.randint(1, WIDTH - 2)
        y = random.randint(1, HEIGHT - 2)
        if (x, y) not in snake:
            return (x, y)

def draw_board(snake, food, score):
    board = [[EMPTY_CHAR for _ in range(WIDTH)] for _ in range(HEIGHT)]
    for i in range(WIDTH):
        board[0][i] = BORDER_CHAR
        board[HEIGHT - 1][i] = BORDER_CHAR
    for i in range(HEIGHT):
        board[i][0] = BORDER_CHAR
        board[i][WIDTH - 1] = BORDER_CHAR
    for i, (x, y) in enumerate(snake):
        if 0 < x < WIDTH - 1 and 0 < y < HEIGHT - 1:
            if i == 0:
                board[y][x] = HEAD_CHAR
            else:
                prev_x, prev_y = snake[i - 1]
                if prev_x == x:
                    board[y][x] = SNAKE_VER_CHAR
                elif prev_y == y:
                    board[y][x] = SNAKE_HOR_CHAR
    if food and 0 < food[0] < WIDTH - 1 and 0 < food[1] < HEIGHT - 1:
        board[food[1]][food[0]] = FOOD_CHAR
    clear()
    print(f"Score: {score}")
    for row in board:
        print("".join(row))
    print("Controls: WASD or arrow keys to move, spacebar to quit")

def check_input(direction):
    key = get_key()
    if not key:
        return True, direction
    if key == b" ":
        return False, direction
    if key == b"w" and direction != (0, 1):
        return True, (0, -1)
    elif key == b"a" and direction != (1, 0):
        return True, (-1, 0)
    elif key == b"s" and direction != (0, -1):
        return True, (0, 1)
    elif key == b"d" and direction != (-1, 0):
        return True, (1, 0)
    elif key == b"\xe0":
        key = get_key()
        if key == b"H" and direction != (0, 1):
            return True, (0, -1)
        elif key == b"K" and direction != (1, 0):
            return True, (-1, 0)
        elif key == b"P" and direction != (0, -1):
            return True, (0, 1)
        elif key == b"M" and direction != (-1, 0):
            return True, (1, 0)
    return True, direction

def update_game(snake, direction, food):
    head_x, head_y = snake[0]
    dir_x, dir_y = direction
    new_head = (head_x + dir_x, head_y + dir_y)
    new_x, new_y = new_head
    if new_x <= 0 or new_x >= WIDTH - 1 or new_y <= 0 or new_y >= HEIGHT - 1:
        return False, snake, food, 0
    if new_head in snake[:-1]:
        return False, snake, food, 0
    snake.insert(0, new_head)
    ate_food = False
    if new_head == food:
        ate_food = True
        food = spawn_food(snake)
    else:
        snake.pop()
    return True, snake, food, 1 if ate_food else 0

def main():
    title()
    snake = [(WIDTH // 4, HEIGHT // 2)]
    direction = (1, 0)
    food = spawn_food(snake)
    score = 0
    running = True
    draw_board(snake, food, score)
    time.sleep(1)
    while running:
        running, direction = check_input(direction)
        if not running:
            break
        running, snake, food, points = update_game(snake, direction, food)
        score += points
        draw_board(snake, food, score)
        time.sleep(1 / FPS)
    clear()
    print(f"\n\n{'=' * 20}\n  GAME OVER\n  Final Score: {score}\n{'=' * 20}")
    time.sleep(2)

if __name__ == "__main__":
    main()
