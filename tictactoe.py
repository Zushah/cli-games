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
EMPTY = " "
PLAYER = "X"
COMPUTER = "O"
GRID_CHAR = "│"
HORIZ_CHAR = "─"
CROSS_CHAR = "┼"
FPS = 10

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def title():
    clear()
    title = [
        "████████╗██╗ ██████╗████████╗ █████╗  ██████╗████████╗ ██████╗ ███████╗",
        "╚══██╔══╝██║██╔════╝╚══██╔══╝██╔══██╗██╔════╝╚══██╔══╝██╔═══██╗██╔════╝",
        "   ██║   ██║██║        ██║   ███████║██║        ██║   ██║   ██║█████╗  ",
        "   ██║   ██║██║        ██║   ██╔══██║██║        ██║   ██║   ██║██╔══╝  ",
        "   ██║   ██║╚██████╗   ██║   ██║  ██║╚██████╗   ██║   ╚██████╔╝███████╗",
        "   ╚═╝   ╚═╝ ╚═════╝   ╚═╝   ╚═╝  ╚═╝ ╚═════╝   ╚═╝    ╚═════╝ ╚══════╝"
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
    print("\n" + " " * ((title_width - len(src)) // 2) + src)
    print("\n" + " " * ((title_width - len(prompt)) // 2) + prompt)
    while True:
        key = get_key()
        if key in [b'\r', b'\n', 13, b'\r\n']:
            break
        time.sleep(0.1)

def initialize_board():
    return [EMPTY] * 9

def draw_board(board, cursor_pos, player_turn, message=""):
    clear()
    print("\n" + " " * ((WIDTH - 11) // 2) + "TIC-TAC-TOE\n")
    horizontal_line = " " * ((WIDTH - 11) // 2) + HORIZ_CHAR * 3 + CROSS_CHAR + HORIZ_CHAR * 3 + CROSS_CHAR + HORIZ_CHAR * 3
    for row in range(3):
        line = " " * ((WIDTH - 11) // 2)
        for col in range(3):
            index = row * 3 + col
            cell = board[index]
            if cell == EMPTY and index == cursor_pos and player_turn:
                cell = "•"
            line += f" {cell} "
            if col < 2:
                line += GRID_CHAR
        print(line)
        if row < 2:
            print(horizontal_line)
    print("\n" + " " * ((WIDTH - len(message)) // 2) + message)
    print("\nControls: WASD or arrow keys to select, enter to place, spacebar to quit")
    if player_turn:
        print("\nYour turn (X)")
    else:
        print("\nComputer's turn (O)")

def check_winner(board):
    win_conditions = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],
        [0, 3, 6], [1, 4, 7], [2, 5, 8],
        [0, 4, 8], [2, 4, 6]
    ]
    for condition in win_conditions:
        if board[condition[0]] != EMPTY and board[condition[0]] == board[condition[1]] == board[condition[2]]:
            return board[condition[0]]
    if EMPTY not in board:
        return "TIE"
    return None

def computer_move(board):
    empty_cells = [i for i, cell in enumerate(board) if cell == EMPTY]
    for cell in empty_cells:
        board_copy = board.copy()
        board_copy[cell] = COMPUTER
        if check_winner(board_copy) == COMPUTER:
            return cell
    for cell in empty_cells:
        board_copy = board.copy()
        board_copy[cell] = PLAYER
        if check_winner(board_copy) == PLAYER:
            return cell
    if board[4] == EMPTY:
        return 4
    corners = [0, 2, 6, 8]
    available_corners = [corner for corner in corners if board[corner] == EMPTY]
    if available_corners:
        return random.choice(available_corners)
    return random.choice(empty_cells)

def check_input(cursor_pos, board):
    key = get_key()
    if not key:
        return cursor_pos, False, True
    if key == b" ":
        return cursor_pos, False, False
    if key in [b'\r', b'\n', 13, b'\r\n']:
        if board[cursor_pos] == EMPTY:
            return cursor_pos, True, True
    if key == b"\xe0":
        key = get_key()
        if key == b"H" and cursor_pos >= 3:
            return cursor_pos - 3, False, True
        elif key == b"P" and cursor_pos < 6:
            return cursor_pos + 3, False, True
        elif key == b"K" and cursor_pos % 3 > 0:
            return cursor_pos - 1, False, True
        elif key == b"M" and cursor_pos % 3 < 2:
            return cursor_pos + 1, False, True
    if key == b"w" and cursor_pos >= 3:
        return cursor_pos - 3, False, True
    elif key == b"s" and cursor_pos < 6:
        return cursor_pos + 3, False, True
    elif key == b"a" and cursor_pos % 3 > 0:
        return cursor_pos - 1, False, True
    elif key == b"d" and cursor_pos % 3 < 2:
        return cursor_pos + 1, False, True
    return cursor_pos, False, True

def main():
    title()
    player_wins = 0
    computer_wins = 0
    ties = 0
    play_again = True
    while play_again:
        board = initialize_board()
        cursor_pos = 4
        player_turn = True
        message = ""
        game_over = False
        while not game_over:
            draw_board(board, cursor_pos, player_turn, message)
            if player_turn:
                cursor_pos, make_move, running = check_input(cursor_pos, board)
                if not running:
                    return
                if make_move:
                    board[cursor_pos] = PLAYER
                    player_turn = False
            else:
                time.sleep(0.5)
                computer_cell = computer_move(board)
                board[computer_cell] = COMPUTER
                player_turn = True
            result = check_winner(board)
            if result:
                draw_board(board, cursor_pos, False, "")
                if result == PLAYER:
                    message = "You win!"
                    player_wins += 1
                elif result == COMPUTER:
                    message = "Computer wins!"
                    computer_wins += 1
                else:
                    message = "It's a tie!"
                    ties += 1
                game_over = True
                draw_board(board, cursor_pos, False, message)
                time.sleep(1)
                print(f"\nScore - Player: {player_wins}  Computer: {computer_wins}  Ties: {ties}")
                print("\nPress Enter to play again, Space to quit")
                waiting_for_key = True
                while waiting_for_key:
                    key = get_key()
                    if key in [b'\r', b'\n', 13, b'\r\n']:
                        waiting_for_key = False
                    elif key == b" ":
                        play_again = False
                        waiting_for_key = False
                    time.sleep(0.1)
            time.sleep(1 / FPS)

if __name__ == "__main__":
    main()
