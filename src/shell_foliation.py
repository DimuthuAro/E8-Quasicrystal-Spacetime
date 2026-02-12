"""
Shell Foliator
==============
Organizes E₈ lattice points into concentric shells by norm².
Each shell corresponds to a representation of E₈ at a given level.
"""

import numpy as np
from collections import defaultdict


def compute_shell_structure(points: np.ndarray, max_shells: int = 10) -> list:
    """Group lattice points into shells by norm²."""
    norms_sq = np.round(np.sum(points ** 2, axis=1), 10)
    unique_norms = np.unique(norms_sq)
    unique_norms = unique_norms[unique_norms > 0]  # exclude origin
    unique_norms.sort()

    shells = []
    for idx, nsq in enumerate(unique_norms[:max_shells]):
        mask = np.abs(norms_sq - nsq) < 1e-8
        shell_points = points[mask]
        shells.append({
            'norm_squared': float(nsq),
            'points': shell_points,
            'point_count': len(shell_points),
            'shell_index': idx + 1,
        })
    return shells


def shell_point_counts(shells: list) -> np.ndarray:
    """Return array of point counts per shell."""
    return np.array([s['point_count'] for s in shells])


def compute_theta_series_coefficients(shells: list) -> dict:
    """Compute theta series Θ_{E₈}(q) = 1 + Σ aₙ q^n.
    The E₈ theta series is 1 + 240q + 2160q² + 6720q³ + ..."""
    coeffs = {0: 1}
    for s in shells:
        n = int(round(s['norm_squared'] / 2))  # norm²/2 gives the q-exponent
        coeffs[n] = s['point_count']
    return coeffs


def expected_theta_series() -> dict:
    """Known theta series coefficients for E₈ (first few terms).
    Θ_{E₈}(q) = 1 + 240q + 2160q² + 6720q³ + 17520q⁴ + 30240q⁵ + ..."""
    return {
        0: 1,
        1: 240,
        2: 2160,
        3: 6720,
        4: 17520,
        5: 30240,
        6: 60480,
        7: 82560,
        8: 140400,
    }
