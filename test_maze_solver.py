import unittest
from pathlib import Path

from maze_solver import Maze, astar, main, manhattan

MAZES = Path(__file__).with_name("mazes")


class MazeTest(unittest.TestCase):

    def test_finds_start_and_end(self):
        maze = Maze("#####\n#S E#\n#####")
        self.assertEqual(maze.start, (1, 1))
        self.assertEqual(maze.end, (1, 3))

    def test_missing_end_raises(self):
        with self.assertRaises(ValueError):
            Maze("####\n#S #\n####")

    def test_neighbors_skip_walls(self):
        maze = Maze("#####\n#S E#\n#####")
        self.assertEqual(list(maze.neighbors((1, 1))), [(1, 2)])

    def test_render_marks_path_but_keeps_endpoints(self):
        maze = Maze("#####\n#S E#\n#####")
        self.assertEqual(maze.render([(1, 1), (1, 2), (1, 3)]).splitlines()[1], "#S.E#")


class AStarTest(unittest.TestCase):

    def test_manhattan(self):
        self.assertEqual(manhattan((0, 0), (3, 4)), 7)

    def test_straight_corridor(self):
        path, _ = astar(Maze("#######\n#S   E#\n#######"))
        self.assertEqual(len(path) - 1, 4)

    def test_finds_shortest_path_around_wall(self):
        maze = Maze(
            "#######\n"
            "#S # E#\n"
            "#  #  #\n"
            "#     #\n"
            "#######"
        )
        path, _ = astar(maze)
        self.assertEqual(path[0], maze.start)
        self.assertEqual(path[-1], maze.end)
        self.assertEqual(len(path) - 1, 8)

    def test_path_steps_are_adjacent(self):
        path, _ = astar(Maze.from_file(MAZES / "large.txt"))
        for a, b in zip(path, path[1:]):
            self.assertEqual(manhattan(a, b), 1)

    def test_unsolvable(self):
        path, explored = astar(Maze.from_file(MAZES / "unsolvable.txt"))
        self.assertIsNone(path)
        self.assertGreater(explored, 0)


class CliTest(unittest.TestCase):

    def test_exit_codes(self):
        from contextlib import redirect_stdout
        from io import StringIO
        with redirect_stdout(StringIO()):
            self.assertEqual(main([str(MAZES / "small.txt")]), 0)
            self.assertEqual(main([str(MAZES / "unsolvable.txt")]), 2)


if __name__ == "__main__":
    unittest.main()
