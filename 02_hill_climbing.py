"""
N-Queens: Greedy Hill-Climbing
==============================
Queens are placed one per column (random initial placement).
At each step the queen with the most conflicts is moved within
its column to the least-conflicting row.
Random restarts escape stagnation.

Complexity per restart: O(N^2)
Works well up to N = 500+
"""

import random
import time
import tracemalloc


def count_conflicts(board, col, row, n):
    """Count how many other queens attack the queen at (col, row)."""
    conflicts = 0
    for c in range(n):
        if c == col:
            continue
        r = board[c]
        if r == row or abs(r - row) == abs(c - col):
            conflicts += 1
    return conflicts


def all_conflicts(board, n):
    """Return a list of conflict counts for every queen."""
    return [count_conflicts(board, col, board[col], n) for col in range(n)]


def total_conflicts(board, n):
    """Total number of attacking pairs (each pair counted once per queen)."""
    return sum(all_conflicts(board, n)) // 2


def hill_climb_once(n, max_steps=None):
    """
    One hill-climbing attempt starting from a random board.

    Returns (board, steps) if a solution is found, else (None, steps).
    """
    if max_steps is None:
        max_steps = n * n * 10

    board = list(range(n))
    random.shuffle(board)

    for step in range(max_steps):
        conflicts = all_conflicts(board, n)

        # Check if solved
        if max(conflicts) == 0:
            return board, step

        # Pick the most conflicted queen (random tie-break)
        max_c = max(conflicts)
        candidates = [col for col, c in enumerate(conflicts) if c == max_c]
        col = random.choice(candidates)

        # Move it to the row with fewest conflicts
        best_row = board[col]
        best_val = conflicts[col]
        for row in range(n):
            if row == board[col]:
                continue
            val = count_conflicts(board, col, row, n)
            if val < best_val:
                best_val = val
                best_row = row

        board[col] = best_row

    return None, max_steps


def n_queens_hill_climbing(n, max_restarts=1000):
    """
    Solve N-Queens with greedy hill-climbing + random restarts.

    Returns (solution, restarts, total_steps) or (None, max_restarts, ...).
    """
    total_steps = 0
    for restart in range(max_restarts):
        solution, steps = hill_climb_once(n)
        total_steps += steps
        if solution is not None:
            return solution, restart + 1, total_steps
    return None, max_restarts, total_steps


def print_board(solution):
    n = len(solution)
    for row in range(n - 1, -1, -1):
        line = ""
        for col in range(n):
            line += "Q " if solution[col] == row else ". "
        print(line)
    print()


# ── Main ──────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    # ---- Change N here ----
    N = 50
    MAX_RESTARTS = 1000
    # -----------------------

    print(f"N-Queens Greedy Hill-Climbing  |  N = {N}")
    print("=" * 45)

    tracemalloc.start()
    t0 = time.perf_counter()

    solution, restarts, steps = n_queens_hill_climbing(N, MAX_RESTARTS)

    elapsed = time.perf_counter() - t0
    _, peak_mem = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    if solution:
        print(f"Solution found after {restarts} restart(s), {steps} total steps")
        conflicts_left = total_conflicts(solution, N)
        print(f"Conflicts remaining : {conflicts_left}")
    else:
        print("No solution found within restart limit.")

    print(f"Time                : {elapsed:.4f} s")
    print(f"Peak memory         : {peak_mem / 1024**2:.2f} MB")

    if solution and N <= 20:
        print("\nSolution board (bottom row = row 0):")
        print_board(solution)
