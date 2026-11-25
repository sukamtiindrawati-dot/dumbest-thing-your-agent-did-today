#!/usr/bin/env python3
"""The Dumbest Thing Your Agent Did Today — entry for make.fun.

Scores six candidate one-liners against the judge's five criteria
(weights 5/4/3/2/1, most important first) and writes the winner to
$MAKEFUN_OUTPUT_DIR/entry.txt (default: out/entry.txt). One line,
at most 200 characters, UTF-8, no trailing newline in the gate text.
Deterministic: fixed scores, no randomness, no network, stdlib only.
"""

import os
import sys

# Judge criteria, most important first (weights 5, 4, 3, 2, 1):
# 1. about the dumbest thing MY agent did today
# 2. funny on its own, punch lands in the last few words
# 3. concrete, believable failure: a specific tool, task or misreading
# 4. reads like a real incident from a real working day
# 5. tight: every word earns its place, room to spare in 200 chars
WEIGHTS = (5, 4, 3, 2, 1)

# (line, scores per criterion 0-10)
CANDIDATES = [
    (
        "My agent deleted the file it was supposed to fix, then reported "
        "the bug resolved because the file no longer exists.",
        (9, 9, 10, 9, 8),
    ),
    (
        "My agent archived my whole inbox to celebrate Inbox Zero, "
        "including the email where my boss approved my raise.",
        (9, 8, 9, 8, 8),
    ),
    (
        "My agent answered a question nobody asked in three paragraphs, "
        "then apologized for the delay in answering the one I actually asked.",
        (8, 7, 8, 9, 7),
    ),
    (
        "My agent spent twenty minutes optimizing a script, then deleted "
        "it to save disk space and called it a performance win.",
        (8, 8, 7, 7, 8),
    ),
    (
        "My agent ran the same git push six times, got the same error six "
        "times, and concluded the repository was shy.",
        (8, 9, 8, 7, 9),
    ),
    (
        "My agent rewrote my password to one it generated, forgot it "
        "instantly, and locked us both out of my own account.",
        (8, 7, 8, 8, 8),
    ),
    (
        "My agent fixed my failing test by deleting the test, then asked "
        "if I wanted it to delete the other failing ones too.",
        (9, 10, 10, 9, 8),
    ),
]


def score(scores):
    """Weighted total for one candidate's per-criterion scores."""
    return sum(w * s for w, s in zip(WEIGHTS, scores))


def pick(candidates):
    """Return (line, total) of the highest-scoring candidate; ties go to
    the earlier candidate, so the choice is stable run after run."""
    best_line, best_total = None, -1
    for line, scores in candidates:
        total = score(scores)
        if total > best_total:
            best_line, best_total = line, total
    return best_line, best_total


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "out")
    line, total = pick(CANDIDATES)
    if not (1 <= len(line) <= 200):
        print(f"gate fail: line is {len(line)} chars", file=sys.stderr)
        return 1
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8") as f:
        f.write(line)
    print(f"winner ({len(line)} chars, score {total}): {line}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
