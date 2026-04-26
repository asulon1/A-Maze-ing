# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  a_maze_ing.py                                     :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: asulon <asulon@student.42.fr>             +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 0026/03/08 00:24:33 by sulon           #+#    #+#               #
#  Updated: 2026/04/26 16:35:19 by asulon          ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

from typing import Dict, Any
import sys

from mazegen import MazeGenerator


class ConfigError(Exception):
    def __init__(self, message: str) -> None:
        print(f"Configation Error : {message}")


def parse_config(filename: str) -> Dict[str, str]:
    """Parse data from config file return Dict[Key: Value]"""
    config = {}
    try:
        with open(filename) as file:
            config_list = file.read().split("\n")
            for line in config_list:
                if line.startswith("#"):
                    continue
                splited_line = line.split("=")
                if len(splited_line[0]) > 0:
                    config.update({splited_line[0]: splited_line[1]})
    except (FileNotFoundError, PermissionError) as error:
        ConfigError(f"'{error.filename}' not found")
        sys.exit(1)
    except ValueError:
        ConfigError(f"error near '{line}'")
        sys.exit(1)
    return config


def validate_config(config: Dict[str, Any]) -> Dict[str, Any]:
    """Check config file keys and values"""

    """Checking required keys"""
    required_key = ['WIDTH', 'HEIGHT', 'ENTRY',
                    'EXIT', 'OUTPUT_FILE', 'PERFECT']
    for key in required_key:
        if key not in config:
            print(
                f"Error: Missing mandatory key '{key}' in configuration.")
            sys.exit(1)
    try:
        """Assign new values with the correct types to the config keys"""
        config['WIDTH'] = int(config['WIDTH'])
        config['HEIGHT'] = int(config['HEIGHT'])
        config['ENTRY'] = tuple(map(int, config['ENTRY'].split(',')))
        config['EXIT'] = tuple(map(int, config['EXIT'].split(',')))
        config['PERFECT'] = config['PERFECT'].upper() in [
            "Y", "TRUE", '1', 'YES']
        if 'SEED' in config:
            config['SEED'] = int(config['SEED'])
    except (ValueError, TypeError):
        print("Error: Invalid value type in configuration.")
        sys.exit(1)

    """Testing invalid values"""
    if config['WIDTH'] < 0 or config['HEIGHT'] < 0:
        print("Error: WIDTH and HEIGHT must be positive integers.")
        sys.exit(1)
    w, h = config['WIDTH'], config['HEIGHT']
    if not (0 <= config['ENTRY'][0] <= w and 0 <= config['ENTRY'][1] <= h):
        print("Error : Entry out of bounds")
    if not (0 <= config['EXIT'][0] <= w and 0 <= config['EXIT'][1] <= h):
        print("Error : Entry out of bounds")
    if config['ENTRY'] == config['EXIT']:
        print("Error: ENTRY and EXIT coordinates cannot be the same.")
        sys.exit(1)
    return config


def write_maze_to_file(generator: MazeGenerator, file: str) -> None:
    """Writes the maze structure and solution to a file."""
    wall = {'N': 1, 'E': 2, 'S': 4, 'W': 8}

    try:
        with open(file, 'w') as f:
            for row in generator.get_grid():
                row_arr = []
                for cell in row:
                    wall_value = 0
                    if cell.walls['N']:
                        wall_value |= wall['N']
                    if cell.walls['E']:
                        wall_value |= wall['E']
                    if cell.walls['S']:
                        wall_value |= wall['S']
                    if cell.walls['W']:
                        wall_value |= wall['W']
                    row_arr.append(f"{wall_value:X}")
                f.write("".join(row_arr) + '\n')

            f.write('\n')
            f.write(f"{generator.entry[0]},{generator.entry[1]}\n")
            f.write(f"{generator.exit[0]},{generator.exit[1]}\n")
            solution = generator.get_solution()
            if (solution):
                f.write(solution + '\n')
    except IOError as error:
        print(f"Error writing to file '{file}': {error}")
        sys.exit(1)


def display_maze(generator: MazeGenerator) -> None:
    from typing import List, Set, Tuple, cast
    grid = generator.get_grid()
    h, w = len(grid), len(grid[0])

    # Create a matrix of "tags" to know what to display at each pixel
    # 'W' = Wall, 'P' = Path, 'S' = Start, 'E' = End, 'X' = Solution
    # 'F' = pattern 42
    render: List[List[str]] = cast(List[List[str]],
                                   [["W" for _ in range(2 * w + 1)]
                                    for _ in range(2 * h + 1)])

    # Calculate the solution path in render coordinates
    sol_coords: Set[Tuple[int, int]] = set()
    if generator.solution:
        curr_x, curr_y = generator.entry
        # Starting position in render coordinates: (2*y+1, 2*x+1)
        sol_coords.add((2 * curr_y + 1, 2 * curr_x + 1))

        for move in generator.solution:
            # Mark both the cell and the passage between cells
            dy, dx = 0, 0
            if move == 'N':
                dy = -1
            elif move == 'S':
                dy = 1
            elif move == 'E':
                dx = 1
            elif move == 'W':
                dx = -1

            # The passage (broken wall)
            sol_coords.add((2 * curr_y + 1 + dy, 2 * curr_x + 1 + dx))
            # New cell
            curr_y += dy
            curr_x += dx
            sol_coords.add((2 * curr_y + 1, 2 * curr_x + 1))

    # Carve out the maze in the render matrix
    for y in range(h):
        for x in range(w):
            ry, rx = 2 * y + 1, 2 * x + 1
            cell = grid[y][x]

            # If cell is part of the "42" pattern, mark it and don't carve
            # around it (all walls stay)
            if getattr(cell, "pattern", False):
                render[ry][rx] = 'F'
                continue

            # The cell itself
            render[ry][rx] = 'P'

            # The walls (if no walls, becomes a path 'P')
            if not cell.walls['N']:
                render[ry-1][rx] = 'P'
            if not cell.walls['S']:
                render[ry+1][rx] = 'P'
            if not cell.walls['W']:
                render[ry][rx-1] = 'P'
            if not cell.walls['E']:
                render[ry][rx+1] = 'P'

    # Place solution, entry and exit on top
    for (sy, sx) in sol_coords:
        render[sy][sx] = 'X'

    ex, ey = generator.entry
    render[2 * ey + 1][2 * ex + 1] = 'S'

    ox, oy = generator.exit
    render[2 * oy + 1][2 * ox + 1] = 'E'

    # Final display
    for row in render:
        line = ""
        for char in row:
            if char == 'W':
                line += generator.colors["WALL"]
            elif char == 'S':
                line += generator.colors["START"]
            elif char == 'E':
                line += generator.colors["END"]
            elif char == 'X':
                line += generator.colors["SOL"]
            elif char == 'F':
                line += generator.colors["42"]
            else:
                line += generator.colors["PATH"]
        print(line)


def user_input(generator: MazeGenerator) -> int:
    input_text = "=== A-Maze-ing ===\n" \
        "1. Re-generate a new maze\n" \
        "2. Show/Hide path from entry to exit\n" \
        "3. Rotate maze color\n" \
        "4. Exit\n" \
        "Choise? (1-4): "

    choise = 0
    try:
        while (choise != 4):
            choise = int(input(input_text))
            match choise:
                case 1:
                    generator = generate_maze()
                case 2:
                    generator.display_solution_path()
                    display_maze(generator)
                case 3:
                    generator.swap_color()
                    display_maze(generator)
                case 4:
                    sys.exit(1)
                case _:
                    raise ValueError
    except ValueError:
        print("\nInvalid value : Choose between 1-4\n")
    finally:
        return choise


def generate_maze() -> MazeGenerator:
    raw_config = parse_config(sys.argv[1])
    config = validate_config(raw_config)

    generator = MazeGenerator(
        width=config['WIDTH'],
        height=config['HEIGHT'],
        seed=config.get('SEED'),
        entry=config['ENTRY'],
        exit=config['EXIT'],
        perfect=config['PERFECT']
    )
    generator.generate()

    if generator.solve():
        print("Solution found.")
    else:
        print("No solution found for the maze.")

    write_maze_to_file(generator, config['OUTPUT_FILE'])

    display_maze(generator)
    return generator


def main() -> None:
    if (len(sys.argv) != 2):
        print(f"Usage: {sys.argv[0]} <config_file>")
        sys.exit(1)

    try:
        generator = generate_maze()
        config = 0
        while (config != 4):
            config = user_input(generator)
    except ValueError as error:
        print(f"Error: {error}")
        sys.exit(1)


if __name__ == "__main__":
    main()
