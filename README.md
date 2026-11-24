# AI Maze Solver (A*)

Solves text mazes with the **A\* search** algorithm and prints the maze with the
shortest path drawn on it. Uses only the Python standard library.

## Features

- A* search with a Manhattan-distance heuristic (guaranteed shortest path)
- Simple text maze format: `#` walls, `S` start, `E` end, spaces are open
- Prints path length and number of explored cells
- Bundled sample mazes in `mazes/`

## Usage

```bash
python3 maze_solver.py mazes/small.txt
```

```
##########
#S   #   #
#.## # # #
#..#   # #
##.##### #
# .....# #
# ####.# #
#    #..E#
##########

Path length: 13 steps, explored 21 cells.
```

Exit codes: `0` solved, `1` invalid maze file, `2` no path exists.

### Maze format

```
#####
#S E#
#####
```

`#` is a wall, `S` the start, `E` the end; any other character is walkable.
Moves are up, down, left and right.

## How it works

A* keeps a priority queue of cells ordered by `f = g + h`, where `g` is the number
of steps taken from the start and `h` is the Manhattan distance to the end. Because
the Manhattan distance never overestimates the remaining steps on a 4-connected grid,
the first time A* reaches the end it has found a shortest path.

## Tests

```bash
python3 -m unittest test_maze_solver.py
```
