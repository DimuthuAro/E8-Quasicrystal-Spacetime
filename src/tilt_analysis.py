"""
Tilt / Entropy Analysis
========================
Tests Hypothesis 1: The arithmetical selection criterion corresponds
to an entropy/causality gradient (tilt angle).

Key question: Is the Sadoc–Mosseri selection mathematically equivalent
to selecting points above/below a tilted hyperplane?
"""

import numpy as np
from scipy import stats


def compute_projection_tilt(P_parallel: np.ndarray, P_perp: np.ndarray,
                             points_8d: np.ndarray) -> dict:
    """Compute the tilt angle between the projection hyperplane and the lattice.
    
    The tilt measures how "far" the cutting hyperplane is from being
    aligned with a lattice direction.
    """
    parallel_4d = points_8d @ P_parallel
    perp_4d = points_8d @ P_perp
    
    # Tilt: angle between mean direction in parallel and perpendicular spaces
    par_norms = np.linalg.norm(parallel_4d, axis=1)
    perp_norms = np.linalg.norm(perp_4d, axis=1)
    
    # Avoid division by zero
    mask = (par_norms > 1e-10) & (perp_norms > 1e-10)
    
    if np.sum(mask) == 0:
        return {'tilt_angle': 0.0, 'correlation': 0.0}
    
    # Tilt angle: arctan(mean_perp / mean_par)
    mean_par = float(np.mean(par_norms[mask]))
    mean_perp = float(np.mean(perp_norms[mask]))
    tilt = np.arctan2(mean_perp, mean_par)
    
    # Correlation between parallel and perpendicular norms
    corr, p_value = stats.pearsonr(par_norms[mask], perp_norms[mask])
    
    return {
        'tilt_angle': float(tilt),
        'tilt_degrees': float(np.degrees(tilt)),
        'mean_parallel_norm': mean_par,
        'mean_perpendicular_norm': mean_perp,
        'correlation': float(corr),
        'correlation_p_value': float(p_value),
    }


def entropy_gradient_field(perp_4d: np.ndarray, n_bins: int = 20) -> dict:
    """Compute entropy as Shannon entropy of local density distribution.
    S = -Σ pᵢ log pᵢ where pᵢ are normalized densities in perpendicular space.
    """
    norms = np.linalg.norm(perp_4d, axis=1)
    
    # Bin by perpendicular-space distance
    bins = np.linspace(0, np.max(norms) + 0.01, n_bins + 1)
    counts, _ = np.histogram(norms, bins=bins)
    
    # Normalize to probabilities
    total = np.sum(counts)
    if total == 0:
        return {'entropy': np.zeros(n_bins), 'bin_centers': (bins[:-1]+bins[1:])/2}
    
    probs = counts / total
    
    # Shannon entropy per bin (local entropy)
    eps = 1e-15
    entropy_per_bin = np.where(probs > 0, -probs * np.log(probs + eps), 0)
    total_entropy = float(np.sum(entropy_per_bin))
    
    bin_centers = (bins[:-1] + bins[1:]) / 2
    
    # Entropy gradient (finite differences)
    gradient = np.gradient(entropy_per_bin, bin_centers)
    
    return {
        'entropy_per_bin': entropy_per_bin,
        'total_entropy': total_entropy,
        'bin_centers': bin_centers,
        'entropy_gradient': gradient,
        'probability_distribution': probs,
    }


def correlation_analysis(selection_mask: np.ndarray,
                          invariants: np.ndarray,
                          tilt_angle: float) -> dict:
    """Statistical test: does selection correlate with tilt-based prediction?"""
    # Predicted selection based on tilt angle
    predicted = invariants > np.cos(tilt_angle) * np.mean(invariants)
    
    # Agreement rate
    agreement = np.mean(selection_mask == predicted)
    
    # Chi-squared test
    contingency = np.array([
        [np.sum(selection_mask & predicted), np.sum(selection_mask & ~predicted)],
        [np.sum(~selection_mask & predicted), np.sum(~selection_mask & ~predicted)],
    ])
    
    if np.any(contingency.sum(axis=0) == 0) or np.any(contingency.sum(axis=1) == 0):
        chi2, p_val = 0.0, 1.0
    else:
        chi2, p_val = stats.chi2_contingency(contingency)[:2]
    
    return {
        'agreement_rate': float(agreement),
        'chi_squared': float(chi2),
        'p_value': float(p_val),
        'significant': p_val < 0.05,
        'contingency_table': contingency.tolist(),
    }
