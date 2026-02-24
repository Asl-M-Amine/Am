import os
import time
import sys

# ANSI color codes
BLUE = "\033[34m"
CYAN = "\033[36m"
RESET = "\033[0m"
CLEAR = "\033[2J\033[H"

BIG_TEXT = [
    ("   ______           __       __   ______   ________  ________     ______"
     "  __    __   ______ "),
    (" /      \\         /  \\     /  | /      \\ /        |/        |   /    "
     "  |/  \\  /  | /      \\ "),
    ("/$$$$$$  |        $$  \\   /$$ |/$$$$$$  |$$$$$$$$/ $$$$$$$$/    $$$$$$/"
     " $$  \\ $$ |/$$$$$$  |"),
    ("$$ |__$$ | ______ $$$  \\ /$$$ |$$ |__$$ |    /$$/  $$ |__  ______ $$ | "
     " $$$  \\$$ |$$ | _$$/ "),
    ("$$    $$ |/      |$$$$  /$$$$ |$$    $$ |   /$$/   $$    |/      |$$ |  "
     "$$$$  $$ |$$ |/    |"),
    ("$$$$$$$$ |$$$$$$/ $$ $$ $$/$$ |$$$$$$$$ |  /$$/    $$$$$/ $$$$$$/ $$ |  "
     "$$ $$ $$ |$$ |$$$$ |"),
    ("$$ |  $$ |        $$ |$$$/ $$ |$$ |  $$ | /$$/____ $$ |_____     _$$ |_ "
     "$$ |$$$$ |$$ \\__$$ |"),
    ("$$ |  $$ |        $$ | $/  $$ |$$ |  $$ |/$$      |$$       |   / $$   |"
     "$$ | $$$ |$$    $$/ "),
    ("$$/   $$/         $$/      $$/ $$/   $$/ $$$$$$$$/ $$$$$$$$/    $$$$$$/ "
     "$$/   $$/  $$$$$$/  ")
]


def animate_big_text(text_lines: list, delay: float = 0.1):
    rows, columns = os.get_terminal_size()
    start_row = (rows - len(text_lines)) // 2
    for i, line in enumerate(text_lines):
        print(f"\033[{start_row + i};1H{BLUE}{line}{RESET}")
        time.sleep(delay)
    for i in range(12):
        print("\n")
        time.sleep(delay)
    time.sleep(0.5)


def animate_loading_bar(width=75, delay=0.02):
    print("\n")
    for i in range(width + 1):
        bar = f"[{'#' * i}{' ' * (width - i)}]"
        print(f"\r{CYAN}Loading Maze {bar}{RESET}", end="")
        sys.stdout.flush()
        time.sleep(delay)
    print("\n")


def show_intro():
    print(CLEAR)
    animate_big_text(BIG_TEXT)
    animate_loading_bar()
