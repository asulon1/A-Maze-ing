# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  __init__.py                                       :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: asulon <asulon@student.42.fr>             +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/03/22 12:22:30 by asulon          #+#    #+#               #
#  Updated: 2026/04/26 17:23:08 by asulon          ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

import random
from typing import List, Tuple, Optional


class Cell:
    """
    Represents a single cell within the maze's grid.

    Attributes:
        x: The x-coordinate of the cell.
        y: The y-coordinate of the cell.
        walls: States of walls ('N', 'E', 'S', 'W').
                                True wall exists.
        visited (bool): A flag used by generation and solving algorithms.
        pattern: 42 parterns
    """

    def __init__(self, x: int, y: int) -> None:
        self.x: int = x
        self.y: int = y
        self.walls: dict[str, bool] = {
            'N': True, 'E': True, 'S': True, 'W': True}
        self.visited: bool = False
        self.pattern: bool = False


class MazeGenerator:
    def __init__(self, width: int, height: int, seed: Optional[int] = None,
                 entry: Tuple[int, int] = (0, 0),
                 exit: Tuple[int, int] = (0, 0),
                 perfect: bool = True) -> None:
        if width <= 0 or height <= 0:
            raise ValueError("Width and height must be positive.")
        self.width: int = width
        self.height: int = height
        self.seed: Optional[int] = seed
        self.entry: Tuple[int, int] = entry
        self.exit: Tuple[int, int] = exit
        self.perfect: bool = perfect
        self.grid: List[List[Cell]] = []
        self.solution: Optional[str] = None
        """ANSI color mapping for wall, path, start, end, solution, and 42."""
        self.colors: dict[str, str] = {
            "WALL": "\033[97m██\033[0m",
            "PATH": "  ",
            "START":  "\033[35m██\033[0m",
            "END": "\033[31m██\033[0m",
            "SOL":  "\033[42m  \033[0m",
            "42": "\033[33m██\033[0m"
        }

        if self.seed is not None:
            random.seed(self.seed)

        self._initialize_grid()
        self._carve_42_pattern()

    def _initialize_grid(self) -> None:
        self.grid = [[Cell(x, y) for x in range(self.width)]
                     for y in range(self.height)]

    def _carve_42_pattern(self) -> None:
        """
        Carves the '42' pattern into the maze. cells are marked as
        'visited' to be ignored by the generation algorithm.
        """
        """Define the shapes of 4 and 2 in local coordinates."""
        pattern_4 = [
            (0, 0), (2, 0), (0, 1), (1, 1), (2, 1),
            (2, 2), (2, 3), (2, 4)
        ]
        pattern_2 = [
            (0, 0), (1, 0), (2, 0), (2, 1), (0, 2), (1, 2), (2, 2),
            (0, 3), (0, 4), (1, 4), (2, 4)
        ]

        """Skip 42 pattern when the maze is too small."""
        if self.width < 9 or self.height < 7:
            print("Warning: Maze too small to draw '42' pattern.")
            return

        """Compute top-left origin of the centered 42 pattern."""

        start_x = (self.width - 8) // 2
        start_y = (self.height - 5) // 2

        """Apply the 4 pattern by freezing selected cells."""
        for dx, dy in pattern_4:
            x, y = start_x + dx, start_y + dy
            if 0 <= x < self.width and 0 <= y < self.height:
                cell = self.grid[y][x]
                cell.visited = True
                cell.pattern = True
                for wall in cell.walls:
                    cell.walls[wall] = True

        """Apply the 2 pattern offset to the right."""
        for dx, dy in pattern_2:
            x, y = start_x + dx + 4, start_y + dy
            if 0 <= x < self.width and 0 <= y < self.height:
                cell = self.grid[y][x]
                cell.visited = True
                cell.pattern = True

                for wall in cell.walls:
                    cell.walls[wall] = True

    def _get_unvisited_neighbors(self, cell: Cell) -> List[Cell]:
        """Return unvisited cells next to given cell."""
        neighbors: List[Cell] = []
        x, y = cell.x, cell.y

        if y > 0 and not self.grid[y - 1][x].visited:
            neighbors.append(self.grid[y - 1][x])
        if y < self.height - 1 and not self.grid[y + 1][x].visited:
            neighbors.append(self.grid[y + 1][x])
        if x < self.width - 1 and not self.grid[y][x + 1].visited:
            neighbors.append(self.grid[y][x + 1])
        if x > 0 and not self.grid[y][x - 1].visited:
            neighbors.append(self.grid[y][x - 1])
        return neighbors

    def _creates_large_open_area(self, cell1: Cell, cell2: Cell) -> bool:
        """
        Heuristic check to prevent creating 3x3 open areas.

        It works by checking if removing a wall would complete a 2x2 open
        square, which is a precursor to larger open areas.
        """
        """Check vertical moves that would create a 2x2 opening."""
        if cell1.x == cell2.x:
            x = cell1.x
            y = min(cell1.y, cell2.y)
            """Check potential opening on the left side."""
            if (x > 0 and not self.grid[y][x].walls['W'] and
                    not self.grid[y+1][x].walls['W']):
                if (not self.grid[y][x-1].walls['S'] and
                        not self.grid[y+1][x-1].walls['N']):
                    return True
            """Check potential opening on the right side."""
            if (x < self.width - 1 and not self.grid[y][x].walls['E'] and
                    not self.grid[y+1][x].walls['E']):
                if (not self.grid[y][x+1].walls['S'] and
                        not self.grid[y+1][x+1].walls['N']):
                    return True

        else:
            """Check horizontal moves that would create a 2x2 opening."""
            y = cell1.y
            x = min(cell1.x, cell2.x)
            """Check potential opening above."""
            if (y > 0 and not self.grid[y][x].walls['N'] and
                    not self.grid[y][x+1].walls['N']):
                if (not self.grid[y-1][x].walls['E'] and
                        not self.grid[y-1][x+1].walls['W']):
                    return True
            """Check potential opening below."""
            if (y < self.height - 1 and not self.grid[y][x].walls['S'] and
                    not self.grid[y][x+1].walls['S']):
                if (not self.grid[y+1][x].walls['E'] and
                        not self.grid[y+1][x+1].walls['W']):
                    return True
        return False

    def _remove_wall(self, current: Cell, next_cell: Cell) -> None:
        """Removes the wall between two adjacent cells."""
        dx = next_cell.x - current.x
        dy = next_cell.y - current.y

        if dx == 1:
            """Moved East."""
            current.walls['E'], next_cell.walls['W'] = False, False
        elif dx == -1:
            """Moved West."""
            current.walls['W'], next_cell.walls['E'] = False, False
        elif dy == 1:
            """Moved South."""
            current.walls['S'], next_cell.walls['N'] = False, False
        elif dy == -1:
            """Moved North."""
            current.walls['N'], next_cell.walls['S'] = False, False

    def _open_entry_exit_walls(self) -> None:
        """Opens the external walls for the entry and exit points."""
        if self.entry[1] == 0:
            self.grid[self.entry[1]][self.entry[0]].walls['N'] = False
        if self.entry[0] == 0:
            self.grid[self.entry[1]][self.entry[0]].walls['W'] = False
        if self.entry[1] == self.height - 1:
            self.grid[self.entry[1]][self.entry[0]].walls['S'] = False
        if self.entry[0] == self.width - 1:
            self.grid[self.entry[1]][self.entry[0]].walls['E'] = False

        if self.exit[1] == 0:
            self.grid[self.exit[1]][self.exit[0]].walls['N'] = False
        if self.exit[0] == 0:
            self.grid[self.exit[1]][self.exit[0]].walls['W'] = False
        if self.exit[1] == self.height - 1:
            self.grid[self.exit[1]][self.exit[0]].walls['S'] = False
        if self.exit[0] == self.width - 1:
            self.grid[self.exit[1]][self.exit[0]].walls['E'] = False

    def _bfs_path(self, forbidden_edge: Optional[Tuple[Tuple[int, int],
                                                       Tuple[int, int]]] = None
                  ) -> Optional[List[Tuple[int, int]]]:
        """Internal BFS that returns one path from entry to exit as a list
        of (x, y) coordinates. If ``forbidden_edge`` is provided, that
        undirected edge is ignored during the search.
        """

        start = (self.entry[0], self.entry[1])
        goal = (self.exit[0], self.exit[1])

        queue: List[Tuple[int, int]] = [start]
        came_from: dict[Tuple[int, int], Optional[Tuple[int, int]]] = {
            start: None
        }

        """Helper to reject traversal through the forbidden edge."""
        def edge_is_forbidden(a: Tuple[int, int], b: Tuple[int, int]) -> bool:
            if forbidden_edge is None:
                return False
            (fx1, fy1), (fx2, fy2) = forbidden_edge
            return ((a[0] == fx1 and a[1] == fy1 and
                     b[0] == fx2 and b[1] == fy2) or
                    (a[0] == fx2 and a[1] == fy2 and
                     b[0] == fx1 and b[1] == fy1))

        while queue:
            x, y = queue.pop(0)
            if (x, y) == goal:
                """Reconstruct a path from goal to start using parents."""
                path: List[Tuple[int, int]] = []
                cur: Optional[Tuple[int, int]] = goal
                while cur is not None:
                    path.append(cur)
                    cur = came_from[cur]
                path.reverse()
                return path

            cell = self.grid[y][x]
            """Explore neighbors according to open walls."""
            """North."""
            if (not cell.walls['N'] and y > 0):
                nx, ny = x, y - 1
                if ((nx, ny) not in came_from and
                        not edge_is_forbidden((x, y), (nx, ny))):
                    came_from[(nx, ny)] = (x, y)
                    queue.append((nx, ny))
            """East."""
            if (not cell.walls['E'] and x < self.width - 1):
                nx, ny = x + 1, y
                if ((nx, ny) not in came_from and
                        not edge_is_forbidden((x, y), (nx, ny))):
                    came_from[(nx, ny)] = (x, y)
                    queue.append((nx, ny))
            """South."""
            if (not cell.walls['S'] and y < self.height - 1):
                nx, ny = x, y + 1
                if ((nx, ny) not in came_from and
                        not edge_is_forbidden((x, y), (nx, ny))):
                    came_from[(nx, ny)] = (x, y)
                    queue.append((nx, ny))
            """West."""
            if (not cell.walls['W'] and x > 0):
                nx, ny = x - 1, y
                if ((nx, ny) not in came_from and
                        not edge_is_forbidden((x, y), (nx, ny))):
                    came_from[(nx, ny)] = (x, y)
                    queue.append((nx, ny))

        return None

    def _has_multiple_solutions(self) -> bool:
        """Returns True if at least two distinct paths exist between
        the entry and exit points.

        First computes one path using BFS, then virtually removes
        each edge of that path one by one. If for at least one edge,
        another path still exists, then there are multiple solutions.
        """

        path = self._bfs_path()
        if path is None or len(path) <= 1:
            return False

        """Iterate through each consecutive edge of the path found"""
        for i in range(len(path) - 1):
            a = path[i]
            b = path[i + 1]
            if self._bfs_path(forbidden_edge=(a, b)) is not None:
                return True
        return False

    def _add_extra_passages(self) -> None:
        """Adds extra openings to create loops in the maze.

        Progressively opens walls between random neighboring cells
        until at least two different paths exist between entry and exit
        (or no more internal walls to open).
        """

        if self._has_multiple_solutions():
            return

        """List all internal walls that may be opened."""
        candidates: List[Tuple[Tuple[int, int], Tuple[int, int]]] = []
        for y in range(self.height):
            for x in range(self.width):
                cell = self.grid[y][x]
                if cell.pattern:
                    continue
                """Inspect eastern neighbor wall."""
                if x < self.width - 1:
                    neighbor = self.grid[y][x + 1]
                    if (not neighbor.pattern and
                            cell.walls['E'] and neighbor.walls['W']):
                        candidates.append(((x, y), (x + 1, y)))
                """Inspect southern neighbor wall."""
                if y < self.height - 1:
                    neighbor = self.grid[y + 1][x]
                    if (not neighbor.pattern and
                            cell.walls['S'] and neighbor.walls['N']):
                        candidates.append(((x, y), (x, y + 1)))

        random.shuffle(candidates)

        for (x1, y1), (x2, y2) in candidates:
            cell1 = self.grid[y1][x1]
            cell2 = self.grid[y2][x2]

            """Open one candidate wall."""
            self._remove_wall(cell1, cell2)

            """Stop once multiple solutions are detected."""
            if self._has_multiple_solutions():
                return

    def generate(self) -> None:
        stack: List[Cell] = []

        start_cell = None
        while start_cell is None or start_cell.visited:
            start_x = random.randint(0, self.width - 1)
            start_y = random.randint(0, self.height - 1)
            start_cell = self.grid[start_y][start_x]

        start_cell.visited = True
        stack.append(start_cell)

        while stack:
            current_cell = stack[-1]
            neighbors = self._get_unvisited_neighbors(current_cell)

            """Use classic DFS neighbors in perfect mode.

            In non-perfect mode, filter neighbors with the open-area
            heuristic to avoid creating large empty regions.
            """
            if self.perfect:
                valid_neighbors = neighbors
            else:
                valid_neighbors = [
                    n for n in neighbors
                    if not self._creates_large_open_area(current_cell, n)
                ]
            if valid_neighbors:
                """Pick and visit a valid neighbor."""
                next_cell = random.choice(valid_neighbors)
                self._remove_wall(current_cell, next_cell)
                next_cell.visited = True
                stack.append(next_cell)
            else:
                """Backtrack when no valid neighbors remain."""
                stack.pop()
        """Optionally open outer border walls for entry and exit."""
        """self._open_entry_exit_walls()"""

        """In imperfect mode, add loops for multiple solutions."""
        if not self.perfect:
            self._add_extra_passages()

    def get_grid(self) -> List[List[Cell]]:
        """Returns the generated maze grid."""
        return self.grid

    def swap_color(self) -> None:
        """ANSI color indexes used for random palette rotation."""
        colors_list = ["1",
                       "2",
                       "3",
                       "4",
                       "5",
                       "6",
                       "7"
                       ]
        for key in self.colors.keys():
            color = random.choice(colors_list)
            colors_list.remove(color)
            if key == "SOL":
                self.colors[key] = f"\033[4{color}m  \033[0m"
            elif key == "WALL":
                self.colors[key] = f"\033[9{color}m██\033[0m"
            else:
                self.colors[key] = f"\033[3{color}m██\033[0m"

    def display_solution_path(self) -> None:
        if self.colors["SOL"] != self.colors["PATH"]:
            self.colors["SOL"] = self.colors["PATH"]
        else:
            self.colors["SOL"] = "\033[42m  \033[0m"

    def solve(self) -> Optional[str]:
        start_cell = self.grid[self.entry[1]][self.entry[0]]
        end_cell = self.grid[self.exit[1]][self.exit[0]]

        queue: List[Tuple[Cell, str]] = [(start_cell, "")]
        visited: set[Cell] = {start_cell}

        while queue:
            current_cell, path = queue.pop(0)

            """Return as soon as the end cell is reached."""
            if current_cell == end_cell:
                self.solution = path
                return path

            """Explore reachable neighbors."""
            x, y = current_cell.x, current_cell.y

            """North."""
            if (not current_cell.walls['N'] and y > 0 and
                    self.grid[y-1][x] not in visited):
                visited.add(self.grid[y-1][x])
                queue.append((self.grid[y-1][x], path + "N"))
            """East."""
            if (not current_cell.walls['E'] and x < self.width - 1 and
                    self.grid[y][x+1] not in visited):
                visited.add(self.grid[y][x+1])
                queue.append((self.grid[y][x+1], path + "E"))
            """South."""
            if (not current_cell.walls['S'] and y < self.height - 1 and
                    self.grid[y+1][x] not in visited):
                visited.add(self.grid[y+1][x])
                queue.append((self.grid[y+1][x], path + "S"))
            """West."""
            if (not current_cell.walls['W'] and x > 0 and
                    self.grid[y][x-1] not in visited):
                visited.add(self.grid[y][x-1])
                queue.append((self.grid[y][x-1], path + "W"))
        self.solution = None
        return None

    def get_solution(self) -> Optional[str]:
        """
        Returns the solution path if the maze has been solved.

        Returns:
            Optional[str]: The solution path, or None if solve() has not
                           been called or no path exists.
        """
        return self.solution
