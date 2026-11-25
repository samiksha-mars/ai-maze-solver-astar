"""Solve text mazes with A* search."""

import argparse
import heapq
import sys

WALL, START, END, PATH = "#", "S", "E", "."


class Maze:

    def __init__(self, text):
        lines = text.splitlines()
        # Trim blank lines around the maze, but keep blank rows inside it: they are open cells.
        while lines and not lines[0].strip():
            lines.pop(0)
        while lines and not lines[-1].strip():
            lines.pop()
        if not lines:
            raise ValueError("maze is empty")
        width = max(len(line) for line in lines)
        self.grid = [list(line.ljust(width)) for line in lines]
        self.start = self._find(START)
        self.end = self._find(END)

    @classmethod
    def from_file(cls, path):
        with open(path, encoding="utf-8") as f:
            return cls(f.read())

    def _find(self, symbol):
        for r, row in enumerate(self.grid):
            for c, cell in enumerate(row):
                if cell == symbol:
                    return (r, c)
        raise ValueError(f"maze has no '{symbol}' cell")

    def neighbors(self, cell):
        r, c = cell
        for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            nr, nc = r + dr, c + dc
            if 0 <= nr < len(self.grid) and 0 <= nc < len(self.grid[nr]) \
                    and self.grid[nr][nc] != WALL:
                yield (nr, nc)

    def render(self, path=()):
        grid = [row.copy() for row in self.grid]
        for r, c in path:
            if grid[r][c] not in (START, END):
                grid[r][c] = PATH
        return "\n".join("".join(row).rstrip() for row in grid)


def manhattan(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def astar(maze):
    """Return (path, explored_count). `path` is None if the maze has no solution."""
    start, goal = maze.start, maze.end
    open_heap = [(manhattan(start, goal), 0, start)]
    came_from = {}
    cost = {start: 0}
    explored = set()

    while open_heap:
        _, g, current = heapq.heappop(open_heap)
        if current in explored:
            continue
        explored.add(current)
        if current == goal:
            path = [current]
            while current in came_from:
                current = came_from[current]
                path.append(current)
            return path[::-1], len(explored)
        for neighbor in maze.neighbors(current):
            new_cost = g + 1
            if new_cost < cost.get(neighbor, float("inf")):
                cost[neighbor] = new_cost
                came_from[neighbor] = current
                heapq.heappush(open_heap, (new_cost + manhattan(neighbor, goal), new_cost, neighbor))
    return None, len(explored)


def main(argv=None):
    parser = argparse.ArgumentParser(description="Solve a text maze with A* search.")
    parser.add_argument("maze", help="path to a maze file (# walls, S start, E end)")
    args = parser.parse_args(argv)

    try:
        maze = Maze.from_file(args.maze)
    except (OSError, ValueError) as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

    path, explored = astar(maze)
    if path is None:
        print(maze.render())
        print(f"\nNo path found (explored {explored} cells).")
        return 2
    print(maze.render(path))
    print(f"\nPath length: {len(path) - 1} steps, explored {explored} cells.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
