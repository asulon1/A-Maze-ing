# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  a_maze_ing.py                                     :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: asulon <asulon@student.42nice.fr>         +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 0026/03/08 00:24:33 by sulon           #+#    #+#               #
#  Updated: 2026/04/05 22:55:38 by asulon          ###   ########.fr        #
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
                """split Key value"""
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


def write_maze_to_file(generator: MazeGenerator, file: str):
    """Writes the maze structure and solution to a file."""
    wall = {'N': 1, 'E': 2, 'S': 4, 'W': 8}

    try:
        with open(file, 'w') as f:
            for row in generator.get_grid():
                row_arr = []
                for cell in row:
                    wall_value = 0
                    if cell.walls['N']:
                        wall_value += wall['N']
                    if cell.walls['E']:
                        wall_value += wall['E']
                    if cell.walls['S']:
                        wall_value += wall['S']
                    if cell.walls['W']:
                        wall_value += wall['W']
                    row_arr.append(f"{wall_value:X}")
                f.write("".join(row_arr) + '\n')

            f.write('\n')
            f.write(f"{generator.entry[0]},{generator.entry[1]}\n")
            f.write(f"{generator.exit[0]},{generator.exit[1]}\n")
            # add solution
    except IOError as error:
        print(f"Error writing to file '{file}': {error}")
        sys.exit(1)


def display_maze(generator):
    grid = generator.get_grid()
    h, w = len(grid), len(grid[0])

    # 1. On définit nos styles (chaque élément fait exactement 2 caractères de large)
    C_WALL = "\033[97m██\033[0m"        # Blanc
    C_PATH = "  "                       # Vide
    C_START = "\033[35m██\033[0m"       # Violet (entrée)
    C_END = "\033[31m██\033[0m"         # Rouge (sortie)
    C_SOL = "\033[42m  \033[0m"         # Vert (chemin solution)
    C_42 = "\033[33m██\033[0m"          # Jaune pour le motif "42"

    # 2. On crée une matrice de "tags" pour savoir quoi afficher à chaque pixel
    # 'W' = Wall, 'P' = Path, 'S' = Start, 'E' = End, 'X' = Solution, 'F' = motif 42
    render = [["W" for _ in range(2 * w + 1)] for _ in range(2 * h + 1)]

    # 3. On calcule le chemin de la solution en coordonnées de rendu
    sol_coords = set()
    if generator.solution:
        curr_x, curr_y = generator.entry
        # Position de départ dans le rendu : (2*y+1, 2*x+1)
        sol_coords.add((2 * curr_y + 1, 2 * curr_x + 1))

        for move in generator.solution:
            # On doit marquer la cellule ET le passage entre les cellules
            dy, dx = 0, 0
            if move == 'N':
                dy = -1
            elif move == 'S':
                dy = 1
            elif move == 'E':
                dx = 1
            elif move == 'W':
                dx = -1

            # Passage (le "mur" cassé)
            sol_coords.add((2 * curr_y + 1 + dy, 2 * curr_x + 1 + dx))
            # Nouvelle cellule
            curr_y += dy
            curr_x += dx
            sol_coords.add((2 * curr_y + 1, 2 * curr_x + 1))

    # 4. On "creuse" le labyrinthe dans la matrice de rendu
    for y in range(h):
        for x in range(w):
            ry, rx = 2 * y + 1, 2 * x + 1
            cell = grid[y][x]

            # Si la cellule fait partie du motif "42", on la marque
            # spécifiquement et on ne creuse pas autour (tous les murs restent).
            if getattr(cell, "pattern", False):
                render[ry][rx] = 'F'
                continue

            # La cellule elle-même
            render[ry][rx] = 'P'

            # Les murs (si pas de mur, on devient un chemin 'P')
            if not cell.walls['N']:
                render[ry-1][rx] = 'P'
            if not cell.walls['S']:
                render[ry+1][rx] = 'P'
            if not cell.walls['W']:
                render[ry][rx-1] = 'P'
            if not cell.walls['E']:
                render[ry][rx+1] = 'P'

    # 5. On place la solution, l'entrée et la sortie par-dessus
    for (sy, sx) in sol_coords:
        render[sy][sx] = 'X'

    ex, ey = generator.entry
    render[2 * ey + 1][2 * ex + 1] = 'S'

    ox, oy = generator.exit
    render[2 * oy + 1][2 * ox + 1] = 'E'

    # 6. Affichage final
    for row in render:
        line = ""
        for cell in row:
            if cell == 'W':
                line += C_WALL
            elif cell == 'S':
                line += C_START
            elif cell == 'E':
                line += C_END
            elif cell == 'X':
                line += C_SOL
            # elif cell == 'F':
            #     line += C_42
            else:
                line += C_PATH
        print(line)


def main():
    if (len(sys.argv) != 2):
        print(f"Usage: {sys.argv[0]} <config_file>")
        sys.exit(1)
    raw_config = parse_config(sys.argv[1])
    config = validate_config(raw_config)

    try:
        generator = MazeGenerator(
            width=config['WIDTH'],
            height=config['HEIGHT'],
            seed=config.get('SEED'),
            entry=config['ENTRY'],
            exit=config['EXIT'],
            perfect=config['PERFECT']
        )
        generator.generate()
        print("Maze generated successfully.")

        write_maze_to_file(generator, config['OUTPUT_FILE'])
        print(f"Maze written to {config['OUTPUT_FILE']}")

        display_maze(generator)
        # TODO: add solution path
    except ValueError as error:
        print(f"Error: {error}")
        sys.exit(1)


if __name__ == "__main__":
    main()
