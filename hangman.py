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
WORD_LIST = [
    "algorithm", "binary", "browser", "compiler", "computer",
    "database", "debugging", "developer", "framework", "function",
    "hangman", "hardware", "interface", "keyboard", "language",
    "memory", "network", "programming", "project", "python",
    "software", "syntax", "terminal", "variable", "workflow"
]
MAX_ATTEMPTS = 6
FPS = 30

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def title():
    clear()
    title = [
        " ██╗  ██╗ █████╗ ███╗   ██╗ ██████╗ ███╗   ███╗ █████╗ ███╗   ██╗",
        " ██║  ██║██╔══██╗████╗  ██║██╔════╝ ████╗ ████║██╔══██╗████╗  ██║",
        " ███████║███████║██╔██╗ ██║██║  ███╗██╔████╔██║███████║██╔██╗ ██║",
        " ██╔══██║██╔══██║██║╚██╗██║██║   ██║██║╚██╔╝██║██╔══██║██║╚██╗██║",
        " ██║  ██║██║  ██║██║ ╚████║╚██████╔╝██║ ╚═╝ ██║██║  ██║██║ ╚████║",
        " ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝ ╚═════╝ ╚═╝     ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝"
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

def get_hangman_art(attempts):
    stages = [
        """
          +---+
          |   |
          O   |
         /|\\  |
         / \\  |
              |
        =========
        """,
        """
          +---+
          |   |
          O   |
         /|\\  |
         /    |
              |
        =========
        """,
        """
          +---+
          |   |
          O   |
         /|\\  |
              |
              |
        =========
        """,
        """
          +---+
          |   |
          O   |
         /|   |
              |
              |
        =========
        """,
        """
          +---+
          |   |
          O   |
          |   |
              |
              |
        =========
        """,
        """
          +---+
          |   |
          O   |
              |
              |
              |
        =========
        """,
        """
          +---+
          |   |
              |
              |
              |
              |
        =========
        """
    ]
    return stages[attempts]

def draw_board(word, guessed_letters, attempts):
    clear()
    print(get_hangman_art(attempts))
    display_word = []
    for letter in word:
        if letter in guessed_letters:
            display_word.append(letter)
        else:
            display_word.append("_")
    word_display = " ".join(display_word)
    print("\nWord: " + word_display)
    if guessed_letters:
        print("\nGuessed letters: " + ", ".join(sorted(guessed_letters)))
    else:
        print("\nGuessed letters: None")
    print(f"\nAttempts remaining: {attempts}")
    print("\nType a letter to guess or press spacebar to quit")

def check_input(guessed_letters):
    key = get_key()
    if not key:
        return None, True
    if key == b" ":
        return None, False
    try:
        if isinstance(key, bytes):
            key = key.decode("utf-8").lower()
        if key.isalpha() and len(key) == 1:
            return key, True
    except:
        pass
    return None, True

def main():
    title()
    word = random.choice(WORD_LIST).lower()
    guessed_letters = set()
    attempts = MAX_ATTEMPTS
    running = True
    draw_board(word, guessed_letters, attempts)
    time.sleep(1)
    while running:
        guess, running = check_input(guessed_letters)
        if not running:
            break
        if guess and guess not in guessed_letters:
            guessed_letters.add(guess)
            if guess not in word:
                attempts -= 1
        draw_board(word, guessed_letters, attempts)
        if attempts == 0:
            print(f"\nGame Over! The word was: {word}")
            time.sleep(2)
            break
        if all(letter in guessed_letters for letter in word):
            print("\nCongratulations! You guessed the word!")
            time.sleep(2)
            break
        time.sleep(1 / FPS)
    clear()
    print(f"\n\n{'=' * 20}\n  GAME OVER\n  Word: {word}\n{'=' * 20}")
    time.sleep(2)

if __name__ == "__main__":
    main()
