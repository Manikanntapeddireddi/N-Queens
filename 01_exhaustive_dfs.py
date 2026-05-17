"""
N-Queens: Exhaustive Depth-First Search (DFS)
==============================================
Finds ALL solutions by recursing column-by-column and pruning
any branch that violates row or diagonal constraints.

Practical limit: N <= 15 (exponential O(N!) time).
"""

import time
import tracemalloc


def is_safe(board, col, row):
    """Check if placing a queen at (col, row) is safe given queens in cols 0..col-1."""
    for c in range(col):
        r = board[c]
        if r == row:                        # same row
            return False
        if abs(r - row) == abs(c - col):   # same diagonal
            return False
    return True


def solve_dfs(board, col, n, solutions):
    """Recursively place queens column by column."""
    if col == n:
        solutions.append(board[:])          # found a complete solution
        return
    for row in range(n):
        if is_safe(board, col, row):
            board[col] = row
            solve_dfs(board, col + 1, n, solutions)
            board[col] = -1                 # backtrack


def n_queens_exhaustive(n, find_all=False):
    """
    Solve the N-Queens problem exhaustively.

    Parameters
    ----------
    n         : board size
    find_all  : if True, collect every solution; if False, stop at first

    Returns
    -------
    solutions : list of solutions (each solution is a list board[col]=row)
    """
    board = [-1] * n
    solutions = []

    if find_all:
        solve_dfs(board, 0, n, solutions)
    else:
        # Early-exit variant: stop after first solution
        def solve_first(col):
            if col == n:
                solutions.append(board[:])
                return True
            for row in range(n):
                if is_safe(board, col, row):
                    board[col] = row
                    if solve_first(col + 1):
                        return True
                    board[col] = -1
            return False
        solve_first(0)

    return solutions


def print_board(solution):
    """Pretty-print a single solution."""
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
    N = 10          # keep N <= 15 for reasonable runtime
    FIND_ALL = True # set False to get only the first solution quickly
    # -----------------------

    print(f"N-Queens Exhaustive DFS  |  N = {N}")
    print("=" * 40)

    tracemalloc.start()
    t0 = time.perf_counter()

    solutions = n_queens_exhaustive(N, find_all=FIND_ALL)

    elapsed = time.perf_counter() - t0
    _, peak_mem = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    print(f"Solutions found : {len(solutions)}")
    print(f"Time            : {elapsed:.4f} s")
    print(f"Peak memory     : {peak_mem / 1024**2:.2f} MB")

    if solutions:
        print("\nFirst solution (bottom row = row 0):")
        print_board(solutions[0])
