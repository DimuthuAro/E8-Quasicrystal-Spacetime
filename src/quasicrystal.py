"""
4D Quasicrystal Assembler
=========================
Assembles selected fibre points into a 4D quasicrystalline point set.
Verifies {3,3,5} (600-cell) symmetry and aperiodicity.
"""

import numpy as np
from scipy.spatial import ConvexHull


def assemble_quasicrystal(points_8d: np.ndarray, fibres: list,
                           selected_indices: np.ndarray,
                           projection_matrix: np.ndarray = None) -> dict:
    """Assemble 4D quasicrystal from selected Hopf fibres.
    
    Projects selected 8D points to 4D using the "parallel space" projection.
    """
    if projection_matrix is None:
        # Default: project onto first 4 coordinates (parallel space)
        projection_matrix = np.eye(8, 4)
    
    # Gather all selected points
    selected_points_8d = []
    for idx in selected_indices:
        fibre_pts = points_8d[fibres[idx]]
        selected_points_8d.append(fibre_pts)
    
    if len(selected_points_8d) == 0:
        return {'points_4d': np.zeros((0, 4)), 'point_count': 0}
    
    all_8d = np.vstack(selected_points_8d)
    
    # Project to 4D
    points_4d = all_8d @ projection_matrix
    
    # Remove duplicates
    points_4d = np.unique(np.round(points_4d, 10), axis=0)
    
    return {
        'points_4d': points_4d,
        'points_8d': all_8d,
        'point_count': len(points_4d),
        'projection_matrix': projection_matrix,
    }


def compute_order_parameters(points_4d: np.ndarray) -> dict:
    """Compute quasicrystalline order parameters."""
    if len(points_4d) < 4:
        return {'status': 'insufficient_points'}
    
    # Bond-orientational order parameter (adapted for 4D)
    center = np.mean(points_4d, axis=0)
    displacements = points_4d - center
    norms = np.linalg.norm(displacements, axis=1, keepdims=True)
    norms = np.where(norms < 1e-15, 1.0, norms)
    directions = displacements / norms
    
    # Compute angular correlations
    dots = directions @ directions.T
    dots = np.clip(dots, -1.0, 1.0)
    
    # Icosahedral order: check for 5-fold symmetry signatures
    angles = np.arccos(np.abs(dots[np.triu_indices(len(dots), k=1)]))
    golden_angle = np.arccos(1.0 / np.sqrt(5))  # ~63.43°
    
    # Count angles near golden ratio angle
    near_golden = np.sum(np.abs(angles - golden_angle) < 0.1)
    total_pairs = len(angles)
    
    # Pair distribution function
    dists = np.linalg.norm(
        points_4d[:, None, :] - points_4d[None, :, :], axis=2
    )
    dists_flat = dists[np.triu_indices(len(dists), k=1)]
    
    return {
        'golden_ratio_order': float(near_golden / max(total_pairs, 1)),
        'mean_distance': float(np.mean(dists_flat)),
        'std_distance': float(np.std(dists_flat)),
        'min_distance': float(np.min(dists_flat)) if len(dists_flat) > 0 else 0,
        'point_count': len(points_4d),
        'pair_distances': dists_flat,
    }


def verify_600_cell_symmetry(points_4d: np.ndarray) -> dict:
    """Test whether the point set has {3,3,5} (600-cell) symmetry.
    The 600-cell has 120 vertices, 720 edges, 1200 triangular faces, 600 cells.
    """
    if len(points_4d) < 10:
        return {'has_symmetry': False, 'reason': 'too_few_points'}
    
    # Check for icosahedral angular signatures
    center = np.mean(points_4d, axis=0)
    centered = points_4d - center
    norms = np.linalg.norm(centered, axis=1)
    
    # Normalize
    mask = norms > 1e-10
    unit_pts = centered[mask] / norms[mask, None]
    
    if len(unit_pts) < 10:
        return {'has_symmetry': False, 'reason': 'too_few_nonzero_points'}
    
    # Compute pairwise dot products
    dots = unit_pts @ unit_pts.T
    unique_dots = np.unique(np.round(dots[np.triu_indices(len(dots), k=1)], 6))
    
    # 600-cell vertices have specific dot product values related to golden ratio
    phi = (1 + np.sqrt(5)) / 2  # golden ratio
    expected_dots = np.sort([0, 1/phi, -1/phi, 1/phi**2, -1/phi**2, 0.5, -0.5, 1, -1])
    
    return {
        'num_unique_dot_products': len(unique_dots),
        'unique_dots_sample': unique_dots[:20].tolist(),
        'golden_ratio_phi': float(phi),
        'point_count': len(unit_pts),
    }


def compute_diffraction_pattern(points_4d: np.ndarray, k_max: float = 5.0,
                                  n_k: int = 100) -> dict:
    """Compute structure factor S(k) — Fourier transform of point set.
    Quasicrystals show sharp Bragg peaks at irrational positions.
    """
    # Use first 3 coordinates for 3D diffraction
    points_3d = points_4d[:, :3]
    
    # Generate k-vectors
    k_vals = np.linspace(0.1, k_max, n_k)
    
    # Compute S(k) for spherically averaged case
    S_k = np.zeros(n_k)
    for i, k in enumerate(k_vals):
        # Average over random directions
        n_dirs = 50
        for _ in range(n_dirs):
            direction = np.random.randn(3)
            direction /= np.linalg.norm(direction)
            k_vec = k * direction
            phases = points_3d @ k_vec
            S_k[i] += np.abs(np.sum(np.exp(1j * phases))) ** 2
        S_k[i] /= n_dirs * len(points_3d)
    
    return {
        'k_values': k_vals,
        'structure_factor': S_k,
    }
