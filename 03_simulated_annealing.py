"""
N-Queens: Simulated Annealing (SA)
===================================
Starts from a random permutation and iteratively swaps two queens.
A worsening move is accepted with probability exp(-ΔE / T).
Temperature cools as T ← 0.995·T from T₀ = 1.0.

Complexity: O(N² × T_steps)
Reliable for N up to 500+
"""

import random
import math
import time
import tracemalloc


def diagonal_conflicts(board):
    """Count the total number of diagonal attacking pairs."""
    n = len(board)
    conflicts = 0
    for i in range(n):
        for j in range(i + 1, n):
            if abs(board[i] - board[j]) == abs(i - j):
                conflicts += 1
    return conflicts


def n_queens_sa(n,
                T0=1.0,
                cooling=0.995,
                min_temp=1e-4,
                steps_per_temp=None,
                max_steps=None):
    """
    Solve N-Queens with Simulated Annealing.

    The board is encoded as a permutation (board[col] = row), so row and
    column conflicts are eliminated by construction; only diagonal conflicts
    are minimised.

    Parameters
    ----------
    n              : board size
    T0             : initial temperature
    cooling        : multiplicative cooling factor (< 1)
    min_temp       : stop cooling when T drops below this value
    steps_per_temp : SA iterations per temperature level (default: N)
    max_steps      : hard cap on total iterations (default: 10·N²)

    Returns
    -------
    (board, conflicts, total_steps)
    """
    if steps_per_temp is None:
        steps_per_temp = max(n, 100)
    if max_steps is None:
        max_steps = 10 * n * n

    # Random permutation: one queen per row AND per column
    board = list(range(n))
    random.shuffle(board)

    current_cost = diagonal_conflicts(board)
    best_board = board[:]
    best_cost = current_cost

    T = T0
    total_steps = 0

    while T > min_temp and total_steps < max_steps:
        for _ in range(steps_per_temp):
            if current_cost == 0:
                return board, 0, total_steps

            # Random swap of two column positions
            i, j = random.sample(range(n), 2)
            board[i], board[j] = board[j], board[i]
            new_cost = diagonal_conflicts(board)

            delta = new_cost - current_cost
            if delta < 0 or random.random() < math.exp(-delta / T):
                current_cost = new_cost
                if current_cost < best_cost:
                    best_cost = current_cost
                    best_board = board[:]
            else:
                board[i], board[j] = board[j], board[i]  # undo

            total_steps += 1

        T *= cooling

    return best_board, best_cost, total_steps


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
    N = 100
    # -----------------------

    print(f"N-Queens Simulated Annealing  |  N = {N}")
    print("=" * 45)

    tracemalloc.start()
    t0 = time.perf_counter()

    solution, conflicts, steps = n_queens_sa(N)

    elapsed = time.perf_counter() - t0
    _, peak_mem = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    status = "✓ SOLVED" if conflicts == 0 else f"✗ {conflicts} conflicts remaining"
    print(f"Result              : {status}")
    print(f"Total SA steps      : {steps:,}")
    print(f"Time                : {elapsed:.4f} s")
    print(f"Peak memory         : {peak_mem / 1024**2:.2f} MB")

    if N <= 20:
        print("\nSolution board (bottom row = row 0):")
        print_board(solution)
