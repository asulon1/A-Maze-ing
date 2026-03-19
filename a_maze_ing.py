# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  a_maze_ing.py                                     :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: asulon <asulon@student.42.fr>             +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 0026/03/08 00:24:33 by sulon           #+#    #+#               #
#  Updated: 2026/03/19 19:18:50 by asulon          ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

from typing import Dict


def parse_config(filename: str) -> Dict[str, str]:

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
        print(f"Error while parsing_config : {error}")

    return config


def check_config_errors(config: Dict[str, str]) -> bool:
    print(config)
    pass


def main():
    config = parse_config("config.txt")
    check_config_errors(config)
    # TODO: Get data from config.txt
    # check valid data
    pass


if __name__ == "__main__":
    main()
