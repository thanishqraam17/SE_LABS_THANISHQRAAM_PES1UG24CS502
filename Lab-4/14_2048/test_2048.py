"""Run with:  python -m unittest test_2048 -v"""
import builtins
import io
import sys
import unittest

from board import Board
from game import Game


def game_with(grid, score=0):
    g = Game()
    g.board.grid = [row[:] for row in grid]
    g.board.score = score
    return g


def tile_count(board):
    return sum(1 for r in board.grid for x in r if x)


def play(inputs, game=None):
    """Feed scripted input to Game.run() and return everything it printed."""
    it = iter(inputs)
    old_in, old_out = builtins.input, sys.stdout
    builtins.input = lambda prompt="": next(it)
    sys.stdout = io.StringIO()
    try:
        (game or Game()).run()
        return sys.stdout.getvalue()
    finally:
        builtins.input, sys.stdout = old_in, old_out


class TestMerge(unittest.TestCase):
    def test_ordinary_slide(self):
        self.assertEqual(Board.slide_line([0, 2, 0, 4])[0], [2, 4, 0, 0])

    def test_four_equal(self):
        self.assertEqual(Board.slide_line([2, 2, 2, 2])[0], [4, 4, 0, 0])

    def test_three_equal(self):
        self.assertEqual(Board.slide_line([2, 2, 2, 0])[0], [4, 2, 0, 0])

    def test_no_chain_merge(self):  # the original bug: [2,2,4] became [8]
        self.assertEqual(Board.slide_line([2, 2, 4, 0])[0], [4, 4, 0, 0])
        self.assertEqual(Board.slide_line([4, 2, 2, 4])[0], [4, 4, 4, 0])

    def test_separated_equal_pair(self):
        self.assertEqual(Board.slide_line([2, 0, 0, 2])[0], [4, 0, 0, 0])
        self.assertEqual(Board.slide_line([2, 4, 2, 4])[0], [2, 4, 2, 4])

    def test_all_directions(self):
        row = [[2, 2, 4, 0]] + [[0] * 4 for _ in range(3)]
        g = game_with(row)
        g.board.move_left()
        self.assertEqual(g.board.grid[0], [4, 4, 0, 0])
        g = game_with(row)
        g.board.move_right()
        self.assertEqual(g.board.grid[0], [0, 0, 4, 4])
        col = [[2, 0, 0, 0], [2, 0, 0, 0], [4, 0, 0, 0], [0, 0, 0, 0]]
        g = game_with(col)
        g.board.move_up()
        self.assertEqual([r[0] for r in g.board.grid], [4, 4, 0, 0])
        g = game_with(col)
        g.board.move_down()
        self.assertEqual([r[0] for r in g.board.grid], [0, 0, 4, 4])

    def test_score_increases_on_merge(self):
        g = game_with([[2, 2, 4, 4]] + [[0] * 4 for _ in range(3)])
        g.board.move_left()
        self.assertEqual(g.board.score, 12)


class TestGameState(unittest.TestCase):
    def test_unchanged_move_spawns_nothing(self):
        g = game_with([[2, 4, 0, 0]] + [[0] * 4 for _ in range(3)])
        before = [r[:] for r in g.board.grid]
        self.assertFalse(g.move("a"))
        self.assertEqual(g.board.grid, before)

    def test_changed_move_spawns_one_tile(self):
        g = game_with([[0, 0, 0, 2]] + [[0] * 4 for _ in range(3)])
        self.assertTrue(g.move("a"))
        self.assertEqual(tile_count(g.board), 2)

    def test_win_detected(self):
        g = game_with([[1024, 1024, 0, 0]] + [[0] * 4 for _ in range(3)])
        g.board.move_left()
        self.assertTrue(g.board.has_won())

    def test_win_ends_game(self):
        g = game_with([[2048, 0, 0, 0]] + [[0] * 4 for _ in range(3)])
        self.assertIn("You reached 2048", play([], g))

    def test_no_moves_on_full_board(self):
        g = game_with([[2, 4, 2, 4], [4, 2, 4, 2], [2, 4, 2, 4], [4, 2, 4, 2]])
        self.assertFalse(g.board.can_move())

    def test_no_moves_ends_game(self):
        g = game_with([[2, 4, 2, 4], [4, 2, 4, 2], [2, 4, 2, 4], [4, 2, 4, 2]])
        self.assertIn("No legal moves", play([], g))

    def test_full_board_with_merge_still_playable(self):
        g = game_with([[2, 2, 2, 4], [4, 2, 4, 2], [2, 4, 2, 4], [4, 2, 4, 2]])
        self.assertTrue(g.board.can_move())


class TestUndoAndBest(unittest.TestCase):
    def test_undo_restores_board_and_score_without_tile(self):
        g = game_with([[2, 2, 4, 0], [0, 0, 0, 2], [0] * 4, [0] * 4], score=10)
        orig = [r[:] for r in g.board.grid]
        g.move("a")
        self.assertTrue(g.undo())
        self.assertEqual(g.board.grid, orig)
        self.assertEqual(g.board.score, 10)

    def test_undo_only_one_level(self):
        g = game_with([[0, 0, 0, 2]] + [[0] * 4 for _ in range(3)])
        g.move("a")
        g.undo()
        self.assertFalse(g.undo())

    def test_undo_with_nothing_to_undo(self):
        self.assertFalse(Game().undo())

    def test_unchanged_move_does_not_overwrite_undo(self):
        g = game_with([[2, 4, 0, 0]] + [[0] * 4 for _ in range(3)])
        g.undo_state = "sentinel"
        g.move("a")  # changes nothing
        self.assertEqual(g.undo_state, "sentinel")

    def test_best_score_tracks_run(self):
        g = game_with([[2, 2, 0, 0]] + [[0] * 4 for _ in range(3)])
        g.move("a")
        self.assertEqual(g.best_score, 4)
        g.undo()
        self.assertEqual(g.best_score, 4)  # undo doesn't lower best


class TestFeedback(unittest.TestCase):
    def test_merge_message(self):
        g = game_with([[2, 2, 0, 0]] + [[0] * 4 for _ in range(3)])
        g.move("a")
        self.assertIn("1 merge", g.message)
        self.assertIn("+4", g.message)

    def test_plain_move_message(self):
        g = game_with([[0, 0, 0, 2]] + [[0] * 4 for _ in range(3)])
        g.move("a")
        self.assertEqual(g.message, "Moved left.")

    def test_unchanged_move_does_not_claim_move(self):
        g = game_with([[2, 4, 0, 0]] + [[0] * 4 for _ in range(3)])
        g.move("a")
        self.assertNotIn("Moved", g.message)


class TestInput(unittest.TestCase):
    def test_invalid_and_quit(self):
        out = play(["", "wa", "x", "q"])
        self.assertEqual(out.count("Invalid command"), 3)

    def test_undo_nothing(self):
        self.assertIn("Nothing to undo", play(["u", "q"]))


if __name__ == "__main__":
    unittest.main()