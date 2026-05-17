"""
N-Queens: Genetic Algorithm (GA)
==================================
Each chromosome is a permutation of {0, …, N-1}, so row and column
conflicts are zero by construction.  Only diagonal conflicts are minimised.

Pipeline (matches Algorithm 1 in the paper):
  - Tournament selection (k = 5)
  - Order Crossover (OX)
  - Swap mutation (p_m = 0.05)
  - 5 % elitism
  - Termination: zero conflicts OR 5,000 generations

Complexity: O(P · N · G)   P = population, G = generations
Best scalability among the four algorithms.
"""

import random
import time
import tracemalloc
from copy import deepcopy


# ── Fitness ───────────────────────────────────────────────────────────────────

def diagonal_conflicts(board):
    """Count diagonal attacking pairs (lower = better; 0 = solution)."""
    n = len(board)
    conflicts = 0
    for i in range(n):
        for j in range(i + 1, n):
            if abs(board[i] - board[j]) == abs(i - j):
                conflicts += 1
    return conflicts


# ── Genetic operators ─────────────────────────────────────────────────────────

def tournament_select(population, fitness, k=5):
    """Pick the best individual from k randomly chosen candidates."""
    contenders = random.sample(range(len(population)), k)
    best = min(contenders, key=lambda i: fitness[i])
    return population[best][:]


def order_crossover(parent1, parent2):
    """
    Order Crossover (OX):
    Copy a random slice from parent1; fill remaining positions
    in the order they appear in parent2.
    """
    n = len(parent1)
    a, b = sorted(random.sample(range(n), 2))
    child = [-1] * n
    child[a:b+1] = parent1[a:b+1]
    fill = [x for x in parent2 if x not in child[a:b+1]]
    pos = 0
    for i in range(n):
        if child[i] == -1:
            child[i] = fill[pos]
            pos += 1
    return child


def swap_mutate(board, p_m=0.05):
    """Swap two random positions with probability p_m."""
    if random.random() < p_m:
        i, j = random.sample(range(len(board)), 2)
        board[i], board[j] = board[j], board[i]
    return board


# ── Main GA ───────────────────────────────────────────────────────────────────

def n_queens_ga(n,
                pop_size=200,
                max_gen=5000,
                p_m=0.05,
                tournament_k=5,
                elite_frac=0.05):
    """
    Solve N-Queens with a Genetic Algorithm.

    Parameters
    ----------
    n            : board size
    pop_size     : population size (paper uses 200)
    max_gen      : maximum generations (paper uses 5000)
    p_m          : mutation probability (paper uses 0.05)
    tournament_k : tournament size    (paper uses 5)
    elite_frac   : fraction of elites to carry over (paper uses 0.05)

    Returns
    -------
    (best_board, best_conflicts, generation_found)
    """
    n_elites = max(1, int(pop_size * elite_frac))

    # Initialise population: random permutations
    population = [random.sample(range(n), n) for _ in range(pop_size)]

    best_board = None
    best_cost = float("inf")

    for gen in range(max_gen):
        # Evaluate fitness
        fitness = [diagonal_conflicts(ind) for ind in population]

        # Track best
        gen_best_idx = min(range(pop_size), key=lambda i: fitness[i])
        if fitness[gen_best_idx] < best_cost:
            best_cost = fitness[gen_best_idx]
            best_board = population[gen_best_idx][:]

        # Early termination
        if best_cost == 0:
            return best_board, 0, gen

        # Sort by fitness for elitism
        sorted_pop = [x for _, x in
                      sorted(zip(fitness, population), key=lambda p: p[0])]

        # Elites carry straight through
        new_population = [ind[:] for ind in sorted_pop[:n_elites]]

        # Fill the rest with children
        while len(new_population) < pop_size:
            p1 = tournament_select(population, fitness, tournament_k)
            p2 = tournament_select(population, fitness, tournament_k)
            child = order_crossover(p1, p2)
            child = swap_mutate(child, p_m)
            new_population.append(child)

        population = new_population

    return best_board, best_cost, max_gen


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
    N        = 50
    POP_SIZE = 200
    MAX_GEN  = 5000
    # -----------------------

    print(f"N-Queens Genetic Algorithm  |  N = {N}")
    print("=" * 45)

    tracemalloc.start()
    t0 = time.perf_counter()

    solution, conflicts, gen = n_queens_ga(N, pop_size=POP_SIZE, max_gen=MAX_GEN)

    elapsed = time.perf_counter() - t0
    _, peak_mem = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    status = "✓ SOLVED" if conflicts == 0 else f"✗ {conflicts} conflicts remaining"
    print(f"Result              : {status}")
    print(f"Generation          : {gen:,}")
    print(f"Time                : {elapsed:.4f} s")
    print(f"Peak memory         : {peak_mem / 1024**2:.2f} MB")

    if N <= 20:
        print("\nSolution board (bottom row = row 0):")
        print_board(solution)
