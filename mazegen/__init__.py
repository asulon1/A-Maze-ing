# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  __init__.py                                       :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: asulon <asulon@student.42nice.fr>         +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/03/22 12:22:30 by asulon          #+#    #+#               #
#  Updated: 2026/04/05 22:59:14 by asulon          ###   ########.fr        #
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
        start_x = self.width - 8 // 2
        start_y = self.height - 5 // 2

        # Carve "4" by setting walls as visited
        for pos_x, pos_y in pattern_4:
            x, y = start_x + pos_x, start_y + pos_y
            if 0 <= x < self.width and 0 <= y < self.height:
                cell = self.grid[y][x]
                cell.visited = True
                cell.pattern = True
                for wall in cell.walls:
                    cell.walls[wall] = True
        # Carve "2" by setting walls as visited
        for pos_x, pos_y in pattern_2:
            x, y = start_x + pos_x, start_y + pos_y
            if 0 <= x < self.width and 0 <= y < self.height:
                cell = self.grid[y][x]
                cell.visited = True
                cell.pattern = True
                for wall in cell.walls:
                    cell.walls[wall] = True

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
            pass

    def get_grid(self) -> List[List[Cell]]:
        """Returns the generated maze grid."""
        return self.grid

    def get_solution(self) -> Optional[str]:
        """
        Returns the solution path if the maze has been solved.

        Returns:
            Optional[str]: The solution path, or None if solve() has not
                           been called or no path exists.
        """
        return self.solution
