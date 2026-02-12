#!/usr/bin/env python3
"""
🧪 QUICK TEST - E1 Half-space entropy sweep only
"""

import sys
import os
import numpy as np
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

def quick_e1_test():
    print("🧪 QUICK E1 TEST: Half-space entropy sweep")
    print("="*50)
    
    # Load minimal data
    roots = generate_root_vectors()
    print(f"Roots shape: {roots.shape}")
    
    shells = compute_shell_structure(roots)
    shell_1_points = shells[0]['points']
    print(f"Shell 1 shape: {shell_1_points.shape}")
    
    s7_embedded = embed_shell_in_s7(shell_1_points)
    print(f"S7 embedded shape: {s7_embedded.shape}")
    
    base_coords, fibre_coords = hopf_map(s7_embedded)
    print(f"Base coords shape: {base_coords.shape}")
    print(f"Fibre coords shape: {fibre_coords.shape}")
    
    # Try to call group_into_fibres and catch any error
    try:
        grouped_fibres = group_into_fibres(base_coords, tolerance=0.2)
        print(f"Grouped fibres: {len(grouped_fibres)} fibres")
    except Exception as e:
        print(f"Error in group_into_fibres: {e}")
        print(f"base_coords type: {type(base_coords)}")
        print(f"base_coords[0] shape: {base_coords[0].shape}")
        return
    
    print(f"Data loaded: {len(roots)} roots → {len(grouped_fibres)} fibres")
    
    # Simple entropy sweep (fewer angles for speed)
    tilt_angles = np.linspace(-np.pi/4, np.pi/4, 10)  # Just 10 angles
    entropy_values = []
    
    for angle in tilt_angles:
        # Half-space selection
        selected = []
        normal = np.array([np.cos(angle), np.sin(angle), 0, 0])
        
        for j, fibre in enumerate(grouped_fibres):
            fibre_points = roots[fibre]
            perp_coords = fibre_points[:, 4:8]
            mean_perp = np.mean(perp_coords, axis=0)
            projection = np.dot(mean_perp, normal)
            
            if projection > 0:
                selected.append(j)
        
        n_selected = len(selected)
        if n_selected == 0 or n_selected == len(grouped_fibres):
            entropy = 0.0
        else:
            p = n_selected / len(grouped_fibres)
            entropy = -(p * np.log(p) + (1-p) * np.log(1-p))
        
        entropy_values.append(entropy)
        print(f"  Angle {np.degrees(angle):6.1f}°: {n_selected:2d} fibres, entropy={entropy:.4f}")
    
    # Find maximum
    max_idx = np.argmax(entropy_values)
    print(f"\\n🎯 Max entropy: {entropy_values[max_idx]:.4f} at {np.degrees(tilt_angles[max_idx]):+.1f}°")
    
    # Quick plot
    os.makedirs("experiments_output", exist_ok=True)
    plt.figure(figsize=(8, 5))
    plt.plot(np.degrees(tilt_angles), entropy_values, 'b-o', linewidth=2)
    plt.xlabel('Tilt Angle (degrees)')
    plt.ylabel('Shannon Entropy')
    plt.title('E1 Quick Test: Half-space Selection Entropy')
    plt.grid(True, alpha=0.3)
    plt.savefig('experiments_output/E1_quick_test.png', dpi=150, bbox_inches='tight')
    plt.close()
    
    print("✓ E1 quick test complete! Plot saved to experiments_output/E1_quick_test.png")
    return entropy_values

if __name__ == "__main__":
    quick_e1_test()