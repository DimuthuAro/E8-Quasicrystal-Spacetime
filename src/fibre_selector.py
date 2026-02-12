"""
Fibre Selector (Sadoc–Mosseri Criterion)
=========================================
Implements the binary selection criterion that chooses fibres from the
Hopf fibration to produce the 4D quasicrystal.

The selection is based on an arithmetical criterion related to a "tilt angle"
in the perpendicular space, which we hypothesize corresponds to an
entropy/causality gradient.
"""

import numpy as np


def compute_fibre_invariant(points_8d: np.ndarray, fibre_indices: np.ndarray) -> float:
    """Compute an invariant quantity for a fibre.
    
    Reference: Sadoc & Mosseri use norm of perpendicular component or parity 
    of scalar product. For E8 roots as (a,b) quaternions, the perpendicular 
    coordinate relates to a * conj(q0).
    """
    fibre_points = points_8d[fibre_indices]
    
    # Method 1: Sum of perpendicular-space projections (dims 4-7)
    perp_sum = np.sum(fibre_points[:, 4:])
    
    # Method 2: Quaternionic invariant (alternative)
    # Split 8D points into two quaternions (a,b)
    a_quat = fibre_points[:, :4]  # first quaternion
    b_quat = fibre_points[:, 4:]  # second quaternion
    
    # Compute quaternion norms
    norm_a = np.sum(a_quat ** 2, axis=1)
    norm_b = np.sum(b_quat ** 2, axis=1)
    
    # Invariant: difference of norms (relates to perpendicular projection)
    quat_invariant = np.sum(norm_a - norm_b)
    
    # Debug: print both methods
    print(f"    Fibre size={len(fibre_indices)}: perp_sum={perp_sum:.4f}, quat_inv={quat_invariant:.4f}")
    
    # Return the quaternionic invariant (more theoretically justified)
    return quat_invariant / max(len(fibre_indices), 1)


def sadoc_mosseri_criterion(points_8d: np.ndarray, fibres: list,
                             tilt_angle: float = 0.3,
                             threshold: float = 0.5,
                             debug_bypass: bool = False) -> dict:
    """Apply the Sadoc–Mosseri binary selection criterion using perpendicular-space window.
    
    The proper Sadoc-Mosseri algorithm:
    1. Projects E₈ points to perpendicular space (dims 4-7)
    2. Applies a window/cut in perpendicular space
    3. Selects fibres whose perpendicular coordinates satisfy the criterion
    
    Args:
        points_8d: (N, 8) original lattice points
        fibres: list of index arrays (from Hopf fibre grouping)
        tilt_angle: angle parameterizing the cut hyperplane orientation
        threshold: window size in perpendicular space (default 0.5)
        debug_bypass: if True, use simple alternating selection for debugging
    
    Returns:
        SelectionResult dict
    """
    print(f"\n  Sadoc-Mosseri Selection Analysis")
    print(f"  Total fibres: {len(fibres)}")
    print(f"  Window threshold: {threshold:.4f}")
    print(f"  Tilt angle: {np.degrees(tilt_angle):.2f}°")
    
    if debug_bypass:
        # Simple alternating selection for debugging/comparison
        selected_indices = [i for i in range(0, len(fibres), 2)]  # 0,2,4,6,8,...
        selected = np.array(selected_indices)
        rejected = np.array([i for i in range(len(fibres)) if i not in selected])
        
        print(f"  DEBUG MODE: Alternating selection {selected.tolist()}")
        
        # Still compute invariants for analysis
        invariants = []
        for i, fibre in enumerate(fibres):
            inv = compute_fibre_invariant(points_8d, fibre)
            invariants.append(inv)
            print(f"  Fibre {i}: invariant = {inv:.6f}")
            
        selection_mask = np.zeros(len(fibres), dtype=bool)
        selection_mask[selected] = True
        
        return {
            'selected_fibres': selected,
            'rejected_fibres': rejected,
            'selection_mask': selection_mask,
            'invariants': np.array(invariants),
            'tilt_angle': tilt_angle,
            'threshold': threshold,
            'selection_ratio': len(selected) / max(len(fibres), 1),
            'debug_mode': True,
        }
    
    # PROPER SADOC-MOSSERI ALGORITHM
    print(f"  Applying proper perpendicular-space window selection...")
    
    selected = []
    rejected = []
    fibre_perp_coords = []
    acceptance_values = []
    
    # Define perpendicular-space window using tilt-rotated hyperplane
    # Window normal vector (rotated by tilt angle)
    window_normal = np.array([np.cos(tilt_angle), np.sin(tilt_angle), 0, 0])
    
    for i, fibre in enumerate(fibres):
        # Get perpendicular-space coordinates for this fibre
        fibre_points = points_8d[fibre]
        perp_coords = fibre_points[:, 4:8]  # perpendicular space (dims 4-7)
        
        # Compute fibre's mean position in perpendicular space
        mean_perp = np.mean(perp_coords, axis=0)
        fibre_perp_coords.append(mean_perp)
        
        # Sadoc-Mosseri window criterion: project onto window normal
        projection = np.dot(mean_perp, window_normal)
        
        # Distance from window hyperplane
        distance_from_plane = abs(projection)
        
        # Accept if within threshold distance from hyperplane
        accepted = distance_from_plane <= threshold
        acceptance_values.append(distance_from_plane)
        
        if accepted:
            selected.append(i)
            status = "ACCEPT"
        else:
            rejected.append(i)
            status = "REJECT"
            
        print(f"  Fibre {i}: perp_dist={distance_from_plane:.4f} → {status}")
    
    selected = np.array(selected)
    rejected = np.array(rejected)
    
    # Ensure we have at least one selection (adjust threshold if needed)
    if len(selected) == 0:
        print(f"  Warning: No fibres selected, expanding window...")
        # Select fibre with minimum distance
        min_dist_idx = np.argmin(acceptance_values)
        selected = np.array([min_dist_idx])
        rejected = np.array([i for i in range(len(fibres)) if i != min_dist_idx])
        print(f"  Fallback: Selected fibre {min_dist_idx} (min distance)")
    
    print(f"  Final selection: {len(selected)} fibres {selected.tolist()}")
    print(f"  Selection ratio: {len(selected) / len(fibres):.3f}")
    
    # Compute invariants for analysis
    invariants = []
    for i, fibre in enumerate(fibres):
        inv = compute_fibre_invariant(points_8d, fibre)
        invariants.append(inv)
    
    selection_mask = np.zeros(len(fibres), dtype=bool)
    selection_mask[selected] = True
    
    return {
        'selected_fibres': selected,
        'rejected_fibres': rejected,
        'selection_mask': selection_mask,
        'invariants': np.array(invariants),
        'fibre_perp_coords': np.array(fibre_perp_coords),
        'acceptance_values': np.array(acceptance_values),
        'window_normal': window_normal,
        'tilt_angle': tilt_angle,
        'threshold': threshold,
        'selection_ratio': len(selected) / max(len(fibres), 1),
        'debug_mode': False,
    }


def compute_entropy_gradient(tilt_angle: float, n_fibres: int = 100) -> float:
    """Compute the entropy gradient as a function of tilt angle.
    S(θ) = -Σ pᵢ log(pᵢ) where pᵢ depends on the selection criterion.
    """
    # Model selection probability as function of tilt
    p_select = 0.5 + 0.5 * np.sin(tilt_angle)
    p_reject = 1.0 - p_select
    
    # Shannon entropy
    eps = 1e-15
    S = -(p_select * np.log(p_select + eps) + p_reject * np.log(p_reject + eps))
    
    # Gradient: dS/dθ
    dS = -0.5 * np.cos(tilt_angle) * (np.log(p_select + eps) - np.log(p_reject + eps))
    
    return float(dS)


def sweep_tilt_angles(points_8d: np.ndarray, fibres: list,
                       angles: np.ndarray = None) -> dict:
    """Sweep tilt angle and compute selection ratios and entropy."""
    if angles is None:
        angles = np.linspace(-np.pi/2, np.pi/2, 100)
    
    ratios = []
    entropies = []
    entropy_gradients = []
    
    for angle in angles:
        result = sadoc_mosseri_criterion(points_8d, fibres, tilt_angle=angle)
        ratios.append(result['selection_ratio'])
        
        p = result['selection_ratio']
        eps = 1e-15
        S = -(p * np.log(p + eps) + (1-p) * np.log(1-p + eps))
        entropies.append(S)
        entropy_gradients.append(compute_entropy_gradient(angle))
    
    return {
        'angles': angles,
        'selection_ratios': np.array(ratios),
        'entropies': np.array(entropies),
        'entropy_gradients': np.array(entropy_gradients),
    }
