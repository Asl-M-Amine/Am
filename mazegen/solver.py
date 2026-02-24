from renderer import PALETTES, get_42_pattern_coords, render_ascii
import os
import time
from typing import Dict, List, Tuple


# Directions for your maze
N, E, S, W = 1, 2, 4, 8
DIRECTIONS = {N: (0, -1), E: (1, 0), S: (0, 1), W: (-1, 0)}
OPPOSITE = {N: S, S: N, E: W, W: E}


class Solver:
    @staticmethod
    def solve_bfs(
        grid: List[List[int]],
        entry: Tuple[int, int],
        exit_: Tuple[int, int],
    ) -> List[int]:
        """BFS to get directions list (N,E,S,W)"""
        from collections import deque

        queue = deque([entry])
        visited = {entry}
        parent: Dict[Tuple[int, int], Tuple[int, int, int]] = {}

        while queue:
            x, y = queue.popleft()
            if (x, y) == exit_:
                break
            cell = grid[y][x]
            for direction, (dx, dy) in DIRECTIONS.items():
                if cell & direction:  # wall exists
                    continue
                nx, ny = x + dx, y + dy
                if 0 <= nx < len(grid[0]) and 0 <= ny < len(grid):
                    if (nx, ny) not in visited:
                        visited.add((nx, ny))
                        parent[(nx, ny)] = (x, y, direction)
                        queue.append((nx, ny))
        return Solver.generate_path(parent, entry, exit_)

    @staticmethod
    def generate_path(
        parent: Dict,
        entry: Tuple[int, int],
        exit_: Tuple[int, int],
    ) -> List[int]:
        """Convert BFS parent dict to direction path"""
        path = []
        current = exit_
        while current != entry:
            x, y, direction = parent[current]
            path.append(direction)
            current = (x, y)
        path.reverse()
        return path

    @staticmethod
    def path_to_cells(
        entry: Tuple[int, int],
        path: List[int],
    ) -> List[Tuple[int, int]]:
        x, y = entry
        cells = [(x, y)]
        for d in path:
            dx, dy = DIRECTIONS[d]
            x += dx
            y += dy
            cells.append((x, y))
        return cells

    @staticmethod
    def show_path(
        grid: List[List[int]],
        entry: Tuple[int, int],
        exit_: Tuple[int, int],
        path: List[int],
        origin_theme: Dict[str, str],
        animate: bool = True,
    ) -> None:
        """Show the solution path on your real maze with mouse animation"""
        cells = Solver.path_to_cells(entry, path)
        height = len(grid)
        width = len(grid[0])
        p42 = get_42_pattern_coords(width, height)
        visited = set()

        for px, py in cells:
            visited.add((px, py))
            os.system("cls" if os.name == "nt" else "clear")

            # Create a temporary "grid" with dots for visited
            temp_grid = []
            for y in range(height):
                row = []
                for x in range(width):
                    if (x, y) in visited and (x, y) not in p42:
                        row.append("•")  # dot for visited
                    else:
                        row.append(None)  # leave as maze
                temp_grid.append(row)

            render_ascii(
                grid,
                entry=(px, py),  # current mouse pos
                exit_=exit_,
                origin_theme=origin_theme,
                show_42=True,
                visited=temp_grid,  # pass visited dots
            )
            if animate:
                time.sleep(0.05)
