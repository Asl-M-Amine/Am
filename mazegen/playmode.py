import os
import time
from typing import TYPE_CHECKING, Tuple, Dict

from mazegen.generator import E, N, S, W
from renderer import render_ascii

if TYPE_CHECKING:
    from mazegen.generator import MazeGenerator


class PlayMode:
    """
    Interactive maze play mode WITHOUT bonuses.
    Player has 3 hearts; wrong moves remove a heart.
    Theme colors are passed dynamically.
    """

    @staticmethod
    def play(
        maze: "MazeGenerator",
        entry: Tuple[int, int],
        exit_: Tuple[int, int],
        theme: Dict[str, str],   # <-- pass current theme
    ) -> None:
        """
        Start interactive play mode.
        Move with WASD, lose hearts on invalid moves.
        """
        os.system("cls" if os.name == "nt" else "clear")
        intro_text = "\033[1;31mHurry Up! Find the Exit!\033[0m"
        for c in intro_text:
            print(c, end="", flush=True)
            time.sleep(0.05)
        print()
        time.sleep(1)

        px, py = entry
        goal_x, goal_y = exit_
        steps = 0
        hearts = ["\033[1;31m\u2665\033[0m"] * 3  # fixed 3 hearts

        while True:
            # Clear screen first
            os.system("cls" if os.name == "nt" else "clear")

            # Status bar with hearts, steps, exit
            hearts_display = "".join(["\033[1;31m\u2665\033[0m " for _ in hearts])
            status_bar = f"[ {hearts_display}]  Steps: {steps}  Exit: ({goal_x},{goal_y})"
            border = "═" * len(status_bar)

            print(f"╔{border}╗")
            print(f"║{status_bar}║")
            print(f"╚{border}╝")

            # Fun instruction line (Pac-Man style)
            print("Guide the mouse 🐁 with W/A/S/D. Can you escape to the cheese 🧀?\n")
            render_ascii(
                maze.get_cells(),
                entry=(px, py),
                exit_=exit_,
                origin_theme=theme,   # <-- use dynamic theme
                show_42=True,
            )

            if (px, py) == (goal_x, goal_y):
                print("\033[92mCongrats! You reached the exit!\033[0m")
                time.sleep(1.5)
                break

            move = input("Move: ").lower()
            current_cell = maze.get_cells()[py][px]
            moved = False

            if move == "w" and not (current_cell & N):
                py -= 1
                moved = True
            elif move == "s" and not (current_cell & S):
                py += 1
                moved = True
            elif move == "a" and not (current_cell & W):
                px -= 1
                moved = True
            elif move == "d" and not (current_cell & E):
                px += 1
                moved = True
            elif move == "exit":
                print("Exiting play mode.")
                break
            else:
                # Invalid move → lose one heart
                print("\033[91mInvalid move! You lose a heart.\033[0m")
                if hearts:
                    hearts.pop()
                    time.sleep(0.5)
                if not hearts:
                    print("\033[91mGame Over! You ran out of hearts.\033[0m")
                    break

            if moved:
                steps += 1
