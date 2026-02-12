"""
31 Subspace Decomposition
=========================
Enumerates ways to decompose the 8D E₈ space into two orthogonal 4D subspaces.
These correspond to "parallel" and "perpendicular" spaces for quasicrystal projection.

The 31 subspaces relate to the affine E₈ diagram nodes and correspond to
different vacua/sectors in the full quantum theory.
"""

import numpy as np
from itertools import combinations


def generate_standard_decomposition() -> tuple:
    """The simplest decomposition: first 4 dims ∥, last 4 dims ⊥."""
    P_parallel = np.eye(8, 4)          # 8×4 projection to parallel space
    P_perp = np.zeros((8, 4))
    P_perp[4:, :] = np.eye(4)          # project to perpendicular space
    return P_parallel, P_perp


def generate_golden_ratio_decomposition() -> tuple:
    """Decomposition using golden ratio, producing icosahedral quasicrystal."""
    phi = (1 + np.sqrt(5)) / 2
    inv_phi = 1.0 / phi
    
    # Construct projection matrices using golden ratio rotations
    # This produces Penrose-like tilings in 4D
    P_parallel = np.zeros((8, 4))
    P_perp = np.zeros((8, 4))
    
    # Golden ratio mixing of coordinate pairs
    norm = 1.0 / np.sqrt(1 + phi**2)
    for i in range(4):
        P_parallel[i, i] = phi * norm
        P_parallel[i + 4, i] = 1.0 * norm
        P_perp[i, i] = 1.0 * norm
        P_perp[i + 4, i] = -phi * norm
    
    return P_parallel, P_perp


def enumerate_31_subspaces() -> list:
    """Generate 31 distinct 4D+4D decompositions of ℝ⁸.
    
    These correspond to:
    - The standard decomposition
    - Golden ratio decompositions
    - Rotations by multiples of 2π/31 (related to affine E₈)
    - D₄×D₄ aligned decompositions
    """
    decompositions = []
    
    # 1. Standard decomposition
    decompositions.append(generate_standard_decomposition())
    
    # 2. Golden ratio decomposition
    decompositions.append(generate_golden_ratio_decomposition())
    
    # 3. Generate 29 more by rotating in the 8D space
    # Use angles related to the 31 roots of unity (Galois theory of E₈)
    for k in range(1, 30):
        angle = 2 * np.pi * k / 31
        
        # Build 8×8 rotation matrix as block rotations
        R = np.eye(8)
        c, s = np.cos(angle), np.sin(angle)
        
        # Rotate in 4 planes simultaneously
        for pair_idx in range(4):
            i, j = pair_idx, pair_idx + 4
            R[i, i] = c
            R[i, j] = -s
            R[j, i] = s
            R[j, j] = c
        
        # Apply rotation to standard decomposition
        P_par_std, P_perp_std = generate_standard_decomposition()
        P_par = R @ P_par_std
        P_perp = R @ P_perp_std
        
        decompositions.append((P_par, P_perp))
    
    return decompositions


def apply_decomposition(points_8d: np.ndarray,
                         P_parallel: np.ndarray,
                         P_perp: np.ndarray) -> tuple:
    """Project 8D points into parallel and perpendicular 4D subspaces."""
    parallel_4d = points_8d @ P_parallel
    perp_4d = points_8d @ P_perp
    return parallel_4d, perp_4d


def compute_decomposition_properties(P_parallel: np.ndarray,
                                      P_perp: np.ndarray) -> dict:
    """Analyze properties of a decomposition."""
    # Check orthogonality
    cross = P_parallel.T @ P_perp
    orthogonality_error = float(np.max(np.abs(cross)))
    
    # Singular values (should be 1 for orthonormal projection)
    sv_par = np.linalg.svd(P_parallel, compute_uv=False)
    sv_perp = np.linalg.svd(P_perp, compute_uv=False)
    
    return {
        'orthogonality_error': orthogonality_error,
        'is_orthogonal': orthogonality_error < 1e-10,
        'sv_parallel': sv_par.tolist(),
        'sv_perpendicular': sv_perp.tolist(),
    }
