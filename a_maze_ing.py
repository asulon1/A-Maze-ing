# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  a_maze_ing.py                                     :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: asulon <asulon@student.42nice.fr>         +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 0026/03/08 00:24:33 by sulon           #+#    #+#               #
#  Updated: 2026/03/23 21:15:06 by asulon          ###   ########.fr        #
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

        # TODO: init maze generator
        # create maze
    except ValueError as error:
        print(f"Error: {error}")
        sys.exit(1)


if __name__ == "__main__":
    main()
