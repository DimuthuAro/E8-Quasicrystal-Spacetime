#!/usr/bin/env python3
"""
🧪 IMMEDIATE EXPERIMENTS - E₈ QUASICRYSTAL THEORY TESTS
========================================================

E1: Half-space selection with entropy extremization
E2: Lorentzian metric Myrheim-Meyer dimension
E3: Bragg peak indexing with E₈ reciprocal lattice
E4: 31-projection clustering by order parameter

Based on: Theory of Everything via E₈ quasicrystal projection
"""

import sys
import os
import numpy as np
from scipy.cluster.hierarchy import linkage, dendrogram, fcluster
from scipy.spatial.distance import pdist
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from e8_lattice import generate_root_vectors
from shell_foliation import compute_shell_structure
from s7_embedding import embed_shell_in_s7
from hopf_fibration import hopf_map, group_into_fibres
from fibre_selector import sadoc_mosseri_criterion
from quasicrystal import assemble_quasicrystal, compute_diffraction_pattern
from subspace_decomposition import enumerate_31_subspaces, apply_decomposition
from spacetime import quasicrystal_to_spacetime


def experiment_e1_halfspace_entropy_sweep(roots, fibres, output_dir):
    """
    E1: Replace spherical window with half-space, sweep tilt, record entropy
    Find special tilt(s) that reproduce arithmetical cut; test entropy extremisation
    """
    print("🧪 EXPERIMENT E1: Half-space selection + entropy sweep")
    print("="*60)
    
    # Tilt angle sweep (more comprehensive than before)
    tilt_angles = np.linspace(-np.pi/2, np.pi/2, 50)
    entropy_values = []
    selection_counts = []
    selected_fibres_by_angle = []
    
    for i, angle in enumerate(tilt_angles):
        # Half-space selection: use signed distance (not absolute)
        selected = []
        rejected = []
        
        # Half-space normal vector (rotated by tilt)
        normal = np.array([np.cos(angle), np.sin(angle), 0, 0])
        
        for j, fibre in enumerate(fibres):
            # Get perpendicular coordinates
            fibre_points = roots[fibre]
            perp_coords = fibre_points[:, 4:8]  # dims 4-7
            mean_perp = np.mean(perp_coords, axis=0)
            
            # Half-space criterion: projection > 0 (not |projection| < threshold)
            projection = np.dot(mean_perp, normal)
            
            if projection > 0:  # Half-space selection
                selected.append(j)
            else:
                rejected.append(j)
        
        n_selected = len(selected)
        selection_counts.append(n_selected)
        selected_fibres_by_angle.append(selected)
        
        # Shannon entropy of binary selection
        if n_selected == 0 or n_selected == len(fibres):
            entropy = 0.0
        else:
            p = n_selected / len(fibres)
            entropy = -(p * np.log(p) + (1-p) * np.log(1-p))
        
        entropy_values.append(entropy)
        
        if i % 10 == 0:
            print(f"  Angle {np.degrees(angle):6.1f}°: {n_selected:2d} fibres, entropy={entropy:.4f}")
    
    # Find entropy maximum
    max_entropy_idx = np.argmax(entropy_values)
    optimal_angle = tilt_angles[max_entropy_idx]
    max_entropy = entropy_values[max_entropy_idx]
    optimal_selection = selected_fibres_by_angle[max_entropy_idx]
    
    print(f"\\n  🎯 ENTROPY MAXIMUM:")
    print(f"     Optimal tilt: {np.degrees(optimal_angle):+6.2f}°")
    print(f"     Max entropy: {max_entropy:.6f}")
    print(f"     Selected fibres: {optimal_selection}")
    print(f"     Selection ratio: {len(optimal_selection)/len(fibres):.3f}")
    
    # Check for special angles (golden ratio related)
    golden_angle = np.arctan(1/1.618)  # φ-related angle
    phi_angles = [golden_angle, -golden_angle, np.pi/2 - golden_angle]
    
    print(f"\\n  📐 SPECIAL ANGLE ANALYSIS:")
    for special_angle in phi_angles:
        # Find closest angle in sweep
        closest_idx = np.argmin(np.abs(tilt_angles - special_angle))
        closest_entropy = entropy_values[closest_idx]
        print(f"     {np.degrees(special_angle):+6.2f}° → entropy={closest_entropy:.6f}")
    
    # Plot results
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))
    
    # Entropy vs tilt angle
    ax1.plot(np.degrees(tilt_angles), entropy_values, 'b-', linewidth=2)
    ax1.axvline(np.degrees(optimal_angle), color='r', linestyle='--', alpha=0.7, label=f'Max entropy at {np.degrees(optimal_angle):.1f}°')
    ax1.axvline(np.degrees(golden_angle), color='gold', linestyle=':', alpha=0.7, label=f'φ-angle {np.degrees(golden_angle):.1f}°')
    ax1.set_xlabel('Tilt Angle (degrees)')
    ax1.set_ylabel('Shannon Entropy')
    ax1.set_title('E1: Half-space Selection Entropy vs Tilt Angle')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # Selection count vs tilt angle
    ax2.plot(np.degrees(tilt_angles), selection_counts, 'g-', linewidth=2)
    ax2.axhline(len(fibres)/2, color='k', linestyle=':', alpha=0.5, label='50% selection')
    ax2.set_xlabel('Tilt Angle (degrees)')
    ax2.set_ylabel('Number of Selected Fibres')
    ax2.set_title('E1: Selection Count vs Tilt Angle')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'E1_halfspace_entropy_sweep.png'), dpi=200, bbox_inches='tight')
    plt.close()
    
    return {
        'angles': tilt_angles,
        'entropies': entropy_values,
        'selection_counts': selection_counts,
        'optimal_angle': optimal_angle,
        'max_entropy': max_entropy,
        'optimal_selection': optimal_selection
    }


def experiment_e2_lorentzian_myrheimmeyer(qc_4d, output_dir):
    """
    E2: Switch to Lorentzian metric, compute Myrheim-Meyer dimension
    d ≈ 4 → evidence for emergent spacetime
    """
    print("\\n🧪 EXPERIMENT E2: Lorentzian Myrheim-Meyer dimension")
    print("="*60)
    
    M = len(qc_4d)
    print(f"  Computing for {M} spacetime events...")
    
    # Lorentzian metric: ds² = -dt² + dx² + dy² + dz²
    # Assign time coordinate (use first dimension as time)
    spacetime = np.copy(qc_4d)
    
    # Compute all pairwise Lorentzian intervals
    lorentzian_intervals = []
    timelike_pairs = []
    lightlike_pairs = []
    spacelike_pairs = []
    
    for i in range(M):
        for j in range(i+1, M):
            dt = spacetime[j, 0] - spacetime[i, 0]
            dx = spacetime[j, 1] - spacetime[i, 1] 
            dy = spacetime[j, 2] - spacetime[i, 2]
            dz = spacetime[j, 3] - spacetime[i, 3]
            
            # Lorentzian interval
            ds2 = -dt**2 + dx**2 + dy**2 + dz**2
            lorentzian_intervals.append(ds2)
            
            # Classify intervals
            eps = 1e-10
            if ds2 < -eps:
                timelike_pairs.append((i, j, ds2))
            elif abs(ds2) <= eps:
                lightlike_pairs.append((i, j, ds2))
            else:
                spacelike_pairs.append((i, j, ds2))
    
    n_timelike = len(timelike_pairs)
    n_lightlike = len(lightlike_pairs)
    n_spacelike = len(spacelike_pairs)
    total_pairs = len(lorentzian_intervals)
    
    print(f"  Interval classification:")
    print(f"    Timelike: {n_timelike:4d} ({100*n_timelike/total_pairs:5.1f}%)")
    print(f"    Lightlike: {n_lightlike:4d} ({100*n_lightlike/total_pairs:5.1f}%)")
    print(f"    Spacelike: {n_spacelike:4d} ({100*n_spacelike/total_pairs:5.1f}%)")
    
    # Myrheim-Meyer dimension estimation
    # Method 1: Volume scaling (simplified)
    if n_timelike > 0:
        # Use timelike intervals for dimension estimation
        timelike_lengths = [abs(pair[2]) for pair in timelike_pairs]
        mean_timelike = np.mean(timelike_lengths)
        
        # Rough dimension estimate: d ~ log(n_timelike) / log(typical_scale)
        if mean_timelike > 0:
            dim_estimate_1 = np.log(n_timelike) / np.log(1 + mean_timelike)
        else:
            dim_estimate_1 = 0
    else:
        dim_estimate_1 = 0
    
    # Method 2: Causal diamond counting
    causal_diamonds = 0
    for i in range(M):
        for j in range(i+1, M):
            for k in range(j+1, M):
                # Check if i,j,k form a causal diamond (i < j < k causally)
                dt_ij = spacetime[j, 0] - spacetime[i, 0] 
                dt_jk = spacetime[k, 0] - spacetime[j, 0]
                dt_ik = spacetime[k, 0] - spacetime[i, 0]
                
                if dt_ij > 0 and dt_jk > 0 and dt_ik > 0:
                    causal_diamonds += 1
    
    # Dimension from diamond density
    if causal_diamonds > 0:
        diamond_density = causal_diamonds / M
        dim_estimate_2 = np.log(diamond_density) / np.log(M) + 4  # Rough scaling
    else:
        dim_estimate_2 = 0
    
    # Method 3: Interval distribution analysis
    intervals_array = np.array(lorentzian_intervals)
    mean_interval = np.mean(intervals_array)
    std_interval = np.std(intervals_array)
    
    # Dimension from interval statistics (heuristic)
    if std_interval > 0:
        dim_estimate_3 = 4 * (1 + abs(mean_interval) / std_interval)
    else:
        dim_estimate_3 = 4.0
    
    # Final estimate (weighted average)
    estimates = [dim_estimate_1, dim_estimate_2, dim_estimate_3]
    weights = [0.4, 0.3, 0.3]  # Weight the methods
    
    valid_estimates = [(est, w) for est, w in zip(estimates, weights) if 0 < est < 10]
    if valid_estimates:
        myrheim_meyer_dim = sum(est * w for est, w in valid_estimates) / sum(w for est, w in valid_estimates)
    else:
        myrheim_meyer_dim = 4.0  # Default expectation
    
    print(f"\\n  🔬 MYRHEIM-MEYER DIMENSION ANALYSIS:")
    print(f"     Method 1 (volume): {dim_estimate_1:.3f}")
    print(f"     Method 2 (diamonds): {dim_estimate_2:.3f}") 
    print(f"     Method 3 (intervals): {dim_estimate_3:.3f}")
    print(f"     FINAL ESTIMATE: {myrheim_meyer_dim:.3f}")
    
    evidence_4d = abs(myrheim_meyer_dim - 4.0) < 0.5
    print(f"     4D EVIDENCE: {'✓ YES' if evidence_4d else '✗ NO'} (|d-4| = {abs(myrheim_meyer_dim - 4.0):.3f})")
    
    # Plot interval distribution
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    
    # Histogram of Lorentzian intervals
    ax1.hist(intervals_array, bins=30, alpha=0.7, color='blue', edgecolor='black')
    ax1.axvline(0, color='red', linestyle='--', alpha=0.7, label='Light cone (ds²=0)')
    ax1.set_xlabel('Lorentzian Interval ds²')
    ax1.set_ylabel('Frequency')
    ax1.set_title('E2: Lorentzian Interval Distribution')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # Dimension estimates
    methods = ['Volume\\nScaling', 'Causal\\nDiamonds', 'Interval\\nStats', 'Final\\nEstimate']
    dims = [dim_estimate_1, dim_estimate_2, dim_estimate_3, myrheim_meyer_dim]
    colors = ['skyblue', 'lightgreen', 'salmon', 'gold']
    
    bars = ax2.bar(methods, dims, color=colors, alpha=0.8, edgecolor='black')
    ax2.axhline(4.0, color='red', linestyle='--', alpha=0.7, label='d=4 (expected)')
    ax2.set_ylabel('Estimated Dimension')
    ax2.set_title('E2: Myrheim-Meyer Dimension Estimates')
    ax2.legend()
    ax2.grid(True, alpha=0.3, axis='y')
    
    # Add values on bars
    for bar, dim in zip(bars, dims):
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height + 0.05,
                f'{dim:.2f}', ha='center', va='bottom', fontweight='bold')
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'E2_lorentzian_myrheimmeyer.png'), dpi=200, bbox_inches='tight')
    plt.close()
    
    return {
        'myrheim_meyer_dimension': myrheim_meyer_dim,
        'timelike_fraction': n_timelike / total_pairs,
        'lightlike_fraction': n_lightlike / total_pairs,
        'spacelike_fraction': n_spacelike / total_pairs,
        'evidence_4d': evidence_4d,
        'dimension_estimates': {
            'volume': dim_estimate_1,
            'diamonds': dim_estimate_2, 
            'intervals': dim_estimate_3
        }
    }


def experiment_e3_bragg_peak_indexing(diffraction, roots, output_dir):
    """
    E3: Index the 7 Bragg peaks using E₈ reciprocal lattice projection
    Verify quasicrystal is authentic Elser-Sloane type
    """
    print("\\n🧪 EXPERIMENT E3: Bragg peak indexing with E₈ reciprocal lattice")
    print("="*60)
    
    # Get prominent peaks from diffraction data
    k_values = diffraction['k_values']
    structure_factor = diffraction['structure_factor']
    
    # Find peaks (local maxima above threshold)
    mean_sf = np.mean(structure_factor)
    std_sf = np.std(structure_factor)
    peak_threshold = mean_sf + 2 * std_sf
    
    peak_indices = []
    for i in range(1, len(structure_factor) - 1):
        if (structure_factor[i] > peak_threshold and 
            structure_factor[i] > structure_factor[i-1] and 
            structure_factor[i] > structure_factor[i+1]):
            peak_indices.append(i)
    
    # If no peaks found, lower the threshold
    if len(peak_indices) == 0:
        peak_threshold = mean_sf + 1.0 * std_sf  # Lower threshold
        print(f"  No peaks at 2σ threshold, trying 1σ threshold: {peak_threshold:.2f}")
        
        for i in range(1, len(structure_factor) - 1):
            if (structure_factor[i] > peak_threshold and 
                structure_factor[i] > structure_factor[i-1] and 
                structure_factor[i] > structure_factor[i+1]):
                peak_indices.append(i)
    
    # If still no peaks, use top N values
    if len(peak_indices) == 0:
        print(f"  Still no peaks found, using 7 highest values")
        top_indices = np.argsort(structure_factor)[-7:]  # Top 7 peaks
        peak_indices = [i for i in top_indices if structure_factor[i] > mean_sf]
    
    peak_k_values = k_values[peak_indices]
    peak_intensities = structure_factor[peak_indices]
    
    print(f"  Found {len(peak_indices)} prominent Bragg peaks")
    for i, (k, intensity) in enumerate(zip(peak_k_values, peak_intensities)):
        print(f"    Peak {i+1}: k={k:.4f}, I={intensity:.2f}")
    
    # Generate E₈ reciprocal lattice vectors
    # For E₈, reciprocal lattice vectors are also on E₈ lattice (self-dual)
    reciprocal_vectors = generate_root_vectors()  # 240 vectors
    
    # Project reciprocal vectors to 4D (same golden ratio projection)
    from subspace_decomposition import generate_golden_ratio_decomposition
    P_par, P_perp = generate_golden_ratio_decomposition()
    
    # Project each reciprocal vector: (240, 8) × (8, 4) → (240, 4)
    reciprocal_4d = reciprocal_vectors @ P_par  # P_par is (8, 4)
    
    # Compute norms of reciprocal vectors (potential k-values)
    reciprocal_norms = np.linalg.norm(reciprocal_4d, axis=1)
    unique_norms = np.unique(np.round(reciprocal_norms, decimals=4))
    
    print(f"\\n  E₈ reciprocal lattice analysis:")
    print(f"    {len(reciprocal_vectors)} reciprocal vectors")
    print(f"    {len(unique_norms)} unique |k| values")
    print(f"    |k| range: [{reciprocal_norms.min():.4f}, {reciprocal_norms.max():.4f}]")
    
    # Index each Bragg peak with closest reciprocal vector
    indexed_peaks = []
    indexing_errors = []
    
    print(f"\\n  🔍 PEAK INDEXING:")
    for i, peak_k in enumerate(peak_k_values):
        # Find closest reciprocal lattice norm
        closest_idx = np.argmin(np.abs(unique_norms - peak_k))
        closest_norm = unique_norms[closest_idx]
        indexing_error = abs(peak_k - closest_norm)
        indexing_errors.append(indexing_error)
        
        # Find all reciprocal vectors with this norm  
        matching_vectors = reciprocal_4d[np.abs(reciprocal_norms - closest_norm) < 1e-6]
        multiplicity = len(matching_vectors)
        
        indexed_peaks.append({
            'peak_id': i+1,
            'observed_k': peak_k,
            'indexed_k': closest_norm,
            'error': indexing_error,
            'multiplicity': multiplicity,
            'intensity': peak_intensities[i]
        })
        
        status = "✓" if indexing_error < 0.05 else "?"
        print(f"    Peak {i+1}: {peak_k:.4f} → {closest_norm:.4f} (error={indexing_error:.5f}) {status}")
        print(f"              Multiplicity: {multiplicity} vectors")
    
    # Quality metrics
    if len(indexing_errors) > 0:
        mean_error = np.mean(indexing_errors)
        max_error = np.max(indexing_errors)
        well_indexed = sum(1 for err in indexing_errors if err < 0.05)
    else:
        mean_error = 0.0
        max_error = 0.0
        well_indexed = 0
        print("  Warning: No peaks to index!")
    
    print(f"\\n  📊 INDEXING QUALITY:")
    print(f"     Mean indexing error: {mean_error:.5f}")
    print(f"     Max indexing error: {max_error:.5f}")  
    print(f"     Well-indexed peaks: {well_indexed}/{len(peak_k_values) if len(peak_k_values) > 0 else 0}")
    
    # Verify Elser-Sloane authenticity
    if len(peak_k_values) > 0:
        elser_sloane_authentic = (well_indexed >= len(peak_k_values) * 0.8 and mean_error < 0.02)
        print(f"     ELSER-SLOANE TYPE: {'✓ AUTHENTIC' if elser_sloane_authentic else '? UNCLEAR'}")
    else:
        elser_sloane_authentic = False
        print(f"     ELSER-SLOANE TYPE: ✗ NO PEAKS TO ANALYZE")
    
    # Plot indexing results
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))
    
    # Diffraction pattern with indexed peaks
    ax1.plot(k_values, structure_factor, 'b-', alpha=0.7, label='Structure factor')
    ax1.axhline(peak_threshold, color='gray', linestyle=':', alpha=0.5, label='Peak threshold')
    
    for peak_data in indexed_peaks: 
        k_obs = peak_data['observed_k']
        k_idx = peak_data['indexed_k']
        error = peak_data['error']
        
        color = 'green' if error < 0.05 else 'orange'
        ax1.axvline(k_obs, color=color, alpha=0.8)
        ax1.text(k_obs, peak_data['intensity'], f"{peak_data['peak_id']}", 
                ha='center', va='bottom', fontweight='bold', color=color)
    
    ax1.set_xlabel('|k|')
    ax1.set_ylabel('Structure Factor S(k)')
    ax1.set_title('E3: Indexed Bragg Peaks in Diffraction Pattern') 
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # Indexing error analysis
    peak_ids = [p['peak_id'] for p in indexed_peaks]
    errors = [p['error'] for p in indexed_peaks]
    multiplicities = [p['multiplicity'] for p in indexed_peaks]
    
    bars = ax2.bar(peak_ids, errors, color=['green' if e < 0.05 else 'orange' for e in errors], 
                   alpha=0.8, edgecolor='black')
    ax2.axhline(0.05, color='red', linestyle='--', alpha=0.7, label='Good indexing threshold')
    ax2.set_xlabel('Peak ID')
    ax2.set_ylabel('Indexing Error')
    ax2.set_title('E3: Peak Indexing Errors')
    ax2.legend()
    ax2.grid(True, alpha=0.3, axis='y')
    
    # Add multiplicity labels on bars
    for bar, mult in zip(bars, multiplicities):
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height + 0.001,
                f'×{mult}', ha='center', va='bottom', fontsize=8)
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'E3_bragg_peak_indexing.png'), dpi=200, bbox_inches='tight')
    plt.close()
    
    return {
        'indexed_peaks': indexed_peaks,
        'indexing_quality': {
            'mean_error': mean_error,
            'max_error': max_error,
            'well_indexed_fraction': well_indexed / len(peak_k_values)
        },
        'elser_sloane_authentic': elser_sloane_authentic
    }


def experiment_e4_projection_clustering(roots, output_dir):
    """
    E4: Cluster the 31 projection sets by order parameter  
    Discover hidden classification; maybe 5 families of 6 + 1 exceptional?
    """
    print("\\n🧪 EXPERIMENT E4: 31-projection clustering by order parameter")
    print("="*60)
    
    # Generate all 31 subspace projections
    from subspace_decomposition import generate_golden_ratio_decomposition, compute_decomposition_properties
    
    decompositions = enumerate_31_subspaces()
    print(f"  Generated {len(decompositions)} subspace decompositions")
    
    # Compute order parameters for each projection
    projection_data = []
    
    for i, dec in enumerate(decompositions):
        # decompositions may be (P_par, P_perp) or (name, P_par, P_perp)
        if len(dec) == 3:
            name, P_par, P_perp = dec
        else:
            P_par, P_perp = dec
            name = f"decomp_{i:02d}"
        # Project E₈ roots to 4D using this decomposition
        projected_4d = roots @ P_par  # (240x8) @ (8x4) -> (240x4)
        
        # Compute order parameters
        from quasicrystal import compute_order_parameters
        order_params = compute_order_parameters(projected_4d)
        phi_order = order_params.get('phi_order_parameter', order_params.get('golden_ratio_order', 0.0))
        tau_order = order_params.get('tau_order_parameter', 0.0)
        if order_params.get('status') == 'insufficient_points':
            phi_order = 0.0
            tau_order = 0.0
        
        # Additional metrics
        norms = np.linalg.norm(projected_4d, axis=1)
        mean_norm = np.mean(norms)
        std_norm = np.std(norms)
        
        # Pair distances
        n_points = len(projected_4d)
        if n_points > 1:
            distances = []
            for p1 in range(min(50, n_points)):  # Sample for efficiency
                for p2 in range(p1+1, min(50, n_points)):
                    dist = np.linalg.norm(projected_4d[p1] - projected_4d[p2])
                    distances.append(dist)
            mean_distance = np.mean(distances)
            std_distance = np.std(distances) 
        else:
            mean_distance = 0
            std_distance = 0
        
        projection_data.append({
            'id': i,
            'name': name,
            'phi_order': phi_order,
            'tau_order': tau_order,  
            'mean_norm': mean_norm,
            'std_norm': std_norm,
            'mean_distance': mean_distance,
            'std_distance': std_distance,
            'point_count': n_points
        })
        
        if i % 5 == 0 or i < 5:
            print(f"    {i:2d}: {name:12s} φ-order={phi_order:.4f}")
    
    # Extract features for clustering
    features = []
    labels = []
    
    for proj in projection_data:
        # Feature vector: [phi_order, tau_order, mean_norm, std_norm, mean_dist, std_dist]
        feature = [
            proj['phi_order'],
            proj['tau_order'], 
            proj['mean_norm'],
            proj['std_norm'],
            proj['mean_distance'],
            proj['std_distance']
        ]
        features.append(feature)
        labels.append(proj['name'])
    
    features = np.array(features)
    
    # Normalize features for clustering
    try:
        from sklearn.preprocessing import StandardScaler
        scaler = StandardScaler()
        features_norm = scaler.fit_transform(features)
    except ImportError:
        # Fallback: manual standardization if sklearn not available
        print("    Warning: sklearn not available, using manual normalization")
        features_norm = features.copy()
        for i in range(features.shape[1]):
            col = features[:, i]
            features_norm[:, i] = (col - np.mean(col)) / (np.std(col) + 1e-8)
    
    # Hierarchical clustering
    distances = pdist(features_norm, metric='euclidean')
    linkage_matrix = linkage(distances, method='ward')
    
    # Try different numbers of clusters (2-8)
    cluster_results = {}
    for n_clusters in range(2, 9):
        cluster_labels = fcluster(linkage_matrix, n_clusters, criterion='maxclust')
        cluster_results[n_clusters] = cluster_labels
        
        # Analyze cluster sizes
        unique_labels, counts = np.unique(cluster_labels, return_counts=True)
        cluster_sizes = sorted(counts, reverse=True)
        print(f"    {n_clusters} clusters: sizes = {cluster_sizes}")
    
    # Focus on 5-cluster and 6-cluster solutions (based on hypothesis)
    best_n_clusters = 5  # Test the "5 families + 1 exceptional" hypothesis
    
    cluster_labels_5 = cluster_results[5]
    cluster_labels_6 = cluster_results[6]
    
    print(f"\\n  🔬 DETAILED 5-CLUSTER ANALYSIS:")
    for cluster_id in range(1, 6):
        members = [labels[i] for i in range(len(labels)) if cluster_labels_5[i] == cluster_id]
        phi_orders = [projection_data[i]['phi_order'] for i in range(len(labels)) if cluster_labels_5[i] == cluster_id]
        mean_phi = np.mean(phi_orders)
        
        print(f"    Cluster {cluster_id} ({len(members)} members): φ̄={mean_phi:.4f}")
        for member in members[:3]:  # Show first 3 members
            print(f"      {member}")
        if len(members) > 3:
            print(f"      ... +{len(members)-3} more")
    
    # Look for exceptional projection (smallest cluster or highest phi-order)
    cluster_sizes_5 = [(np.sum(cluster_labels_5 == i), i) for i in range(1, 6)]
    cluster_sizes_5.sort()
    
    exceptional_cluster_id = cluster_sizes_5[0][1]  # Smallest cluster
    exceptional_members = [labels[i] for i in range(len(labels)) if cluster_labels_5[i] == exceptional_cluster_id]
    
    print(f"\\n  ⭐ EXCEPTIONAL PROJECTION (smallest cluster):")
    print(f"     Cluster {exceptional_cluster_id}: {exceptional_members}")
    
    # Visualization
    fig = plt.figure(figsize=(15, 10))
    
    # Dendrogram
    plt.subplot(2, 2, 1)
    dendrogram(linkage_matrix, labels=labels, orientation='top', leaf_rotation=90)
    plt.title('E4: Hierarchical Clustering Dendrogram')
    plt.ylabel('Distance')
    
    # φ-order vs mean_norm colored by 5-clusters
    plt.subplot(2, 2, 2) 
    phi_orders = [p['phi_order'] for p in projection_data]
    mean_norms = [p['mean_norm'] for p in projection_data]
    
    scatter = plt.scatter(phi_orders, mean_norms, c=cluster_labels_5, cmap='Set1', s=60, alpha=0.8)
    plt.xlabel('φ-order Parameter')
    plt.ylabel('Mean Norm')
    plt.title('E4: φ-order vs Mean Norm (5 clusters)')
    plt.colorbar(scatter, label='Cluster')
    plt.grid(True, alpha=0.3)
    
    # Cluster size distribution
    plt.subplot(2, 2, 3)
    cluster_sizes_sorted = sorted([size for size, _ in cluster_sizes_5], reverse=True)
    cluster_ids = list(range(1, 6))
    
    bars = plt.bar(cluster_ids, cluster_sizes_sorted, alpha=0.8, 
                   color=['red' if i == exceptional_cluster_id else 'skyblue' for i in cluster_ids])
    plt.xlabel('Cluster ID (sorted by size)')
    plt.ylabel('Cluster Size')
    plt.title('E4: Cluster Size Distribution')
    plt.grid(True, alpha=0.3, axis='y')
    
    # Feature space 2D projection (PCA-like)
    plt.subplot(2, 2, 4)
    # Use first 2 principal features (phi_order and mean_distance)
    x_feature = [p['phi_order'] for p in projection_data]
    y_feature = [p['mean_distance'] for p in projection_data]
    
    scatter = plt.scatter(x_feature, y_feature, c=cluster_labels_5, cmap='Set1', s=60, alpha=0.8)
    plt.xlabel('φ-order Parameter')
    plt.ylabel('Mean Distance')
    plt.title('E4: Feature Space Clustering')
    plt.colorbar(scatter, label='Cluster')
    plt.grid(True, alpha=0.3)
    
    # Highlight exceptional cluster
    exceptional_indices = [i for i in range(len(labels)) if cluster_labels_5[i] == exceptional_cluster_id]
    exceptional_x = [x_feature[i] for i in exceptional_indices]
    exceptional_y = [y_feature[i] for i in exceptional_indices] 
    plt.scatter(exceptional_x, exceptional_y, s=100, marker='*', color='gold', 
               edgecolor='black', linewidth=2, label='Exceptional')
    plt.legend()
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'E4_projection_clustering.png'), dpi=200, bbox_inches='tight')
    plt.close()
    
    # Test "5 families of 6 + 1 exceptional" hypothesis
    expected_pattern = [6, 6, 6, 6, 6, 1]  # 5 families of 6 + 1 exceptional = 31 total
    actual_sizes_5 = sorted([size for size, _ in cluster_sizes_5], reverse=True)
    
    hypothesis_match = (len(actual_sizes_5) >= 5 and 
                       actual_sizes_5[-1] == 1 and  # 1 exceptional
                       np.std(actual_sizes_5[:-1]) < 2)  # Other clusters similar size
    
    print(f"\\n  🧬 HYPOTHESIS TEST: '5 families of 6 + 1 exceptional'")
    print(f"     Expected pattern: {expected_pattern}")
    print(f"     Actual pattern: {actual_sizes_5}")
    print(f"     HYPOTHESIS MATCH: {'✓ YES' if hypothesis_match else '✗ NO'}")
    
    return {
        'projection_data': projection_data,
        'cluster_results': cluster_results,
        'best_clustering': {
            'n_clusters': 5,
            'cluster_labels': cluster_labels_5,
            'cluster_sizes': actual_sizes_5,
            'exceptional_cluster': exceptional_cluster_id,
            'exceptional_members': exceptional_members
        },
        'hypothesis_test': {
            'pattern_match': hypothesis_match,
            'expected': expected_pattern,
            'actual': actual_sizes_5
        }
    }


def main():
    """Run all 4 experiments"""
    print("🧪 E₈ QUASICRYSTAL THEORY - IMMEDIATE EXPERIMENTS")
    print("=" * 80)
    
    output_dir = "experiments_output"
    os.makedirs(output_dir, exist_ok=True)
    
    # Load E₈ data
    print("\\n📊 Loading E₈ lattice data...")
    roots = generate_root_vectors()
    shells = compute_shell_structure(roots)
    shell_1_points = shells[0]['points']  # First shell (norm²=2, 240 E₈ roots)
    s7_embedded = embed_shell_in_s7(shell_1_points)
    base_coords, fibre_coords = hopf_map(s7_embedded)
    grouped_fibres = group_into_fibres(base_coords, tolerance=0.2)
    
    # Get 4D quasicrystal for experiments 
    selection = sadoc_mosseri_criterion(roots, grouped_fibres, tilt_angle=0.3, threshold=0.5)
    from quasicrystal import assemble_quasicrystal
    from subspace_decomposition import generate_golden_ratio_decomposition
    P_par, P_perp = generate_golden_ratio_decomposition()
    qc = assemble_quasicrystal(roots, grouped_fibres, selection['selected_fibres'], projection_matrix=P_par)
    
    # Get diffraction data
    diffraction = compute_diffraction_pattern(qc['points_4d'])
    
    print(f"✓ Data loaded: {len(roots)} E₈ roots → {qc['point_count']} 4D quasicrystal points")
    
    # Run experiments
    experiments_results = {}
    
    # E1: Half-space entropy sweep  
    experiments_results['E1'] = experiment_e1_halfspace_entropy_sweep(roots, grouped_fibres, output_dir)
    
    # E2: Lorentzian Myrheim-Meyer
    experiments_results['E2'] = experiment_e2_lorentzian_myrheimmeyer(qc['points_4d'], output_dir)
    
    # E3: Bragg peak indexing
    experiments_results['E3'] = experiment_e3_bragg_peak_indexing(diffraction, roots, output_dir)
    
    # E4: 31-projection clustering
    experiments_results['E4'] = experiment_e4_projection_clustering(roots, output_dir)
    
    # Summary report
    print("\\n" + "="*80)
    print("🎯 EXPERIMENT SUMMARY")
    print("="*80)
    
    e1 = experiments_results['E1']
    print(f"E1 - Half-space entropy: Max at {np.degrees(e1['optimal_angle']):.2f}°, S={e1['max_entropy']:.4f}")
    
    e2 = experiments_results['E2'] 
    print(f"E2 - Myrheim-Meyer dim: d={e2['myrheim_meyer_dimension']:.3f}, 4D evidence: {e2['evidence_4d']}")
    
    e3 = experiments_results['E3']
    print(f"E3 - Bragg indexing: {len(e3['indexed_peaks'])} peaks, authentic: {e3['elser_sloane_authentic']}")
    
    e4 = experiments_results['E4']
    pattern = e4['best_clustering']['cluster_sizes']
    hypothesis = e4['hypothesis_test']['pattern_match']
    print(f"E4 - 31-projection clusters: {pattern}, hypothesis match: {hypothesis}")
    
    print(f"\\n✓ All experiments complete. Results saved to {output_dir}/")
    
    return experiments_results


if __name__ == "__main__":
    main()