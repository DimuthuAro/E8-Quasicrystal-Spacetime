"""
Hopf Fibration
==============
Implements the quaternionic Hopf fibration S⁷ → S⁴ with fibre S³.

The Hopf map uses quaternion pairs: for (q₁, q₂) ∈ ℍ² with |q₁|²+|q₂|²=1,
the map is h(q₁,q₂) = (|q₁|²−|q₂|², 2q₁q₂*) ∈ ℝ×ℍ ≅ ℝ⁵ → S⁴.

Fibres are orbits of right multiplication by unit quaternions.
"""

import numpy as np
from scipy.spatial.distance import cdist


def _to_quaternion_pair(v: np.ndarray) -> tuple:
    """Convert 8D vector to pair of quaternions (q1, q2).
    q1 = v[0] + v[1]i + v[2]j + v[3]k
    q2 = v[4] + v[5]i + v[6]j + v[7]k
    """
    return v[:4].copy(), v[4:].copy()


def _quat_conjugate(q: np.ndarray) -> np.ndarray:
    """Quaternion conjugate: (a, -b, -c, -d)."""
    return np.array([q[0], -q[1], -q[2], -q[3]])


def _quat_multiply(p: np.ndarray, q: np.ndarray) -> np.ndarray:
    """Hamilton product of two quaternions."""
    a1, b1, c1, d1 = p
    a2, b2, c2, d2 = q
    return np.array([
        a1*a2 - b1*b2 - c1*c2 - d1*d2,
        a1*b2 + b1*a2 + c1*d2 - d1*c2,
        a1*c2 - b1*d2 + c1*a2 + d1*b2,
        a1*d2 + b1*c2 - c1*b2 + d1*a2,
    ])


def hopf_map(points_s7: np.ndarray) -> tuple:
    """Apply quaternionic Hopf fibration S⁷ → S⁴.
    
    Args:
        points_s7: (N, 8) array of unit vectors on S⁷
    Returns:
        (base_coords, fibre_data) where:
            base_coords: (N, 5) points on S⁴
            fibre_data: (N, 4) fibre coordinates
    """
    N = len(points_s7)
    base_coords = np.zeros((N, 5))
    fibre_coords = np.zeros((N, 4))

    for i in range(N):
        q1, q2 = _to_quaternion_pair(points_s7[i])
        norm_q1_sq = np.sum(q1 ** 2)
        norm_q2_sq = np.sum(q2 ** 2)
        
        # Base point on S⁴: (|q1|²-|q2|², 2*q1*conj(q2))
        q2_conj = _quat_conjugate(q2)
        product = _quat_multiply(q1, q2_conj)
        
        base_coords[i, 0] = norm_q1_sq - norm_q2_sq
        base_coords[i, 1:] = 2.0 * product
        
        # Fibre coordinate: phase of q1 (or q2)
        if np.linalg.norm(q1) > 1e-10:
            fibre_coords[i] = q1 / np.linalg.norm(q1)
        else:
            fibre_coords[i] = q2 / max(np.linalg.norm(q2), 1e-15)

    return base_coords, fibre_coords


def group_into_fibres(base_coords: np.ndarray, tolerance: float = 0.15) -> list:
    """Cluster points into Hopf fibres based on base-space proximity.
    Points mapping to the same base point belong to the same fibre.
    
    Returns list of arrays, each containing indices of points in one fibre.
    """
    N = len(base_coords)
    visited = np.zeros(N, dtype=bool)
    fibres = []
    
    for i in range(N):
        if visited[i]:
            continue
        # Find all points close to this base point
        dists = np.linalg.norm(base_coords - base_coords[i], axis=1)
        fibre_mask = dists < tolerance
        fibre_indices = np.where(fibre_mask)[0]
        visited[fibre_mask] = True
        fibres.append(fibre_indices)
    
    return fibres


def compute_fibre_statistics(fibres: list) -> dict:
    """Statistics about the fibre decomposition."""
    sizes = [len(f) for f in fibres]
    return {
        'num_fibres': len(fibres),
        'fibre_sizes': sizes,
        'mean_size': float(np.mean(sizes)),
        'min_size': min(sizes),
        'max_size': max(sizes),
        'total_points': sum(sizes),
    }
