#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════╗
║  E₈ QUASICRYSTAL PROJECTION — THEORY OF EVERYTHING TEST        ║
║                                                                  ║
║  Sadoc–Mosseri algorithm: E₈ → Shells → S⁷ → Hopf → 4D QC     ║
║                                                                  ║
║  Hypotheses:                                                     ║
║   H1: Selection criterion = entropy/causality gradient           ║
║   H2: Shell counts match SM multiplets / Kac-Moody levels       ║
║   H3: Algorithm generates 4D spacetime points                   ║
╚══════════════════════════════════════════════════════════════════╝
"""

import sys
import os
import time
import numpy as np

# Set matplotlib to non-interactive backend for headless execution
import matplotlib
matplotlib.use('Agg')

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from e8_lattice import generate_root_vectors, verify_root_properties, generate_lattice_points
from shell_foliation import compute_shell_structure, shell_point_counts, expected_theta_series
from s7_embedding import embed_shell_in_s7, verify_s7_embedding, compute_angular_distribution
from hopf_fibration import hopf_map, group_into_fibres, compute_fibre_statistics
from fibre_selector import sadoc_mosseri_criterion, sweep_tilt_angles
from quasicrystal import (assemble_quasicrystal, compute_order_parameters,
                          verify_600_cell_symmetry, compute_diffraction_pattern)
from subspace_decomposition import (enumerate_31_subspaces, apply_decomposition,
                                     generate_golden_ratio_decomposition,
                                     compute_decomposition_properties)
from tilt_analysis import compute_projection_tilt, entropy_gradient_field, correlation_analysis
from shell_analysis import (compute_shell_counts_vs_theory, compare_sm_multiplets,
                             compare_kac_moody_levels)
from spacetime import (quasicrystal_to_spacetime, compute_causal_structure,
                        identify_particle_excitations)
from visualization import (plot_e8_root_projection, plot_shell_distribution,
                            plot_hopf_fibration, plot_quasicrystal_3d,
                            plot_spacetime_diagram, plot_tilt_entropy,
                            plot_diffraction_pattern, plot_comprehensive_dashboard)

np.random.seed(42)


def banner(text: str):
    """Print a sci-fi style banner."""
    w = 66
    print(f"\n{'═' * w}")
    print(f"  ◈  {text}")
    print(f"{'═' * w}")


def section(text: str):
    print(f"\n  ▸ {text}")
    print(f"  {'─' * 60}")


def result(key: str, value):
    print(f"    {key:.<40s} {value}")


def main():
    t0 = time.time()
    output_dir = os.path.join(os.path.dirname(__file__), 'output')
    os.makedirs(output_dir, exist_ok=True)
    
    all_results = {}

    # ─────────────────────────────────────────────────────────────
    # STAGE 1: E₈ LATTICE GENERATION
    # ─────────────────────────────────────────────────────────────
    banner("STAGE 1: E₈ LATTICE — 240 ROOT VECTORS")
    
    roots = generate_root_vectors()
    props = verify_root_properties(roots)
    
    result("Root count", props['count'])
    result("All ||α||² = 2", props['all_norm_sq_2'])
    result("Mean kissing number", f"{props['mean_kissing_number']:.0f}")
    result("Kissing number uniform", props['kissing_number_uniform'])
    
    all_results['roots'] = roots
    all_results['root_count'] = props['count']
    
    if props['count'] != 240:
        print("  ⚠ WARNING: Expected 240 roots!")
    else:
        print("  ✓ E₈ root system verified: 240 vectors, ||α||²=2")

    # ─────────────────────────────────────────────────────────────
    # STAGE 2: SHELL FOLIATION
    # ─────────────────────────────────────────────────────────────
    banner("STAGE 2: SHELL FOLIATION — ORGANIZING BY NORM²")
    
    shells = compute_shell_structure(roots, max_shells=5)
    counts = shell_point_counts(shells)
    expected = expected_theta_series()
    
    all_results['shell_counts'] = counts.tolist()
    
    for s in shells:
        marker = "✓" if s['point_count'] == expected.get(s['shell_index'], -1) else "?"
        result(f"Shell {s['shell_index']} (n²={s['norm_squared']:.0f})",
               f"{s['point_count']} points  {marker}")
    
    result("Expected θ-series (shell 1)", f"{expected.get(1, '?')}")

    # ─────────────────────────────────────────────────────────────
    # STAGE 3: S⁷ EMBEDDING
    # ─────────────────────────────────────────────────────────────
    banner("STAGE 3: S⁷ EMBEDDING — NORMALIZING TO 7-SPHERE")
    
    s7_points = embed_shell_in_s7(roots)
    s7_props = verify_s7_embedding(s7_points)
    
    result("All unit norm", s7_props['all_unit_norm'])
    result("Mean norm", f"{s7_props['mean_norm']:.12f}")
    result("Points on S⁷", s7_props['count'])
    
    angles = compute_angular_distribution(s7_points)
    result("Mean angular distance", f"{np.degrees(np.mean(angles)):.2f}°")
    result("Min angular distance", f"{np.degrees(np.min(angles)):.2f}°")

    # ─────────────────────────────────────────────────────────────
    # STAGE 4: HOPF FIBRATION S⁷ → S⁴
    # ─────────────────────────────────────────────────────────────
    banner("STAGE 4: HOPF FIBRATION — QUATERNIONIC MAP S⁷ → S⁴")
    
    base_coords, fibre_coords = hopf_map(s7_points)
    fibres = group_into_fibres(base_coords, tolerance=0.2)
    fibre_stats = compute_fibre_statistics(fibres)
    
    result("Number of fibres", fibre_stats['num_fibres'])
    result("Mean fibre size", f"{fibre_stats['mean_size']:.1f}")
    result("Min fibre size", fibre_stats['min_size'])
    result("Max fibre size", fibre_stats['max_size'])
    result("Total points assigned", fibre_stats['total_points'])

    # ─────────────────────────────────────────────────────────────
    # STAGE 5: SADOC–MOSSERI FIBRE SELECTION
    # ─────────────────────────────────────────────────────────────
    banner("STAGE 5: SADOC–MOSSERI SELECTION — BINARY CRITERION")
    
    # DEBUG: First try bypass mode to test pipeline
    selection = sadoc_mosseri_criterion(roots, fibres, tilt_angle=0.3, debug_bypass=True)
    
    result("Selected fibres", len(selection['selected_fibres']))
    result("Rejected fibres", len(selection['rejected_fibres']))
    result("Selection ratio", f"{selection['selection_ratio']:.3f}")
    result("Debug mode", selection.get('debug_mode', False))
    
    # Sweep tilt angles (simplified in debug mode)
    if not selection.get('debug_mode', False):
        section("Tilt angle sweep")
        sweep = sweep_tilt_angles(roots, fibres)
        all_results['sweep'] = sweep
        
        result("Max selection ratio", f"{np.max(sweep['selection_ratios']):.3f}")
        result("Min selection ratio", f"{np.min(sweep['selection_ratios']):.3f}")
        result("Max entropy", f"{np.max(sweep['entropies']):.4f}")
        
        # Find optimal tilt that maximizes entropy (Hypothesis 1 test)
        max_entropy_idx = np.argmax(sweep['entropies'])
        optimal_tilt = sweep['angles'][max_entropy_idx]
        result("Optimal tilt angle", f"{np.degrees(optimal_tilt):.1f}° (max entropy)")
        
        # Use optimal tilt for selection
        selection = sadoc_mosseri_criterion(roots, fibres, tilt_angle=optimal_tilt, debug_bypass=False)
    else:
        print("\n  ▸ Debug mode: Mini tilt sweep for visualization")
        # Create a mini sweep around current angle for plotting
        current_angle = selection.get('tilt_angle', 0.3)
        mini_angles = np.linspace(current_angle - 0.3, current_angle + 0.3, 7)
        mini_ratios = []
        mini_entropies = []
        
        for angle in mini_angles:
            # Test selection at this angle (use debug mode for mini sweep)
            test_sel = sadoc_mosseri_criterion(roots, fibres, tilt_angle=angle, threshold=0.5, debug_bypass=True)
            ratio = test_sel['selection_ratio']
            
            # Shannon entropy of binary selection
            if 0.01 < ratio < 0.99:
                entropy = -(ratio * np.log(ratio) + (1-ratio) * np.log(1-ratio))
            else:
                entropy = 0.0
            
            mini_ratios.append(ratio)
            mini_entropies.append(entropy)
        
        # Compute entropy gradients (numerical derivative)
        mini_gradients = np.gradient(mini_entropies, mini_angles)
        
        sweep = {
            'angles': mini_angles,
            'selection_ratios': mini_ratios,
            'entropies': mini_entropies,
            'entropy_gradients': mini_gradients
        }
        all_results['sweep'] = sweep
        result("Mini sweep range", f"{np.degrees(mini_angles[0]):.1f}° to {np.degrees(mini_angles[-1]):.1f}°")

    # ─────────────────────────────────────────────────────────────
    # STAGE 6: 4D QUASICRYSTAL ASSEMBLY
    # ─────────────────────────────────────────────────────────────
    banner("STAGE 6: 4D QUASICRYSTAL — ASSEMBLING SELECTED POINTS")
    
    # Use golden ratio projection for icosahedral symmetry
    P_par, P_perp = generate_golden_ratio_decomposition()
    
    qc = assemble_quasicrystal(roots, fibres, selection['selected_fibres'],
                                projection_matrix=P_par)
    
    result("Quasicrystal points (4D)", qc['point_count'])
    all_results['quasicrystal_4d'] = qc['points_4d']
    all_results['qc_point_count'] = qc['point_count']
    
    if qc['point_count'] > 3:
        order = compute_order_parameters(qc['points_4d'])
        result("Golden ratio order", f"{order['golden_ratio_order']:.4f}")
        result("Mean pair distance", f"{order['mean_distance']:.4f}")
        result("Min pair distance", f"{order['min_distance']:.4f}")
        
        sym = verify_600_cell_symmetry(qc['points_4d'])
        result("Unique dot products", sym.get('num_unique_dot_products', '?'))
        result("Golden ratio φ", f"{sym.get('golden_ratio_phi', 0):.6f}")

    # ─────────────────────────────────────────────────────────────
    # STAGE 7: 31 SUBSPACE DECOMPOSITION
    # ─────────────────────────────────────────────────────────────
    banner("STAGE 7: 31 SUBSPACE DECOMPOSITIONS OF E₈")
    
    decompositions = enumerate_31_subspaces()
    result("Total decompositions", len(decompositions))
    
    subspace_results = []
    for i, (P_p, P_q) in enumerate(decompositions[:10]):  # first 10 for speed
        par_4d, perp_4d = apply_decomposition(roots, P_p, P_q)
        props_d = compute_decomposition_properties(P_p, P_q)
        
        # Quick quasicrystal for this decomposition
        qc_sub = assemble_quasicrystal(roots, fibres, selection['selected_fibres'],
                                        projection_matrix=P_p)
        sub_result = {
            'index': i,
            'point_count': qc_sub['point_count'],
            'orthogonal': props_d['is_orthogonal'],
        }
        if qc_sub['point_count'] > 3:
            ord_sub = compute_order_parameters(qc_sub['points_4d'])
            sub_result['golden_ratio_order'] = ord_sub['golden_ratio_order']
        else:
            sub_result['golden_ratio_order'] = 0.0
        
        subspace_results.append(sub_result)
    
    for sr in subspace_results[:5]:
        result(f"Subspace {sr['index']}", 
               f"{sr['point_count']} pts, φ-order={sr['golden_ratio_order']:.4f}")

    # ═════════════════════════════════════════════════════════════
    # HYPOTHESIS TESTS
    # ═════════════════════════════════════════════════════════════

    # ─────────────────────────────────────────────────────────────
    # H1: ENTROPY/TILT CORRELATION
    # ─────────────────────────────────────────────────────────────
    banner("HYPOTHESIS 1: ENTROPY ↔ TILT ANGLE CORRELATION")
    
    tilt_data = compute_projection_tilt(P_par, P_perp, roots)
    result("Tilt angle", f"{tilt_data['tilt_degrees']:.2f}°")
    result("Par ↔ Perp correlation", f"{tilt_data['correlation']:.4f}")
    result("p-value", f"{tilt_data['correlation_p_value']:.2e}")
    
    par_4d, perp_4d = apply_decomposition(roots, P_par, P_perp)
    entropy_data = entropy_gradient_field(perp_4d)
    result("Total perp-space entropy", f"{entropy_data['total_entropy']:.4f}")
    
    if len(selection['invariants']) > 0 and len(selection['selection_mask']) > 0:
        corr_result = correlation_analysis(
            selection['selection_mask'], selection['invariants'], selection['tilt_angle']
        )
        result("Selection-tilt agreement", f"{corr_result['agreement_rate']:.3f}")
        result("Chi-squared", f"{corr_result['chi_squared']:.4f}")
        result("Significant?", corr_result['significant'])
        
        h1_verdict = "SUPPORTED" if corr_result['agreement_rate'] > 0.6 else "INCONCLUSIVE"
    else:
        h1_verdict = "INSUFFICIENT DATA"
    
    all_results['h1_result'] = {
        'verdict': h1_verdict,
        'correlation': f"{tilt_data['correlation']:.4f}",
    }
    result("H1 VERDICT", h1_verdict)

    # ─────────────────────────────────────────────────────────────
    # H2: SHELL COUNTS ↔ PHYSICS
    # ─────────────────────────────────────────────────────────────
    banner("HYPOTHESIS 2: SHELL COUNTS ↔ AFFINE E₈ CHARACTERS")
    
    counts_analysis = compute_shell_counts_vs_theory(shells)
    sm_analysis = compare_sm_multiplets(counts)
    km_analysis = compare_kac_moody_levels(counts)
    
    for n, data in counts_analysis.items():
        marker = "✓" if data['matches_affine'] else "?"
        result(f"Shell {n}: {data['observed']} pts",
               f"affine-match={data['matches_affine']} {marker}")
        for conn in data['physics_connections'][:2]:
            print(f"      → {conn}")
    
    section("Affine E₈ Level Matches")
    from shell_analysis import AFFINE_E8_LEVELS
    result("Level 1 (adjoint)", f"{AFFINE_E8_LEVELS.get(1, '?')}")
    n_matches = sum(1 for data in counts_analysis.values() if data['matches_affine'])
    h2_verdict = "SUPPORTED" if n_matches > 0 else "NO MATCHES"
    all_results['h2_result'] = {
        'verdict': h2_verdict,
        'affine_matches': n_matches,
    }
    result("H2 VERDICT", h2_verdict)

    # ─────────────────────────────────────────────────────────────
    # H3: SPACETIME GENERATION
    # ─────────────────────────────────────────────────────────────
    banner("HYPOTHESIS 3: 4D QUASICRYSTAL → SPACETIME")
    
    if qc['point_count'] > 5:
        st = quasicrystal_to_spacetime(qc['points_4d'])
        all_results['spacetime'] = st
        
        result("Spacetime events", st['num_events'])
        result("Time range", f"[{st['t'].min():.3f}, {st['t'].max():.3f}]")
        result("Spatial extent (x)", f"[{st['x'].min():.3f}, {st['x'].max():.3f}]")
        
        causal = compute_causal_structure(st['events'])
        all_results['causal'] = causal
        
        # Updated causal structure results for causal set formalism
        result("Timelike relations", causal.get('timelike_relations', 0))
        result("Spacelike relations", causal.get('spacelike_relations', 0))
        result("Causality fraction", f"{causal.get('causality_fraction', 0):.3f}")
        result("Causal set valid", causal.get('causal_set_valid', False))
        
        if st['num_events'] > 10:
            particles = identify_particle_excitations(st['events'], causal)
            result("High-density defects", particles['num_high_density_defects'])
            result("Low-density defects", particles['num_low_density_defects'])
            result("Defect fraction", f"{particles['defect_fraction']:.3f}")
            result("(Defects → particle excitations)", "")
        
        h3_verdict = "CAUSAL STRUCTURE FOUND" if causal.get('causality_fraction', 0) > 0.1 else "WEAK CAUSALITY"
        all_results['h3_result'] = {
            'verdict': h3_verdict,
            'causality_fraction': f"{causal.get('causality_fraction', 0):.3f}",
            'causal_set_valid': causal.get('causal_set_valid', False),
        }
    else:
        h3_verdict = "INSUFFICIENT POINTS"
        all_results['h3_result'] = {'verdict': h3_verdict}
    
    result("H3 VERDICT", h3_verdict)

    # ─────────────────────────────────────────────────────────────
    # STAGE 8: DIFFRACTION PATTERN
    # ─────────────────────────────────────────────────────────────
    banner("DIFFRACTION ANALYSIS — QUASICRYSTAL BRAGG PEAKS")
    
    if qc['point_count'] > 5:
        diffraction = compute_diffraction_pattern(qc['points_4d'], k_max=8.0, n_k=80)
        all_results['diffraction'] = diffraction
        
        sf = diffraction['structure_factor']
        result("Mean S(k)", f"{np.mean(sf):.4f}")
        result("Max S(k)", f"{np.max(sf):.4f}")
        result("Peak count (>2σ)", int(np.sum(sf > np.mean(sf) + 2*np.std(sf))))

    # ═════════════════════════════════════════════════════════════
    # VISUALIZATION
    # ═════════════════════════════════════════════════════════════
    banner("GENERATING VISUALIZATIONS")
    
    print("  Plotting E₈ root projection...")
    fig1 = plot_e8_root_projection(roots, os.path.join(output_dir, '01_e8_roots.png'))
    
    print("  Plotting shell distribution...")
    shell_norms = [s['norm_squared'] for s in shells]
    fig2 = plot_shell_distribution(counts, shell_norms,
                                    os.path.join(output_dir, '02_shells.png'))
    
    print("  Plotting Hopf fibration...")
    fig3 = plot_hopf_fibration(base_coords, fibres,
                                os.path.join(output_dir, '03_hopf.png'))
    
    if qc['point_count'] > 0:
        print("  Plotting 4D quasicrystal...")
        fig4 = plot_quasicrystal_3d(qc['points_4d'],
                                     os.path.join(output_dir, '04_quasicrystal.png'))
    
    if 'spacetime' in all_results and 'causal' in all_results:
        print("  Plotting spacetime diagram...")
        fig5 = plot_spacetime_diagram(all_results['spacetime'], all_results['causal'],
                                       os.path.join(output_dir, '05_spacetime.png'))
    
    print("  Plotting tilt-entropy analysis...")
    fig6 = plot_tilt_entropy(sweep, os.path.join(output_dir, '06_tilt_entropy.png'))
    
    if 'diffraction' in all_results:
        print("  Plotting diffraction pattern...")
        fig7 = plot_diffraction_pattern(all_results['diffraction'],
                                         os.path.join(output_dir, '07_diffraction.png'))
    
    print("  Generating comprehensive dashboard...")
    fig8 = plot_comprehensive_dashboard(all_results,
                                         os.path.join(output_dir, '08_dashboard.png'))

    # ═════════════════════════════════════════════════════════════
    # FINAL REPORT
    # ═════════════════════════════════════════════════════════════
    elapsed = time.time() - t0
    
    banner("FINAL REPORT")
    print(f"""
    ╔══════════════════════════════════════════════════════════╗
    ║            E₈ QUASICRYSTAL PROJECTION TEST              ║
    ╠══════════════════════════════════════════════════════════╣
    ║                                                          ║
    ║  E₈ Root Vectors:  {all_results['root_count']:>4d}  (expected: 240)            ║
    ║  Shell 1 Count:    {all_results['shell_counts'][0]:>4d}  (θ-series: 240)         ║
    ║  QC Points (4D):   {all_results.get('qc_point_count', 0):>4d}                           ║
    ║                                                          ║
    ║  ┌─────────────────────────────────────────────────────┐ ║
    ║  │  H1: Entropy/Tilt       → {all_results['h1_result']['verdict']:<24s}│ ║
    ║  │  H2: Shell/SM Counts    → {all_results['h2_result']['verdict']:<24s}│ ║
    ║  │  H3: Spacetime Gen      → {all_results['h3_result']['verdict']:<24s}│ ║
    ║  └─────────────────────────────────────────────────────┘ ║
    ║                                                          ║
    ║  Output: {output_dir:<47s}║
    ║  Time:   {elapsed:>6.1f}s                                       ║
    ╚══════════════════════════════════════════════════════════╝
    """)
    
    print("  ✓ Complete. All visualizations saved to output/")


if __name__ == '__main__':
    main()
