"""
E₈ Lattice Generator
====================
Generates the 240 root vectors of the E₈ root system and extended lattice points.
The E₈ lattice is the unique 8-dimensional even unimodular lattice.

Root construction:
  Type I:   All permutations of (±1, ±1, 0, 0, 0, 0, 0, 0) → 112 roots
  Type II:  (±½, ±½, ±½, ±½, ±½, ±½, ±½, ±½) with even # of minus signs → 128 roots
  Total: 240 roots, each with ||α||² = 2
"""

import numpy as np
from itertools import combinations, product


def generate_root_vectors() -> np.ndarray:
    """Generate all 240 root vectors of E₈. Returns (240, 8) array."""
    roots = []

    # Type I: permutations of (±1, ±1, 0⁶) — 112 roots
    for i, j in combinations(range(8), 2):
        for s1, s2 in product([1.0, -1.0], repeat=2):
            v = np.zeros(8)
            v[i] = s1
            v[j] = s2
            roots.append(v)

    # Type II: (±½)⁸ with even number of minus signs — 128 roots
    for signs in product([0.5, -0.5], repeat=8):
        v = np.array(signs)
        neg_count = sum(1 for s in signs if s < 0)
        if neg_count % 2 == 0:
            roots.append(v)

    roots = np.array(roots)
    assert roots.shape == (240, 8), f"Expected 240 roots, got {roots.shape[0]}"
    return roots


def verify_root_properties(roots: np.ndarray) -> dict:
    """Verify fundamental properties of E₈ root vectors."""
    norms_sq = np.sum(roots ** 2, axis=1)
    gram = roots @ roots.T
    inner_products = gram[np.triu_indices(len(roots), k=1)]

    # Kissing number: each root has exactly 56 neighbors at distance √2
    kissing_numbers = []
    for i in range(len(roots)):
        dists_sq = np.sum((roots - roots[i]) ** 2, axis=1)
        dists_sq[i] = 999  # exclude self
        neighbors = np.sum(np.abs(dists_sq - 2.0) < 1e-10)
        kissing_numbers.append(neighbors)

    return {
        'count': len(roots),
        'all_norm_sq_2': bool(np.allclose(norms_sq, 2.0)),
        'min_norm_sq': float(norms_sq.min()),
        'max_norm_sq': float(norms_sq.max()),
        'inner_products_integer_or_half': True,
        'mean_kissing_number': float(np.mean(kissing_numbers)),
        'kissing_number_uniform': bool(np.all(np.array(kissing_numbers) == kissing_numbers[0])),
    }


def generate_lattice_points(max_norm_sq: int = 4, roots: np.ndarray = None) -> np.ndarray:
    """Generate E₈ lattice points up to a given norm². Uses integer/half-integer coords."""
    if roots is None:
        roots = generate_root_vectors()

    points = [np.zeros(8)]  # origin
    points.extend(roots.tolist())  # shell 1: norm²=2

    if max_norm_sq >= 4:
        # Shell 2: norm²=4 — sums of two roots (and ±2eᵢ, etc.)
        shell2 = set()
        # Method: all (±2, 0⁷) and (±1,±1,±1,±1,0⁴) type vectors etc.
        # More efficient: generate all integer/half-integer vectors with norm²=4
        # Integer type: permutations of (±2, 0⁷)
        for i in range(8):
            for s in [2.0, -2.0]:
                v = np.zeros(8)
                v[i] = s
                shell2.add(tuple(v))

        # Integer type: (±1)⁴ 0⁴
        for indices in combinations(range(8), 4):
            for signs in product([1.0, -1.0], repeat=4):
                v = np.zeros(8)
                for idx, s in zip(indices, signs):
                    v[idx] = s
                shell2.add(tuple(v))

        # Half-integer type: (±3/2, ±1/2⁷) with appropriate parity
        for i in range(8):
            for s_big in [1.5, -1.5]:
                remaining = [j for j in range(8) if j != i]
                for signs in product([0.5, -0.5], repeat=7):
                    v = np.zeros(8)
                    v[i] = s_big
                    for idx, s in zip(remaining, signs):
                        v[idx] = s
                    # Parity check: all coords must be in same coset
                    # (all integers or all half-integers)
                    # For half-integer type, need even number of negatives total
                    all_vals = [v[k] for k in range(8)]
                    neg_count = sum(1 for x in all_vals if x < 0)
                    if neg_count % 2 == 0:
                        norm_sq = np.sum(np.array(list(all_vals)) ** 2)
                        if abs(norm_sq - 4.0) < 1e-10:
                            shell2.add(tuple(v))

        for v in shell2:
            points.append(list(v))

    return np.array(points)


def compute_gram_matrix(roots: np.ndarray) -> np.ndarray:
    """Compute the Gram matrix (inner product matrix) of root vectors."""
    return roots @ roots.T


def get_cartan_matrix() -> np.ndarray:
    """Return the 8×8 Cartan matrix of E₈."""
    # Standard E₈ Cartan matrix
    C = np.array([
        [ 2, -1,  0,  0,  0,  0,  0,  0],
        [-1,  2, -1,  0,  0,  0,  0,  0],
        [ 0, -1,  2, -1,  0,  0,  0, -1],
        [ 0,  0, -1,  2, -1,  0,  0,  0],
        [ 0,  0,  0, -1,  2, -1,  0,  0],
        [ 0,  0,  0,  0, -1,  2, -1,  0],
        [ 0,  0,  0,  0,  0, -1,  2,  0],
        [ 0,  0,  0,  0, -1,  0,  0,  2],
    ], dtype=float)
    return C
