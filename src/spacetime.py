"""
Spacetime Generator
===================
Tests Hypothesis 3: The algorithm generates 4D spacetime points.

Reinterprets quasicrystal vertices as discrete spacetime events (t, x, y, z)
and analyzes causal structure, light cone geometry, and particle-like excitations.
"""

import numpy as np
from scipy.spatial import Voronoi, Delaunay


def quasicrystal_to_spacetime(points_4d: np.ndarray) -> dict:
    """Reinterpret 4D quasicrystal points as spacetime events using causal set formalism.
    In causal set theory, discrete points have partial order from causal relations.
    
    Convention: (t, x, y, z) = (x₀, x₁, x₂, x₃)
    Causal relation: i ≺ j if j is in future light cone of i
    """
    t = points_4d[:, 0]
    x = points_4d[:, 1]
    y = points_4d[:, 2]
    z = points_4d[:, 3]
    
    # Sort by time coordinate (causal set ordering)
    time_order = np.argsort(t)
    sorted_events = points_4d[time_order]
    
    return {
        'events': sorted_events,
        't': sorted_events[:, 0],
        'x': sorted_events[:, 1],
        'y': sorted_events[:, 2],
        'z': sorted_events[:, 3],
        'num_events': len(sorted_events),
        'causal_set_interpretation': True,
    }


def compute_causal_structure(events: np.ndarray) -> dict:
    """Compute light cone structure using Minkowski metric.
    
    For two events: Δs² = -(Δt)² + (Δx)² + (Δy)² + (Δz)²
    - Timelike:  Δs² < 0  (causally connected)
    - Lightlike: Δs² = 0  (on light cone)
    - Spacelike: Δs² > 0  (causally disconnected)
    """
    N = len(events)
    if N < 2:
        return {'status': 'insufficient_events'}
    
    # Compute Minkowski intervals
    # Limit pairs for performance
    max_pairs = min(N, 500)
    subset = events[:max_pairs]
    M = len(subset)
    
    dt = subset[:, 0:1] - subset[:, 0:1].T
    dx = subset[:, 1:2] - subset[:, 1:2].T
    dy = subset[:, 2:3] - subset[:, 2:3].T
    dz = subset[:, 3:4] - subset[:, 3:4].T
    
    ds_sq = -dt**2 + dx**2 + dy**2 + dz**2
    
    # Classify intervals (upper triangle only)
    upper = ds_sq[np.triu_indices(M, k=1)]
    
    eps = 1e-10
    timelike = np.sum(upper < -eps)
    lightlike = np.sum(np.abs(upper) <= eps)
    spacelike = np.sum(upper > eps)
    total = len(upper)
    
    # Causal adjacency matrix (more lenient for discrete spacetime)
    causal_matrix = np.zeros((M, M), dtype=bool)
    timelike_connections = 0
    for i in range(M):
        for j in range(i+1, M):
            ds2_val = ds_sq[i, j] 
            dt_val = dt[i, j]
            
            # Include both timelike and lightlike as causal
            if ds2_val < -1e-6 and dt_val < -1e-10:  # timelike, j in future
                causal_matrix[i, j] = True
                timelike_connections += 1
            elif abs(ds2_val) < 1e-6 and abs(dt_val) > 1e-10:  # lightlike
                causal_matrix[i, j] = True if dt_val < 0 else False
    
    # Causal depth (longest chain)
    depths = np.zeros(M, dtype=int)
    for i in range(M):
        for j in range(i+1, M):
            if causal_matrix[i, j]:
                depths[j] = max(depths[j], depths[i] + 1)
    
    return {
        'timelike_pairs': int(timelike),
        'lightlike_pairs': int(lightlike),
        'spacelike_pairs': int(spacelike),
        'total_pairs': int(total),
        'timelike_fraction': float(timelike / max(total, 1)),
        'spacelike_fraction': float(spacelike / max(total, 1)),
        'causal_matrix': causal_matrix,
        'causal_depth': int(np.max(depths)) if len(depths) > 0 else 0,
        'ds_squared': ds_sq,
    }


def compute_discrete_curvature(events: np.ndarray) -> dict:
    """Estimate discrete curvature from quasicrystal spacetime.
    Uses deficit angles from Voronoi tessellation.
    """
    # Use spatial coordinates for Voronoi
    spatial = events[:, 1:4]
    
    if len(spatial) < 5:
        return {'status': 'insufficient_points'}
    
    try:
        vor = Voronoi(spatial)
        
        # Compute vertex densities (related to curvature)
        volumes = []
        for region_idx in vor.point_region:
            region = vor.regions[region_idx]
            if -1 not in region and len(region) > 0:
                vertices = vor.vertices[region]
                if len(vertices) >= 4:
                    vol = ConvexHull_volume(vertices)
                    volumes.append(vol)
        
        if len(volumes) == 0:
            volumes = [1.0]
        
        volumes = np.array(volumes)
        mean_vol = float(np.mean(volumes))
        
        # Curvature proxy: deviation from uniform density
        curvature_proxy = np.std(volumes) / mean_vol if mean_vol > 0 else 0
        
        return {
            'mean_voronoi_volume': mean_vol,
            'curvature_proxy': float(curvature_proxy),
            'num_cells': len(volumes),
        }
    except Exception:
        return {'status': 'voronoi_failed', 'curvature_proxy': 0.0}


def ConvexHull_volume(vertices: np.ndarray) -> float:
    """Compute volume of convex hull."""
    try:
        from scipy.spatial import ConvexHull
        hull = ConvexHull(vertices)
        return hull.volume
    except Exception:
        return 0.0


def identify_particle_excitations(events: np.ndarray,
                                    causal_structure: dict) -> dict:
    """Identify particle-like excitations as defects in quasiperiodic order.
    
    Defects in quasicrystals can be interpreted as particles:
    - Dislocations → gauge bosons
    - Vacancies → fermions  
    - Interstitials → massive particles
    """
    spatial = events[:, 1:4]
    N = len(spatial)
    
    if N < 10:
        return {'status': 'insufficient_points', 'defects': []}
    
    # Compute local density for each point
    from scipy.spatial import cKDTree
    tree = cKDTree(spatial)
    
    # k nearest neighbors
    k = min(12, N - 1)
    dists, _ = tree.query(spatial, k=k+1)
    local_densities = k / (4/3 * np.pi * dists[:, -1]**3 + 1e-15)
    
    mean_density = np.mean(local_densities)
    std_density = np.std(local_densities)
    
    # Defects: points with anomalous local density
    threshold = 2.0  # sigma
    high_density = local_densities > mean_density + threshold * std_density
    low_density = local_densities < mean_density - threshold * std_density
    
    return {
        'num_high_density_defects': int(np.sum(high_density)),
        'num_low_density_defects': int(np.sum(low_density)),
        'total_defects': int(np.sum(high_density) + np.sum(low_density)),
        'mean_density': float(mean_density),
        'defect_fraction': float((np.sum(high_density) + np.sum(low_density)) / N),
        'high_density_positions': events[high_density],
        'low_density_positions': events[low_density],
    }
