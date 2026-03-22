# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  __init__.py                                       :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: asulon <asulon@student.42nice.fr>         +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/03/22 12:22:30 by asulon          #+#    #+#               #
#  Updated: 2026/03/22 14:10:12 by asulon          ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

import random
from typing import List, Tuple, Optional


class Cell:
    """
    Represents a single cell within the maze's grid.

    Attributes:
        x (int): The x-coordinate of the cell.
        y (int): The y-coordinate of the cell.
        walls (dict[str, bool]): A dictionary tracking the state of the four
                                 walls ('N', 'E', 'S', 'W'). True means a
                                 wall exists.
        visited (bool): A flag used by generation and solving algorithms.
    """

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.walls = {'N': True, 'E': True, 'S': True, 'W': True}
        self.visited = False
        self.pattern = False


class MazeGenerator:
    def __init__(self, width: int, height: int, seed: Optional[int] = None,
                 entry: Tuple[int, int] = (0, 0),
                 exit: Tuple[int, int] = (0, 0),
                 perfect: bool = True) -> None:
        if width <= 0 or height <= 0:
            raise ValueError("Width and height must be positive.")
        self.width = width
        self.height = height
        self.seed = seed
        self.entry = entry
        self.exit = exit
        self.perfect = perfect
        self.grid: List[List[Cell]] = []
        self.solution: Optional[str] = None

        if self.seed is not None:
            random.seed(self.seed)

        self._initialize_grid()
        self._carve_42_pattern()
