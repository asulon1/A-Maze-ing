# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  __init__.py                                       :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: asulon <asulon@student.42.fr>             +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/03/22 12:22:30 by asulon          #+#    #+#               #
#  Updated: 2026/04/10 19:57:25 by asulon          ###   ########.fr        #
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
        # Define the shape of "4" and "2" as coordinates relative to a 5x3 box.
        pattern_4 = [
            (0, 0), (2, 0), (0, 1), (1, 1), (2, 1),
            (2, 2), (2, 3), (2, 4)
        ]
        pattern_2 = [
            (0, 0), (1, 0), (2, 0), (2, 1), (0, 2), (1, 2), (2, 2),
            (0, 3), (0, 4), (1, 4), (2, 4)
        ]

        # Check if maze is large enough to put 42 in it
        # (5x8 cells + borders)
        if self.width < 9 or self.height < 7:
            print("Warning: Maze too small to draw '42' pattern.")
            return

        # Top-left starting pos

        start_x = (self.width - 8) // 2
        start_y = (self.height - 5) // 2

        # Carve the '4' by setting walls and marking as visited.
        for dx, dy in pattern_4:
            x, y = start_x + dx, start_y + dy
            if 0 <= x < self.width and 0 <= y < self.height:
                cell = self.grid[y][x]
                cell.visited = True
                cell.pattern = True
                for wall in cell.walls:
                    cell.walls[wall] = True

        # Carve the '2', offset to the right of the '4'.
        for dx, dy in pattern_2:
            x, y = start_x + dx + 4, start_y + dy
            if 0 <= x < self.width and 0 <= y < self.height:
                cell = self.grid[y][x]
                cell.visited = True
                cell.pattern = True

                for wall in cell.walls:
                    cell.walls[wall] = True

    def _get_unvisited_neighbors(self, cell: Cell) -> List[Cell]:
        """Return unvisited cells next to given cell"""
        neighbors = []
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
        # Check for vertical move creating a 2x2 open area
        if cell1.x == cell2.x:
            x = cell1.x
            y = min(cell1.y, cell2.y)
            # Check left side
            if (x > 0 and not self.grid[y][x].walls['W'] and
                    not self.grid[y+1][x].walls['W']):
                if (not self.grid[y][x-1].walls['S'] and
                        not self.grid[y+1][x-1].walls['N']):
                    return True
            # Check right side
            if (x < self.width - 1 and not self.grid[y][x].walls['E'] and
                    not self.grid[y+1][x].walls['E']):
                if (not self.grid[y][x+1].walls['S'] and
                        not self.grid[y+1][x+1].walls['N']):
                    return True
        # Check for horizontal move creating a 2x2 open area
        else:
            y = cell1.y
            x = min(cell1.x, cell2.x)
            # Check above
            if (y > 0 and not self.grid[y][x].walls['N'] and
                    not self.grid[y][x+1].walls['N']):
                if (not self.grid[y-1][x].walls['E'] and
                        not self.grid[y-1][x+1].walls['W']):
                    return True
            # Check below
            if (y < self.height - 1 and not self.grid[y][x].walls['S'] and
                    not self.grid[y][x+1].walls['S']):
                if (not self.grid[y+1][x].walls['E'] and
                        not self.grid[y+1][x+1].walls['W']):
                    return True
        return False

    def _remove_wall(self, current: Cell, next_cell: Cell):
        """Removes the wall between two adjacent cells."""
        dx = next_cell.x - current.x
        dy = next_cell.y - current.y

        if dx == 1:  # Moved East
            current.walls['E'], next_cell.walls['W'] = False, False
        elif dx == -1:  # Moved West
            current.walls['W'], next_cell.walls['E'] = False, False
        elif dy == 1:  # Moved South
            current.walls['S'], next_cell.walls['N'] = False, False
        elif dy == -1:  # Moved North
            current.walls['N'], next_cell.walls['S'] = False, False

    def _open_entry_exit_walls(self):
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

    def generate(self):
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
            valid_neighbors = [
                n for n in neighbors
                if not self._creates_large_open_area(current_cell, n)
            ]
            if valid_neighbors:
                # If there's a valid neighbor, pick one randomly.
                next_cell = random.choice(valid_neighbors)
                self._remove_wall(current_cell, next_cell)
                next_cell.visited = True
                stack.append(next_cell)  # Move to the next cell.
            else:
                # If there are no valid neighbors, backtrack.
                stack.pop()
        # Ensure the entry and exit points have an opening on the maze's
        # outer border.
        # self._open_entry_exit_walls()

    def get_grid(self) -> List[List[Cell]]:
        """Returns the generated maze grid."""
        return self.grid

    def solve(self) -> Optional[str]:
        start_cell = self.grid[self.entry[1]][self.entry[0]]
        end_cell = self.grid[self.exit[1]][self.exit[0]]

        queue: List[Tuple[Cell, str]] = [(start_cell, "")]
        visited: set[Cell] = {start_cell}

        while queue:
            current_cell, path = queue.pop(0)

            # current_cell reach the end
            if current_cell == end_cell:
                self.solution = path
                return path

            # explore neighbors
            x, y = current_cell.x, current_cell.y

            # North
            if (not current_cell.walls['N'] and y > 0 and
                    self.grid[y-1][x] not in visited):
                visited.add(self.grid[y-1][0])
                queue.append((self.grid[y-1][x], path + "N"))
            # East
            if (not current_cell.walls['E'] and x < self.width - 1 and
                    self.grid[y][x+1] not in visited):
                visited.add(self.grid[y][x+1])
                queue.append((self.grid[y][x+1], path + "E"))
            # South
            if (not current_cell.walls['S'] and y < self.height - 1 and
                    self.grid[y+1][x] not in visited):
                visited.add(self.grid[y+1][x])
                queue.append((self.grid[y+1][x], path + "S"))
            # West
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
