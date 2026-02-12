"""
S⁷ Embedder
============
Embeds E₈ shell points onto the 7-sphere S⁷ ⊂ ℝ⁸.
Each shell of radius r maps to S⁷ by normalization x → x/||x||.
"""

import numpy as np


def embed_shell_in_s7(points: np.ndarray) -> np.ndarray:
    """Normalize 8D points to lie on S⁷ (unit 7-sphere).
    
    Args:
        points: (N, 8) array of E₈ lattice points (nonzero)
    Returns:
        (N, 8) array of unit vectors on S⁷
    """
    norms = np.linalg.norm(points, axis=1, keepdims=True)
    norms = np.where(norms < 1e-15, 1.0, norms)  # avoid division by zero
    return points / norms


def verify_s7_embedding(embedded: np.ndarray) -> dict:
    """Verify points lie on S⁷."""
    norms = np.linalg.norm(embedded, axis=1)
    return {
        'all_unit_norm': bool(np.allclose(norms, 1.0, atol=1e-12)),
        'mean_norm': float(np.mean(norms)),
        'std_norm': float(np.std(norms)),
        'dimension': embedded.shape[1],
        'count': embedded.shape[0],
    }


def compute_angular_distribution(embedded: np.ndarray) -> np.ndarray:
    """Compute pairwise angular distances on S⁷."""
    # Use dot products (cos θ) for efficiency
    dots = embedded @ embedded.T
    dots = np.clip(dots, -1.0, 1.0)
    angles = np.arccos(dots)
    # Extract upper triangle (unique pairs)
    return angles[np.triu_indices(len(embedded), k=1)]


def compute_s7_coordinates(points: np.ndarray) -> dict:
    """Compute S⁷ coordinates with metadata."""
    embedded = embed_shell_in_s7(points)
    norms = np.linalg.norm(points, axis=1)
    return {
        's7_points': embedded,
        'original_norms': norms,
        'shell_radius': float(np.mean(norms)),
    }
