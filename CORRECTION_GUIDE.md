# A-Maze-ing - 42 School Correction Guide

## Project Overview

**A-Maze-ing** is a Python terminal maze generator and solver that reads configuration files, generates mazes using randomized DFS, solves them with BFS, and displays them with colored ASCII art.

---

## Architecture & Components

### 1. **Main Entry Point** (`a_maze_ing.py`)
Handles:
- **Configuration Parsing**: `parse_config()` reads key=value config files
- **Configuration Validation**: `validate_config()` type-checks and validates values
- **File I/O**: `write_maze_to_file()` exports maze in hexadecimal encoding
- **Terminal UI**: `display_maze()` renders colored ASCII maze
- **Interactive Menu**: `user_input()` handles user choices (regenerate, toggle solution, swap colors, exit)

### 2. **Maze Generator** (`mazegen/__init__.py`)

#### `Cell` Class
```python
- x, y: Coordinates
- walls: Dict of booleans for N/E/S/W directions
- visited: Boolean flag for generation/solving
- pattern: Boolean for decorative "42" pattern cells
```

#### `MazeGenerator` Class
Handles maze generation, solving, and rendering:

**Key Methods:**
| Method | Purpose |
|--------|---------|
| `generate()` | Randomized DFS backtracking algorithm |
| `solve()` | BFS pathfinding from entry to exit |
| `get_solution()` | Returns solution path as moves (N/E/S/W) |
| `get_grid()` | Returns the 2D cell grid |
| `display_solution_path()` | Toggle solution path visibility |
| `swap_color()` | Rotate through color themes |

---

## Algorithms Explained

### **Generation (Randomized DFS Backtracking)**

1. **Initialization**: Create grid with all walls intact, all cells unvisited
2. **Pick Random Start**: Choose unvisited cell (avoiding pattern cells)
3. **Carve Passages**:
   - Mark current cell as visited
   - Get unvisited neighbors (N/E/S/W)
   - In perfect mode: pick random neighbor
   - In imperfect mode: avoid neighbors creating 2×2 open areas
   - Remove wall between current and neighbor
   - Move to neighbor, repeat
4. **Backtrack**: When stuck, pop from stack until finding viable neighbors
5. **Perfect vs Imperfect**:
   - **Perfect**: Classic DFS spanning tree (exactly one solution)
   - **Imperfect**: Add extra passages after generation for multiple solutions

### **Solving (Breadth-First Search)**

1. **Initialize**: Queue with entry point, visited set with entry
2. **Explore**: For each cell, check 4 neighbors (N/E/S/W) if walls are open
3. **Track Path**: Store parent cell pointers to reconstruct path
4. **Return Path**: Convert coordinates to moves (N/E/S/W)

### **Decorative "42" Pattern**

- Automatically carved for mazes ≥9×7 cells
- Cells marked as `pattern=True` and `visited=True`
- Prevents generation algorithm from modifying them
- Displayed in yellow during rendering

---

## Configuration File Format

```text
WIDTH=10           # Maze width in cells
HEIGHT=8           # Maze height in cells  
ENTRY=0,0          # Entry coordinates (x,y)
EXIT=9,7           # Exit coordinates (x,y)
OUTPUT_FILE=maze.txt  # File to save maze
PERFECT=False      # Perfect=True (1 solution) or False (multiple paths)
# SEED=42          # Optional: integer seed for deterministic generation
```

---

## Output File Format

```
Row 1 maze data (hex wall values)
Row 2: ...
...
Row N: ...
[blank line]
entry_x,entry_y
exit_x,exit_y
solution_moves
```

**Wall Encoding** (hexadecimal):
- N (North) = 0
- E (East) = 1
- S (South) = 2
- W (West) = 3

Example: `F` = 1111 (all walls present)

---

## Key Design Decisions

### Why Randomized DFS?
- ✓ Produces naturally-looking mazes
- ✓ Easy to integrate bidirectional features
- ✓ Deterministic with seeds
- ✓ Efficiently traceable with stack

### 2×2 Open Area Heuristic
Prevents large open spaces in imperfect mazes by checking if removing a wall would complete a 2×2 square. Keeps mazes challenging.

### Entry/Exit Handling
- Coordinates can be on edges
- Wall removal on boundaries creates openings
- Pattern cells are protected from modification

### Color Support
7 colors (red, green, yellow, blue, purple, cyan, white) rotatable for different themes.

---

## Testing Checklist for Correction

- [ ] **Config parsing**: Handles missing keys, invalid types, out-of-bounds coordinates
- [ ] **Perfect maze**: Generates exactly one solution between entry and exit
- [ ] **Imperfect maze**: Multiple paths exist between entry and exit
- [ ] **Large maze**: "42" pattern renders correctly for large maze dimensions
- [ ] **Small maze**: Handles minimal sizes gracefully (3×3)
- [ ] **Edge cases**: 
  - Entry/exit on borders
  - Entry = exit (should error)
  - Negative dimensions (should error)
- [ ] **File output**: Hexadecimal encoding is correct
- [ ] **Solution path**: BFS finds shortest path
- [ ] **Terminal rendering**: Colors display correctly
- [ ] **Interactive menu**: All options work (regenerate, toggle solution, swap colors)
- [ ] **Linting**: `make lint-strict` passes (mypy --strict + flake8)

---

## Code Quality

✓ **Type Annotations**: Full strict mypy compliance  
✓ **Code Style**: PEP 8 compliance via flake8  
✓ **Documentation**: Comments explain algorithm logic  
✓ **Modularity**: Reusable Cell and MazeGenerator classes  

---

## Reusable Components

You can extract and reuse:
- `MazeGenerator` class for other maze applications
- `Cell` model for grid-based algorithms
- `parse_config()` / `validate_config()` for config files
- `write_maze_to_file()` for maze serialization
- `display_maze()` for ASCII rendering

---

## Common Questions for Correction

**Q: Why BFS for solving instead of DFS?**  
A: BFS guarantees shortest path; practical for verification.

**Q: How does "42" pattern avoid breaking connectivity?**  
A: Pattern cells are pre-marked visited, so DFS naturally goes around them.

**Q: Why cast() in display_maze()?**  
A: Helps mypy --strict type checker recognize render matrix as List[List[str]]

**Q: What happens if no solution exists?**  
A: BFS returns None; main program prints "No solution found"

---

## Running Your Project

```bash
# Install dependencies
make install

# Run with default config
make run

# Debug with pdb
make debug

# Check code quality
make lint-strict

# Clean build artifacts
make clean
```

---

## Files Modified for Correction

- ✅ `a_maze_ing.py`: Added type annotations, fixed line lengths
- ✅ `mazegen/__init__.py`: Added return type annotations
- Both files now pass `mypy --strict` and `flake8`
