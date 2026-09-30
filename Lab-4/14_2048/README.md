# Scenario 14 — 2048

A terminal 2048 implementation with directional movement and tile merging.

## Provided files

- `main.py` — entry point.
- `game.py` — game loop, commands, and game state.
- `board.py` — grid movement and tile logic.
- `requirements.txt` — dependency declaration.

## Setup

```bash
python main.py
```

No package installation is required.

## Before changing the code

Run the starter and deliberately construct repeated-tile rows if possible. Read the
board movement code and trace one complete move from input to tile creation.

## Task 1 — Correct merge semantics

Fix the merge algorithm so an original tile can participate in at most one merge
during a single move. Preserve normal compression and movement behaviour.

**Done when:** repeated patterns such as four equal tiles produce the standard 2048
result, not a chain merge of a newly created tile in the same move.

## Task 2 — Finish game-state handling

Implement win detection, no-move detection, and correct tile creation semantics.
A move that leaves the board unchanged must not create a new tile.

**Done when:** reaching 2048 ends the game, a full board with no legal moves ends the
game, and unchanged moves do not alter the board.

## Task 3 — Undo and best score

Add a one-level undo. Restoring a move must restore both board contents and score.
Track the best score for the current run.

**Done when:** one undo reverses exactly one successful move and does not create a tile.

## Task 4 — Move feedback

Add concise feedback for successful moves and merges. Do not trigger feedback merely
because internal board-scanning functions were called.

**Done when:** one accepted move produces one action-level result and invalid/unchanged
moves do not claim that a move occurred.

## Required testing

Test ordinary slides, four-equal patterns, separated equal pairs, unchanged moves,
2048 detection, no-move boards, undo, score restoration, invalid commands, and quitting.


## LLM usage

You may use an LLM during the lab. The goal is to use it as a coding assistant while
retaining responsibility for understanding and testing the result.

- Inspect the existing code before asking for changes.
- Ask for explanations when you do not understand a proposed change.
- Test generated code against the stated behaviour and edge cases.
- Keep your complete LLM chat history for submission.
- Do not replace the whole project with an unrelated implementation.
- Keep all state in memory; do not add CSV, JSON, SQLite, or other persistence.

## Submission checklist

- [ ] Task 1 completed and the original defect was reproduced and fixed.
- [ ] Tasks 2–4 completed and tested.
- [ ] Boundary and invalid-input cases tested.
- [ ] No unnecessary external dependencies added.
- [ ] No persistent storage added.
- [ ] Code remains understandable and modular.
- [ ] Complete LLM chat-history link included.

## Folder structure

```text
scenario-02-2048/
├── README.md
├── requirements.txt
├── main.py
├── game.py
└── board.py
```

## Submission Checklist

Submission is only the following three things:

- [ ] A 10-second video of gameplay **before** your changes, showing the bug/broken behavior
- [ ] A 10-second video of gameplay **after** your changes, showing the bug fixed and the new features working
- [ ] The Chat/LLM used page link, with the complete chat history
