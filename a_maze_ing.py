import sys
import os
import time
import random
from config import load_config, ConfigError
from mazegen import MazeGenerator
from mazegen.show_path import Solver
from renderer import render_ascii, PALETTES


def clear_screen() -> None:
    os.system("clear")


def generate_and_render(config, pal_idx):
    seed_to_use = (config.seed if config.seed is not None
                   else random.randint(0, 999999))
    generator = MazeGenerator(
        width=config.width,
        height=config.height,
        entry=config.entry,
        exit=config.exit,
        seed=config.seed if config.seed else random.randint(0, 999999),
    )
    pal = PALETTES[pal_idx]
    theme = {"walls": pal["walls"], "inner": pal["inner"],
             "pattern": pal["pattern"]}

    for grid, current_cell in generator.generate_animated(
        perfect=config.perfect
    ):
        clear_screen()
        render_ascii(
            grid,
            config.entry,
            config.exit,
            theme,
            show_42=True,
            current_cell=current_cell
        )
        time.sleep(0.03)

    grid = generator.get_cells()
    return generator, grid


def save_maze_to_file_hex(grid, config):
    """Save maze to file using hex digits, then entry, exit, shortest path."""
    lines = []

    # 1️⃣ Maze cells, row by row
    for row in grid:
        line = "".join(f"{cell:X}" for cell in row)  # hex, no spaces
        lines.append(line)

    # 2️⃣ Empty line
    lines.append("")

    # 3️⃣ Entry coordinates
    lines.append(f"{config.entry[0]} {config.entry[1]}")

    # 4️⃣ Exit coordinates
    lines.append(f"{config.exit[0]} {config.exit[1]}")

    # 5️⃣ Shortest path (convert integers to letters)
    path_dirs = Solver.solve_bfs(
        grid=grid,
        entry=config.entry,
        exit_=config.exit
    )
    dir_map = {N: "N", E: "E", S: "S", W: "W"}
    path_str = "".join(dir_map[d] for d in path_dirs)
    lines.append(path_str)

    # 6️⃣ Write to file
    with open(config.output_file, "w") as f:
        f.write("\n".join(lines) + "\n")  # ensure final newline

    print(f"\033[32mMaze saved to {config.output_file} in subject format\033[0m")


BLUE = "\033[34m"
RED = "\033[31m"
GREEN = "\033[32m"
RESET = "\033[0m"
YELLOW = "\033[33m"


def main() -> None:
    if len(sys.argv) != 2:
        print("Usage: python3 a_maze_ing.py config.txt")
        sys.exit(1)
    try:
        from animations import show_intro
        from mazegen.playmode import PlayMode
        config = load_config(sys.argv[1])
        pal_idx = 0
        # Show intro animation first
        show_intro()
        generator, grid = generate_and_render(config, pal_idx)
        save_maze_to_file_hex(grid, config)

        path_cells = None
        pal = PALETTES[pal_idx]
        theme = {
            "walls": pal["walls"],
            "inner": pal["inner"],
            "pattern": pal["pattern"],
        }
        while True:
            print(f"\n\n\n\n {GREEN}Theme: {PALETTES[pal_idx]['name']}")
            print(f"{BLUE} ▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄"
                  f"▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄{RESET}")
            print(f"{BLUE} ▌            ▌            ▌           ▌          "
                  f"  ▌           ▌{RESET}")
            print(f"{BLUE} ▌{RESET} [R]{RED} Regen{RESET}  {BLUE}▌{RESET} [S]"
                  f"{RED} Solve{RESET}  {BLUE}▌{RESET} [P]{RED} Play{RESET}  "
                  f"{BLUE}▌{RESET} [C]{RED} Theme{RESET}  {BLUE}▌{RESET} [Q]"
                  f"{RED} Quit{RESET}  {BLUE}▌{RESET} [M]{RED} Stop music{RESET} ")
            print(f"{BLUE} ▌            ▌            ▌           ▌          "
                  f"  ▌           ▌{RESET}")
            print(f"{BLUE} ▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀"
                  f"▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀{RESET}")
            choice = input("> ").strip().lower()   # ← wait Enter
            if choice == "q":
                break
            elif choice == "r":
                # regenerate maze
                generator, grid = generate_and_render(config, pal_idx)
                path_cells = None
            elif choice == "s":
                # 🔹 If path already visible → hide it
                if path_cells:
                    path_cells = None
                    clear_screen()
                    render_ascii(grid, config.entry, config.exit, theme,
                                 show_42=True)
                    continue
                # 🔹 Compute path
                path_dirs = Solver.solve_bfs(
                    grid=grid,
                    entry=config.entry,
                    exit_=config.exit
                )
                cells = Solver.path_to_cells(config.entry, path_dirs)
                visible = set()
                # 🔹 Animate one point after another
                for c in cells[1:-1]:
                    visible.add(c)
                    clear_screen()
                    render_ascii(
                        grid,
                        config.entry,
                        config.exit,
                        theme,
                        show_42=True,
                        path_cells=visible
                    )
                    time.sleep(0.05)
                # 🔹 Remember path so next S hides it
                path_cells = set(cells)
            elif choice == "p":
                PlayMode.play(
                    maze=generator,  # pass your MazeGenerator object
                    entry=config.entry,
                    exit_=config.exit,
                    theme=theme
                )
            elif choice == "c":
                pal_idx = (pal_idx + 1) % len(PALETTES)
                clear_screen()
                pal = PALETTES[pal_idx]
                theme = {
                    "walls": pal["walls"],
                    "inner": pal["inner"],
                    "pattern": pal["pattern"],
                }
                render_ascii(grid, config.entry, config.exit, theme,
                             show_42=True)
            # elif choice == "m":
            #     pygame.mixer.music.stop()
            else:
                continue
    except ConfigError as error:
        print(f"Configuration error: {error}")
        sys.exit(1)



if __name__ == "__main__":
    main()

