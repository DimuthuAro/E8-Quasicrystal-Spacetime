"""
Visualization Suite
===================
Publication-quality figures for E₈ quasicrystal analysis.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.cm as cm


def setup_style():
    """Set up dark sci-fi plot style."""
    plt.style.use('dark_background')
    plt.rcParams.update({
        'figure.facecolor': '#0a0a1a',
        'axes.facecolor': '#0a0a1a',
        'savefig.facecolor': '#0a0a1a',
        'text.color': '#00ffaa',
        'axes.labelcolor': '#00ffaa',
        'xtick.color': '#00ccff',
        'ytick.color': '#00ccff',
        'axes.edgecolor': '#333366',
        'grid.color': '#1a1a3a',
        'font.family': 'monospace',
        'font.size': 10,
    })


def plot_e8_root_projection(roots: np.ndarray, save_path: str = None):
    """Project 240 E₈ roots to 3D and plot."""
    setup_style()
    fig = plt.figure(figsize=(14, 10))
    ax = fig.add_subplot(111, projection='3d')
    
    pts = roots[:, :3]
    norms = np.linalg.norm(roots, axis=1)
    colors = cm.plasma(Normalize()(roots[:, 3]))
    
    ax.scatter(pts[:, 0], pts[:, 1], pts[:, 2],
               c=colors, s=25, alpha=0.8, edgecolors='white', linewidths=0.3)
    
    ax.set_title('E₈ ROOT SYSTEM — 240 Vectors Projected to 3D',
                 fontsize=14, color='#00ffaa', pad=20)
    ax.set_xlabel('x₁')
    ax.set_ylabel('x₂')
    ax.set_zlabel('x₃')
    
    if save_path:
        plt.savefig(save_path, dpi=200, bbox_inches='tight')
    return fig


def plot_shell_distribution(shell_counts: np.ndarray, shell_norms: list,
                             save_path: str = None):
    """Bar chart of shell populations with theta series comparison."""
    setup_style()
    fig, ax = plt.subplots(figsize=(12, 6))
    
    n_shells = len(shell_counts)
    x = np.arange(n_shells)
    
    bars = ax.bar(x, shell_counts, color='#00ccff', alpha=0.8, edgecolor='#00ffaa',
                  linewidth=1.5, label='Observed')
    
    # Add count labels
    for bar, count in zip(bars, shell_counts):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 50,
                str(int(count)), ha='center', va='bottom', fontsize=9,
                color='#ffaa00', fontweight='bold')
    
    ax.set_xlabel('Shell Index (norm²)')
    ax.set_ylabel('Point Count')
    ax.set_title('E₈ LATTICE SHELL STRUCTURE', fontsize=14, color='#00ffaa')
    ax.set_xticks(x)
    ax.set_xticklabels([f'n²={n:.0f}' for n in shell_norms], rotation=45)
    ax.legend()
    
    if save_path:
        plt.savefig(save_path, dpi=200, bbox_inches='tight')
    return fig


def plot_hopf_fibration(base_coords: np.ndarray, fibre_indices: list,
                         save_path: str = None):
    """Visualize Hopf fibration base space with fibre coloring."""
    setup_style()
    fig = plt.figure(figsize=(14, 10))
    ax = fig.add_subplot(111, projection='3d')
    
    # Color by fibre index
    colors_all = np.zeros(len(base_coords))
    for i, indices in enumerate(fibre_indices):
        colors_all[indices] = i
    
    pts = base_coords[:, :3] if base_coords.shape[1] > 3 else base_coords
    
    sc = ax.scatter(pts[:, 0], pts[:, 1], pts[:, 2],
                    c=colors_all, cmap='hsv', s=15, alpha=0.7)
    
    ax.set_title('HOPF FIBRATION S⁷ → S⁴ — Fibre Structure',
                 fontsize=14, color='#00ffaa', pad=20)
    plt.colorbar(sc, ax=ax, label='Fibre Index', shrink=0.6)
    
    if save_path:
        plt.savefig(save_path, dpi=200, bbox_inches='tight')
    return fig


def plot_quasicrystal_3d(points_4d: np.ndarray, save_path: str = None):
    """Project 4D quasicrystal to 3D and plot."""
    setup_style()
    fig = plt.figure(figsize=(14, 10))
    ax = fig.add_subplot(111, projection='3d')
    
    pts = points_4d[:, :3]
    color_by = points_4d[:, 3] if points_4d.shape[1] > 3 else np.zeros(len(points_4d))
    
    sc = ax.scatter(pts[:, 0], pts[:, 1], pts[:, 2],
                    c=color_by, cmap='coolwarm', s=20, alpha=0.8,
                    edgecolors='white', linewidths=0.2)
    
    ax.set_title('4D QUASICRYSTAL — Projected to 3D\n(Color = 4th dimension)',
                 fontsize=14, color='#00ffaa', pad=20)
    plt.colorbar(sc, ax=ax, label='x₄ coordinate', shrink=0.6)
    
    if save_path:
        plt.savefig(save_path, dpi=200, bbox_inches='tight')
    return fig


def plot_spacetime_diagram(events: dict, causal: dict, save_path: str = None):
    """Plot spacetime diagram with light cones and causal connections."""
    setup_style()
    fig, axes = plt.subplots(1, 3, figsize=(20, 6))
    
    t = events['t']
    x = events['x']
    y = events['y']
    z = events['z']
    
    # (t, x) diagram
    ax = axes[0]
    ax.scatter(x, t, c='#00ccff', s=8, alpha=0.6, zorder=5)
    # Draw light cone from origin
    t_range = np.linspace(min(t), max(t), 100)
    ax.plot(t_range, t_range, '--', color='#ffaa00', alpha=0.5, label='Light cone')
    ax.plot(-t_range, t_range, '--', color='#ffaa00', alpha=0.5)
    ax.set_xlabel('x')
    ax.set_ylabel('t')
    ax.set_title('SPACETIME (t vs x)', color='#00ffaa')
    ax.legend(fontsize=8)
    
    # (t, y) diagram
    ax = axes[1]
    ax.scatter(y, t, c='#ff6600', s=8, alpha=0.6, zorder=5)
    ax.plot(t_range, t_range, '--', color='#ffaa00', alpha=0.5)
    ax.plot(-t_range, t_range, '--', color='#ffaa00', alpha=0.5)
    ax.set_xlabel('y')
    ax.set_ylabel('t')
    ax.set_title('SPACETIME (t vs y)', color='#00ffaa')
    
    # Causal structure pie chart
    ax = axes[2]
    if 'timelike_pairs' in causal:
        sizes = [causal['timelike_pairs'], causal['spacelike_pairs'], causal['lightlike_pairs']]
        labels = [f"Timelike\n{causal['timelike_pairs']}", 
                  f"Spacelike\n{causal['spacelike_pairs']}",
                  f"Lightlike\n{causal['lightlike_pairs']}"]
        colors_pie = ['#ff3366', '#3366ff', '#ffcc00']
        # Remove zero-size wedges
        non_zero = [(s, l, c) for s, l, c in zip(sizes, labels, colors_pie) if s > 0]
        if non_zero:
            sizes, labels, colors_pie = zip(*non_zero)
            ax.pie(sizes, labels=labels, colors=colors_pie, autopct='%1.1f%%',
                   textprops={'color': 'white', 'fontsize': 9})
    ax.set_title('CAUSAL STRUCTURE', color='#00ffaa')
    
    plt.suptitle('DISCRETE SPACETIME FROM E₈ QUASICRYSTAL', 
                 fontsize=16, color='#00ffaa', y=1.02)
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=200, bbox_inches='tight')
    return fig


def plot_tilt_entropy(sweep_data: dict, save_path: str = None):
    """Plot tilt angle vs selection ratio and entropy."""
    setup_style()
    fig, axes = plt.subplots(1, 3, figsize=(18, 5))
    
    angles = np.degrees(sweep_data['angles'])
    
    # Selection ratio vs tilt
    ax = axes[0]
    ax.plot(angles, sweep_data['selection_ratios'], color='#00ccff', linewidth=2)
    ax.axhline(0.5, color='#ffaa00', linestyle='--', alpha=0.5, label='50%')
    ax.set_xlabel('Tilt Angle (degrees)')
    ax.set_ylabel('Selection Ratio')
    ax.set_title('FIBRE SELECTION vs TILT', color='#00ffaa')
    ax.legend()
    
    # Entropy vs tilt
    ax = axes[1]
    ax.plot(angles, sweep_data['entropies'], color='#ff6600', linewidth=2)
    ax.set_xlabel('Tilt Angle (degrees)')
    ax.set_ylabel('Shannon Entropy')
    ax.set_title('ENTROPY vs TILT', color='#00ffaa')
    
    # Entropy gradient
    ax = axes[2]
    ax.plot(angles, sweep_data['entropy_gradients'], color='#cc00ff', linewidth=2)
    ax.axhline(0, color='#ffaa00', linestyle='--', alpha=0.5)
    ax.set_xlabel('Tilt Angle (degrees)')
    ax.set_ylabel('dS/dθ')
    ax.set_title('ENTROPY GRADIENT', color='#00ffaa')
    
    plt.suptitle('HYPOTHESIS 1: ENTROPY/CAUSALITY GRADIENT',
                 fontsize=14, color='#00ffaa', y=1.02)
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=200, bbox_inches='tight')
    return fig


def plot_diffraction_pattern(diffraction: dict, save_path: str = None):
    """Plot structure factor S(k) — quasicrystal diffraction."""
    setup_style()
    fig, ax = plt.subplots(figsize=(12, 6))
    
    ax.plot(diffraction['k_values'], diffraction['structure_factor'],
            color='#00ffaa', linewidth=1.5)
    ax.fill_between(diffraction['k_values'], 0, diffraction['structure_factor'],
                    alpha=0.3, color='#00ccff')
    
    # Mark prominent peaks
    sf = diffraction['structure_factor']
    threshold = np.mean(sf) + 2 * np.std(sf)
    peaks = diffraction['k_values'][sf > threshold]
    peak_vals = sf[sf > threshold]
    ax.scatter(peaks, peak_vals, color='#ff3366', s=50, zorder=5, label='Bragg peaks')
    
    ax.set_xlabel('|k| (wavevector)')
    ax.set_ylabel('S(k) (structure factor)')
    ax.set_title('QUASICRYSTAL DIFFRACTION PATTERN', fontsize=14, color='#00ffaa')
    ax.legend()
    
    if save_path:
        plt.savefig(save_path, dpi=200, bbox_inches='tight')
    return fig


def plot_31_subspace_comparison(results: list, save_path: str = None):
    """Compare quasicrystal properties across 31 subspace decompositions."""
    setup_style()
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    
    point_counts = [r['point_count'] for r in results]
    golden_orders = [r.get('golden_ratio_order', 0) for r in results]
    
    ax = axes[0]
    ax.bar(range(len(point_counts)), point_counts, color='#00ccff', alpha=0.8)
    ax.set_xlabel('Subspace Index')
    ax.set_ylabel('Quasicrystal Points')
    ax.set_title('POINTS per SUBSPACE', color='#00ffaa')
    
    ax = axes[1]
    ax.bar(range(len(golden_orders)), golden_orders, color='#ff6600', alpha=0.8)
    ax.set_xlabel('Subspace Index')
    ax.set_ylabel('Golden Ratio Order')
    ax.set_title('ICOSAHEDRAL ORDER per SUBSPACE', color='#00ffaa')
    
    plt.suptitle('31 SUBSPACE DECOMPOSITIONS OF E₈',
                 fontsize=14, color='#00ffaa', y=1.02)
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=200, bbox_inches='tight')
    return fig


def plot_comprehensive_dashboard(all_results: dict, save_path: str = None):
    """Generate a comprehensive dashboard of all results."""
    setup_style()
    fig = plt.figure(figsize=(24, 16))
    
    # Title
    fig.suptitle('E₈ QUASICRYSTAL PROJECTION — THEORY OF EVERYTHING TEST',
                 fontsize=20, color='#00ffaa', y=0.98, fontweight='bold')
    
    gs = fig.add_gridspec(3, 4, hspace=0.35, wspace=0.3)
    
    # 1. E₈ roots 3D
    ax = fig.add_subplot(gs[0, 0], projection='3d')
    roots = all_results.get('roots', np.zeros((1, 8)))
    pts = roots[:, :3]
    ax.scatter(pts[:, 0], pts[:, 1], pts[:, 2], c=roots[:, 3],
               cmap='plasma', s=5, alpha=0.8)
    ax.set_title('E₈ Roots (3D proj)', fontsize=9, color='#00ffaa')
    
    # 2. Shell counts
    ax = fig.add_subplot(gs[0, 1])
    shells = all_results.get('shell_counts', [240])
    ax.bar(range(len(shells)), shells, color='#00ccff', alpha=0.8)
    ax.set_title('Shell Populations', fontsize=9, color='#00ffaa')
    ax.set_xlabel('Shell')
    
    # 3. Selection ratio vs tilt
    ax = fig.add_subplot(gs[0, 2])
    if 'sweep' in all_results:
        sweep = all_results['sweep']
        ax.plot(np.degrees(sweep['angles']), sweep['selection_ratios'],
                color='#00ccff', linewidth=1.5)
        ax.set_title('Selection vs Tilt', fontsize=9, color='#00ffaa')
        ax.set_xlabel('Tilt (°)')
    
    # 4. Entropy
    ax = fig.add_subplot(gs[0, 3])
    if 'sweep' in all_results:
        ax.plot(np.degrees(sweep['angles']), sweep['entropies'],
                color='#ff6600', linewidth=1.5)
        ax.set_title('Entropy vs Tilt', fontsize=9, color='#00ffaa')
        ax.set_xlabel('Tilt (°)')
    
    # 5. Quasicrystal 3D
    ax = fig.add_subplot(gs[1, 0:2], projection='3d')
    qc = all_results.get('quasicrystal_4d', np.zeros((1, 4)))
    if len(qc) > 0:
        ax.scatter(qc[:, 0], qc[:, 1], qc[:, 2], c=qc[:, 3] if qc.shape[1]>3 else 'cyan',
                   cmap='coolwarm', s=10, alpha=0.7)
    ax.set_title('4D Quasicrystal (3D proj)', fontsize=9, color='#00ffaa')
    
    # 6. Spacetime diagram
    ax = fig.add_subplot(gs[1, 2])
    if 'spacetime' in all_results:
        st = all_results['spacetime']
        ax.scatter(st['x'], st['t'], c='#00ccff', s=3, alpha=0.5)
        t_r = np.linspace(min(st['t']), max(st['t']), 50)
        ax.plot(t_r, t_r, '--', color='#ffaa00', alpha=0.4)
        ax.plot(-t_r, t_r, '--', color='#ffaa00', alpha=0.4)
        ax.set_xlabel('x')
        ax.set_ylabel('t')
    ax.set_title('Spacetime (t vs x)', fontsize=9, color='#00ffaa')
    
    # 7. Causal structure
    ax = fig.add_subplot(gs[1, 3])
    if 'causal' in all_results:
        c = all_results['causal']
        vals = [c.get('timelike_pairs', 0), c.get('spacelike_pairs', 0)]
        labels = ['Timelike', 'Spacelike']
        colors_pie = ['#ff3366', '#3366ff']
        non_zero = [(v, l, c_) for v, l, c_ in zip(vals, labels, colors_pie) if v > 0]
        if non_zero:
            v, l, c_ = zip(*non_zero)
            ax.pie(v, labels=l, colors=c_, autopct='%1.0f%%',
                   textprops={'color': 'white', 'fontsize': 8})
    ax.set_title('Causal Structure', fontsize=9, color='#00ffaa')
    
    # 8. Diffraction pattern
    ax = fig.add_subplot(gs[2, 0:2])
    if 'diffraction' in all_results:
        d = all_results['diffraction']
        ax.plot(d['k_values'], d['structure_factor'], color='#00ffaa', linewidth=1)
        ax.fill_between(d['k_values'], 0, d['structure_factor'], alpha=0.2, color='#00ccff')
    ax.set_title('Diffraction Pattern S(k)', fontsize=9, color='#00ffaa')
    ax.set_xlabel('|k|')
    
    # 9. Physics summary text
    ax = fig.add_subplot(gs[2, 2:4])
    ax.axis('off')
    summary_text = _build_summary_text(all_results)
    ax.text(0.05, 0.95, summary_text, transform=ax.transAxes, fontsize=8,
            verticalalignment='top', color='#00ffaa', fontfamily='monospace',
            bbox=dict(boxstyle='round', facecolor='#0a0a2a', edgecolor='#333366'))
    ax.set_title('PHYSICS SUMMARY', fontsize=9, color='#00ffaa')
    
    if save_path:
        plt.savefig(save_path, dpi=200, bbox_inches='tight')
    return fig


def _build_summary_text(results: dict) -> str:
    """Build summary text for dashboard."""
    lines = [
        "═══════════════════════════════════════",
        "  E₈ QUASICRYSTAL → THEORY OF EVERYTHING",
        "═══════════════════════════════════════",
        "",
        f"  E₈ Root Vectors: {results.get('root_count', '?')}",
        f"  Shell 1 Count:   {results.get('shell_counts', [0])[0]}",
        f"  QC Points (4D):  {results.get('qc_point_count', '?')}",
        "",
        "  HYPOTHESIS TESTS:",
        "  ─────────────────",
    ]
    
    # H1
    h1 = results.get('h1_result', {})
    lines.append(f"  H1 (Entropy/Tilt):  {h1.get('verdict', 'PENDING')}")
    lines.append(f"      Correlation:    {h1.get('correlation', '?')}")
    
    # H2
    h2 = results.get('h2_result', {})
    lines.append(f"  H2 (Shell Counts):  {h2.get('verdict', 'PENDING')}")
    lines.append(f"      SM matches:     {h2.get('sm_matches', '?')}")
    
    # H3
    h3 = results.get('h3_result', {})
    lines.append(f"  H3 (Spacetime):     {h3.get('verdict', 'PENDING')}")
    lines.append(f"      Timelike frac:  {h3.get('timelike_fraction', '?')}")
    lines.append(f"      Causal depth:   {h3.get('causal_depth', '?')}")
    
    lines.extend([
        "",
        "  ═══════════════════════════════════════",
        "  'The universe is an E₈ quasicrystal'",
        "  ═══════════════════════════════════════",
    ])
    
    return '\n'.join(lines)
