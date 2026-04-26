_This project has been created as part of the 42 curriculum by asulon, klucchin._

# A-Maze-ing

## Description

A-Maze-ing is a Python terminal-based maze generator and solver created for the 42 curriculum. The project reads a configuration file, generates a maze using a randomized depth-first search algorithm, solves the maze from entry to exit, writes the maze data to a file, and displays a colored ASCII rendering in the terminal.

This project supports both perfect mazes (exactly one solution) and imperfect mazes with additional loops. It also includes a decorative "42" pattern carved into large enough mazes.

## Instructions

### Requirements

- Python 3
- No external runtime dependencies are required for core execution.
- Optional development tools are listed in `requirements.txt`:
  - `flake8`
  - `mypy`

### Running the project

1. Ensure `config.txt` is present in the root directory or create a configuration file.
2. Run the generator with:

```bash
make run
```

3. Follow the terminal menu to re-generate the maze, show/hide the solution path, rotate color themes, or exit.

### Config file format

The configuration file is a simple key/value text file. Blank lines and lines starting with `#` are ignored.

Required keys:

- `WIDTH` — maze width in cells
- `HEIGHT` — maze height in cells
- `ENTRY` — entry coordinate as `x,y`
- `EXIT` — exit coordinate as `x,y`
- `OUTPUT_FILE` — output file path for the generated maze data
- `PERFECT` — `True`/`False` to choose between a perfect or imperfect maze

Optional key:

- `SEED` — integer seed for deterministic maze generation

Example:

```text
WIDTH=3
HEIGHT=4
ENTRY=0,0
EXIT=0,2
OUTPUT_FILE=maze.txt
PERFECT=False
# SEED=4
```

### Output format

The output maze file contains:

- one line per maze row with hexadecimal wall values for each cell
- a blank line
- entry coordinates
- exit coordinates
- the solution path as a sequence of moves (`N`, `E`, `S`, `W`)

## Maze generation algorithm

This project uses a randomized depth-first search (DFS) backtracking algorithm to generate the maze. The algorithm starts from a random unvisited cell, carves passages by removing walls between adjacent cells, and backtracks when it reaches a dead end until all reachable cells have been visited.

In perfect mode, the result is a perfect maze with a unique path between any two cells. In imperfect mode, the project adds extra passages after generation to create loops and multiple possible solutions between entry and exit.

## Why this algorithm

The randomized DFS algorithm was chosen because:

- it is simple to implement and easy to reason about,
- it naturally produces a maze with a clear traversal structure,
- it lends itself to both perfect and imperfect maze variants,
- it is easy to integrate with custom features like the decorative "42" pattern.

## Reusable code

The following parts of the project are reusable:

- `mazegen/MazeGenerator` — a reusable class for maze generation, solving, and grid access.
- `mazegen.Cell` — a reusable cell model with wall and visited state.
- `parse_config` and `validate_config` in `a_maze_ing.py` — reusable utilities for configuration parsing and validation.
- `write_maze_to_file` — reusable output serialization logic for maze export.
- `display_maze` — reusable terminal rendering logic for maze visualization.

These components can be extracted into another project for command-line maze tools, educational algorithm demos, or automated maze testing.

## Resources

- Maze generation overview: https://en.wikipedia.org/wiki/Maze_generation_algorithm
- Depth-first search maze generation: https://weblog.jamisbuck.org/2010/12/27/maze-generation-depth-first-search
- Maze solving with breadth-first search: https://en.wikipedia.org/wiki/Breadth-first_search

AI usage:

- AI was used to write and structure this README file.
- AI was used to summarize the project features, explain the configuration format, and document the algorithm choices.
- The core maze generation and solver code was implemented by the project team without AI writing the main algorithm.

## Planning and retrospective

### Planning evolution

The project began with a simple goal: build a configurable maze generator and solver from a text-based config file. Early planning focused on parsing user configuration, generating a maze grid, and rendering a terminal output. As development progressed, the plan expanded to support both perfect and imperfect mazes, deterministic seeds, and a decorative "42" pattern.

### What worked well

- The maze generator architecture was effective: separating `MazeGenerator` from `a_maze_ing.py` kept generation logic reusable.
- Config parsing and validation provided a clean execution flow and helped catch invalid user input early.
- The terminal display and color themes made the project easy to inspect during development.

### What could be improved

- The current solver and generation code could be refactored to separate pathfinding, rendering, and configuration concerns more cleanly.
- More robust boundary validation for entry/exit placement would improve user feedback.
- Adding automated tests would help ensure maze properties remain correct after future changes.

### Tools used

- Python3 for implementation.
- `flake8` for code style checks.
- `mypy` for static type checking.
- The editor environment and terminal for development.

## Team

- Role assignments are intentionally left empty.
