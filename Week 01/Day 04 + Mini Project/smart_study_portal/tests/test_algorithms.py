import unittest
from algorithms import bfs, ucs, a_star

class TestAlgorithms(unittest.TestCase):
    def setUp(self):
        self.graph = {
            "A": {"B": 4.0, "C": 2.0},
            "B": {"A": 4.0, "D": 5.0},
            "C": {"A": 2.0, "D": 1.0},
            "D": {"B": 5.0, "C": 1.0}
        }
        self.heuristics = {
            "A": 3.0,
            "B": 2.0,
            "C": 1.0,
            "D": 0.0
        }

    def test_bfs_finds_path(self):
        path, cost, explored = bfs(self.graph, "A", "D")
        self.assertIn(path, [["A", "B", "D"], ["A", "C", "D"]])
        self.assertGreater(explored, 0)

    def test_ucs_finds_shortest_path(self):
        path, cost, explored = ucs(self.graph, "A", "D")
        self.assertEqual(path, ["A", "C", "D"])
        self.assertEqual(cost, 3.0)

    def test_a_star_finds_shortest_path(self):
        path, cost, explored = a_star(self.graph, "A", "D", self.heuristics)
        self.assertEqual(path, ["A", "C", "D"])
        self.assertEqual(cost, 3.0)

if __name__ == "__main__":
    unittest.main()
