import random
from typing import List, Tuple, Set, Optional

# Direction bitmasks
N, E, S, W = 1, 2, 4, 8
DX = {E: 1, W: -1, N: 0, S: 0}
DY = {E: 0, W: 0, N: -1, S: 1}
OPPOSITE = {N: S, S: N, E: W, W: E}


class MazeGenerator:
    """Generate a perfect maze using DFS with animated generation."""

    def __init__(
        self,
        width: int,
        height: int,
        entry: Tuple[int, int] = (0, 0),
        exit: Tuple[int, int] = (0, 0),
        seed: Optional[int] = None,
    ) -> None:
        self.width = width
        self.height = height
        self.entry = entry
        self.exit = exit
        self.rng = random.Random(seed)

        # Grid: each cell holds wall bitmask
        self.grid: List[List[int]] = [
            [N | E | S | W for _ in range(width)] for _ in range(height)
        ]
        self.visited: List[List[bool]] = [
            [False for _ in range(width)] for _ in range(height)
        ]

        # Blocked cells for the "42" pattern
        self.blocked = self._create_42_pattern()

    # -----------------------------

    def _create_42_pattern(self) -> Set[Tuple[int, int]]:
        """Return coordinates for 42 pattern."""
        if self.width < 7 or self.height < 5:
            return set()

        start_x = (self.width - 7) // 2
        start_y = (self.height - 5) // 2

        pattern = [
            "1000111",
            "1000001",
            "1110111",
            "0010100",
            "0010111",
        ]

        blocked: Set[Tuple[int, int]] = set()
        for dy, row in enumerate(pattern):
            for dx, char in enumerate(row):
                if char == "1":
                    blocked.add((start_x + dx, start_y + dy))
        return blocked

    # -----------------------------

    def get_unvisited_neighbors(self, x: int, y: int, visited: set) -> list:
        """Return unvisited neighbors for DFS."""
        neighbors = []
        directions = [(0, -1), (1, 0), (0, 1), (-1, 0)]  # N, E, S, W
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.width and 0 <= ny < self.height:
                if (nx, ny) not in visited:
                    neighbors.append((nx, ny))
        return neighbors

    # -----------------------------

    def remove_wall(self, a: Tuple[int, int], b: Tuple[int, int]) -> None:
        """Remove wall between two adjacent cells."""
        x1, y1 = a
        x2, y2 = b
        if x2 == x1 + 1:
            self.grid[y1][x1] &= ~E
            self.grid[y2][x2] &= ~W
        elif x2 == x1 - 1:
            self.grid[y1][x1] &= ~W
            self.grid[y2][x2] &= ~E
        elif y2 == y1 + 1:
            self.grid[y1][x1] &= ~S
            self.grid[y2][x2] &= ~N
        elif y2 == y1 - 1:
            self.grid[y1][x1] &= ~N
            self.grid[y2][x2] &= ~S

    # -----------------------------

    def generate_animated(self):
        visited = set()
        entry = self.entry
        visited.add(entry)
        stack = [entry]

        while stack:
            x, y = stack[-1]
            # ✅ Exclude blocked "42" cells
            neighbors = [
                (nx, ny)
                for nx, ny in self.get_unvisited_neighbors(x, y, visited)
                if (nx, ny) not in self.blocked
            ]
            if neighbors:
                nx, ny = self.rng.choice(neighbors)
                self.remove_wall((x, y), (nx, ny))
                visited.add((nx, ny))
                stack.append((nx, ny))
            else:
                stack.pop()
            yield [row[:] for row in self.grid], (x, y)

    # -----------------------------

    def generate(self) -> None:
        """Non-animated DFS generation for final maze."""
        for x, y in self.blocked:
            self.visited[y][x] = True
            self.grid[y][x] = N | E | S | W  # block completely

        sx, sy = self.entry
        if (sx, sy) in self.blocked:
            self.blocked.remove((sx, sy))

        self._dfs(sx, sy)

    def _dfs(self, cx: int, cy: int) -> None:
        self.visited[cy][cx] = True
        dirs = [N, E, S, W]
        self.rng.shuffle(dirs)

        for d in dirs:
            nx, ny = cx + DX[d], cy + DY[d]

            # ✅ Skip blocked "42" cells
            if (nx, ny) in self.blocked:
                continue

            if 0 <= nx < self.width and 0 <= ny < self.height:
                if not self.visited[ny][nx]:
                    self.grid[cy][cx] &= ~d
                    self.grid[ny][nx] &= ~OPPOSITE[d]
                    self._dfs(nx, ny)

    # -----------------------------

    def get_cells(self) -> List[List[int]]:
        return self.grid