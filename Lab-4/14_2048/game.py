from board import Board


class Game:
    def __init__(self):
        self.board = Board()
        self.best_score = 0
        self.message = ""
        self.undo_state = None  # state before the last successful move

    def display(self):
        print("\n" + "+------+------+------+------+")
        for row in self.board.grid:
            print("|" + "|".join(f"{x:^6}" if x else f"{' ':^6}" for x in row) + "|")
            print("+------+------+------+------+")
        print("Score:", self.board.score, " Best:", self.best_score)

    def move(self, key):
        """Apply a move. A tile is spawned only if the board actually changed."""
        moves = {"a": self.board.move_left, "d": self.board.move_right,
                 "w": self.board.move_up, "s": self.board.move_down}
        if key not in moves:
            self.message = "Invalid command."
            return False
        before = self.board.snapshot()
        self.board.last_merges = self.board.last_gain = 0
        changed = moves[key]()
        if changed:
            self.undo_state = before
            self.board.add_random_tile()
            self.best_score = max(self.best_score, self.board.score)
            self.message = self._move_message(key)
        else:
            self.message = "Nothing moved - try another direction."
        return changed

    def _move_message(self, key):
        name = {"a": "left", "d": "right", "w": "up", "s": "down"}[key]
        merges, gain = self.board.last_merges, self.board.last_gain
        if merges:
            return f"Moved {name}. {merges} merge{'s' if merges != 1 else ''}, +{gain} points."
        return f"Moved {name}."

    def undo(self):
        """Restore board and score from before the last move. No tile is spawned."""
        if self.undo_state is None:
            return False
        self.board.restore(self.undo_state)
        self.undo_state = None  # only one level
        self.message = "Undid last move."
        return True

    def run(self):
        print("2048 — W/A/S/D to move, U to undo, Q to quit.")
        while True:
            self.display()
            if self.board.has_won():
                print("You reached 2048! You win!")
                return
            if not self.board.can_move():
                print("No legal moves remain. Game over.")
                return
            key = input("> ").strip().lower()
            if key == "q":
                return
            if key == "u":
                if not self.undo():
                    self.message = "Nothing to undo."
                print(self.message)
                continue
            if key not in ("w", "a", "s", "d"):
                print("Invalid command. Use W/A/S/D, U to undo, Q to quit.")
                continue
            self.move(key)
            print(self.message)