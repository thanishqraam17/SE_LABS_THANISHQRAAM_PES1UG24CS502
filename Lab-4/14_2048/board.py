import random

SIZE = 4
WIN_TILE = 2048


class Board:
    def __init__(self):
        self.grid = [[0] * SIZE for _ in range(SIZE)]
        self.score = 0
        self.add_random_tile()
        self.add_random_tile()

    def add_random_tile(self):
        empty = [(r, c) for r in range(SIZE) for c in range(SIZE) if self.grid[r][c] == 0]
        if empty:
            r, c = random.choice(empty)
            self.grid[r][c] = 4 if random.random() < 0.1 else 2

    @staticmethod
    def slide_line(line):
        """Slide a line toward index 0. Each original tile merges at most once.

        Returns (new_line, points_gained, merge_count).
        """
        values = [x for x in line if x]
        result = []
        gained = 0
        merges = 0
        i = 0
        while i < len(values):
            if i + 1 < len(values) and values[i] == values[i + 1]:
                merged = values[i] * 2
                result.append(merged)
                gained += merged
                merges += 1
                i += 2  # skip both source tiles so the new tile can't merge again
            else:
                result.append(values[i])
                i += 1
        return result + [0] * (SIZE - len(result)), gained, merges

    def _slide(self, line):
        """Slide one line, add merge points to the score, return the new line."""
        new, gained, _merges = self.slide_line(line)
        self.score += gained
        return new

    def move_left(self):
        changed = False
        for r in range(SIZE):
            old = self.grid[r][:]
            self.grid[r] = self._slide(old)
            changed |= old != self.grid[r]
        return changed

    def move_right(self):
        changed = False
        for r in range(SIZE):
            old = self.grid[r][:]
            self.grid[r] = list(reversed(self._slide(list(reversed(old)))))
            changed |= old != self.grid[r]
        return changed

    def move_up(self):
        changed = False
        for c in range(SIZE):
            old = [self.grid[r][c] for r in range(SIZE)]
            new = self._slide(old)
            for r in range(SIZE):
                self.grid[r][c] = new[r]
            changed |= old != new
        return changed

    def move_down(self):
        changed = False
        for c in range(SIZE):
            old = [self.grid[r][c] for r in range(SIZE)]
            new = list(reversed(self._slide(list(reversed(old)))))
            for r in range(SIZE):
                self.grid[r][c] = new[r]
            changed |= old != new
        return changed

    def snapshot(self):
        """Copy of the current state (grid + score) for one-level undo."""
        return [row[:] for row in self.grid], self.score

    def restore(self, snap):
        grid, score = snap
        self.grid = [row[:] for row in grid]
        self.score = score

    def has_won(self):
        return any(tile >= WIN_TILE for row in self.grid for tile in row)

    def can_move(self):
        if any(0 in row for row in self.grid):
            return True
        for r in range(SIZE):
            for c in range(SIZE):
                if c + 1 < SIZE and self.grid[r][c] == self.grid[r][c + 1]:
                    return True
                if r + 1 < SIZE and self.grid[r][c] == self.grid[r + 1][c]:
                    return True
        return False