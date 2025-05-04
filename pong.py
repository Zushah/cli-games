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

WIDTH = 60
HEIGHT = 20
PADDLE_HEIGHT = 4
BALL_CHAR = "O"
PADDLE_CHAR = "█"
BORDER_CHAR = "■"
EMPTY_CHAR = " "
FPS = 30

computer_paddle_pos = HEIGHT // 2 - PADDLE_HEIGHT // 2
player_paddle_pos = HEIGHT // 2 - PADDLE_HEIGHT // 2
ball_x = WIDTH // 2
ball_y = HEIGHT // 2
ball_dx = random.choice([-1, 1])
ball_dy = 0
computer_score = 0
player_score = 0

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def title():
    clear()
    title = [
        " ██████╗  ██████╗ ███╗   ██╗ ██████╗ ",
        " ██╔══██╗██╔═══██╗████╗  ██║██╔════╝ ",
        " ██████╔╝██║   ██║██╔██╗ ██║██║  ███╗",
        " ██╔═══╝ ██║   ██║██║╚██╗██║██║   ██║",
        " ██║     ╚██████╔╝██║ ╚████║╚██████╔╝",
        " ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝ "
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

def draw_board():
    board = [[EMPTY_CHAR for _ in range(WIDTH)] for _ in range(HEIGHT)]
    for i in range(WIDTH):
        board[0][i] = BORDER_CHAR
        board[HEIGHT - 1][i] = BORDER_CHAR
    for i in range(PADDLE_HEIGHT):
        if 0 < computer_paddle_pos + i < HEIGHT - 1:
            board[computer_paddle_pos + i][1] = PADDLE_CHAR
        if 0 < player_paddle_pos + i < HEIGHT - 1:
            board[player_paddle_pos + i][WIDTH - 2] = PADDLE_CHAR
    ball_y_int = int(ball_y)
    ball_x_int = int(ball_x)
    if 0 < ball_y_int < HEIGHT - 1 and 0 < ball_x_int < WIDTH - 1:
        board[ball_y_int][ball_x_int] = BALL_CHAR
    clear()
    print(f"Computer: {computer_score} | Player: {player_score}")
    for row in board:
        print("".join(row))
    print("Controls: W/S/up/down keys to move paddle, spacebar to quit")

def check_input():
    global player_paddle_pos
    key = get_key()
    if key:
        if key == b"w" and player_paddle_pos > 1:
            player_paddle_pos -= 1
        elif key == b"s" and player_paddle_pos < HEIGHT - PADDLE_HEIGHT - 1:
            player_paddle_pos += 1
        elif key == b" ":
            return False
        if key == b"\xe0":
            key = get_key()
            if key == b"H" and player_paddle_pos > 1:
                player_paddle_pos -= 1
            elif key == b"P" and player_paddle_pos < HEIGHT - PADDLE_HEIGHT - 1:
                player_paddle_pos += 1
    return True

def update_computer_paddle():
    global computer_paddle_pos
    if 1 < ball_y < HEIGHT - 2:
        target_y = ball_y - PADDLE_HEIGHT // 2
        if target_y < computer_paddle_pos - 1:
            computer_paddle_pos = max(1, computer_paddle_pos - 1)
        elif target_y > computer_paddle_pos + 1:
            computer_paddle_pos = min(HEIGHT - PADDLE_HEIGHT - 1, computer_paddle_pos + 1)

def update_ball():
    global ball_x, ball_y, ball_dx, ball_dy, computer_score, player_score
    ball_x += ball_dx
    ball_y += ball_dy
    if ball_y <= 1 or ball_y >= HEIGHT - 2:
        ball_dy *= -1
    if ball_x <= 2 and computer_paddle_pos <= ball_y < computer_paddle_pos + PADDLE_HEIGHT:
        ball_dx = abs(ball_dx)
        relative_position = (ball_y - computer_paddle_pos) / PADDLE_HEIGHT
        old_dy = ball_dy * 0.5 
        new_dy = (relative_position - 0.5) * 2
        ball_dy = new_dy + old_dy
        ball_x = 3
    if ball_x >= WIDTH - 3 and player_paddle_pos <= ball_y < player_paddle_pos + PADDLE_HEIGHT:
        ball_dx = -abs(ball_dx)
        relative_position = (ball_y - player_paddle_pos) / PADDLE_HEIGHT
        old_dy = ball_dy * 0.5
        new_dy = (relative_position - 0.5) * 2
        ball_dy = new_dy + old_dy
        ball_x = WIDTH - 4
    if ball_x <= 0:
        player_score += 1
        reset_ball()
    elif ball_x >= WIDTH - 1:
        computer_score += 1
        reset_ball()

def reset_ball():
    global ball_x, ball_y, ball_dx, ball_dy
    ball_x = WIDTH // 2
    ball_y = HEIGHT // 2
    ball_dx = random.choice([-1, 1])
    ball_dy = 0

def main():
    title()
    running = True
    draw_board()
    time.sleep(1)
    while running:
        for _ in range(60):
            if not running:
                break
            running = check_input()
        update_computer_paddle()
        update_ball()
        draw_board()
        time.sleep(1 / FPS)

if __name__ == "__main__":
    main()
