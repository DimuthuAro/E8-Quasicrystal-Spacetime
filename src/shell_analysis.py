"""
Shell Count Analyzer
====================
Tests Hypothesis 2: Shell point counts match physical quantities.

Compares observed E₈ shell counts against:
- Standard Model multiplet degeneracies
- E₈ branching rules (248 → subgroups)
- Kac-Moody level densities
"""

import numpy as np


# Standard Model particle content
SM_PARTICLES = {
    'quarks': {'count': 36, 'description': '6 flavors × 3 colors × 2 (particle/anti)'},
    'leptons': {'count': 12, 'description': '6 leptons × 2 (particle/anti)'},
    'gauge_bosons': {'count': 12, 'description': '8 gluons + W± + Z + γ'},
    'higgs': {'count': 4, 'description': 'Complex doublet (4 real dof)'},
    'total': {'count': 64, 'description': 'Total SM degrees of freedom (per generation: ~16)'},
}

# E₈ branching rules
E8_BRANCHING = {
    'E8_adjoint': 248,
    'E8_to_Spin16': {'128s': 128, '120': 120},  # 248 = 120 + 128
    'E8_to_E6xSU3': {'(78,1)': 78, '(1,8)': 8, '(27,3)': 81, '(27bar,3bar)': 81},
    'E8_to_SU5xSU5': {'(24,1)': 24, '(1,24)': 24, '(5,10)': 50, '(5bar,10bar)': 50,
                        '(10,5bar)': 50, '(10bar,5)': 50},
    'E8_to_SO10xU1': {'45': 45, '16': 16, '16bar': 16, '10': 10, '1': 1},
}

# Affine E₈ representation dimensions (first few levels)
AFFINE_E8_LEVELS = {
    1: 248,      # adjoint representation
    2: 3875,     # level 2
    3: 30380,    # level 3
    4: 147250,   # level 4
    5: 516560,   # level 5
    # These are the dimensions of the affine E₈ representations at level k
}


def compute_shell_counts_vs_theory(observed_shells: list) -> dict:
    """Compare observed shell counts with affine E₈ character dimensions."""
    results = {}
    
    for shell in observed_shells:
        n = shell['shell_index']
        count = shell['point_count']
        norm_sq = shell['norm_squared']
        
        # Expected from affine E₈ level dimensions
        expected = AFFINE_E8_LEVELS.get(n, None)
        
        # Physics connections
        connections = []
        
        if count == 248:
            connections.append("248 = dim(E₈ adjoint)")
        if count == 240:
            connections.append("240 = E₈ roots")
        if count in AFFINE_E8_LEVELS.values():
            level = [k for k, v in AFFINE_E8_LEVELS.items() if v == count]
            connections.append(f"Affine E₈ level {level[0]} representation")
        
        results[n] = {
            'observed': count,
            'expected_affine': expected,
            'matches_affine': count == expected if expected else None,
            'norm_squared': norm_sq,
            'physics_connections': connections,
        }
    
    return results


def compare_sm_multiplets(shell_counts: np.ndarray) -> dict:
    """Compare shell structure with Standard Model particle multiplets."""
    
    # SM representation dimensions
    sm_reps = {
        'quark_doublet': 6,     # (3,2,1/6) → 6 dof
        'up_singlet': 3,        # (3,1,2/3) → 3 dof
        'down_singlet': 3,      # (3,1,-1/3) → 3 dof
        'lepton_doublet': 2,    # (1,2,-1/2) → 2 dof
        'electron_singlet': 1,  # (1,1,-1) → 1 dof
        'neutrino_singlet': 1,  # (1,1,0) → 1 dof (if right-handed)
    }
    total_per_gen = sum(sm_reps.values())  # = 16
    
    matches = []
    for i, count in enumerate(shell_counts):
        # Check if count is related to SM numbers
        if count % total_per_gen == 0:
            factor = count // total_per_gen
            matches.append({
                'shell': i + 1,
                'count': int(count),
                'sm_relation': f"{count} = {factor} × {total_per_gen} (generations × SM rep)",
            })
        if count % 3 == 0 and (count // 3) % total_per_gen == 0:
            matches.append({
                'shell': i + 1,
                'count': int(count),
                'sm_relation': f"{count} = 3 × {count//3} (3 generations × {count//3//total_per_gen} × SM)",
            })
    
    return {
        'sm_total_per_generation': total_per_gen,
        'sm_representations': sm_reps,
        'matches': matches,
    }


def compare_kac_moody_levels(shell_counts: np.ndarray) -> dict:
    """Compare with Kac-Moody algebra level densities.
    
    For affine E₈ at level k, the representation dimension grows as:
    d(k) ~ (240/k) × product formula from Weyl-Kac character formula
    """
    results = []
    
    for i, count in enumerate(shell_counts):
        level = i + 1
        # Simplified Kac-Moody prediction (exact formula is complex)
        # For E₈ level 1: d = 248, level 2: higher
        kac_moody_estimate = 240 * (level + 1)  # rough scaling
        
        ratio = count / kac_moody_estimate if kac_moody_estimate > 0 else 0
        
        results.append({
            'level': level,
            'observed': int(count),
            'kac_moody_estimate': kac_moody_estimate,
            'ratio': float(ratio),
        })
    
    return {'level_comparisons': results}


def statistical_significance(observed: np.ndarray, predicted: np.ndarray) -> dict:
    """Compute statistical significance of count matches."""
    if len(observed) == 0 or len(predicted) == 0:
        return {'chi2': 0, 'p_value': 1.0}
    
    # Chi-squared goodness of fit
    mask = predicted > 0
    if np.sum(mask) < 2:
        return {'chi2': 0, 'p_value': 1.0}
    
    obs = observed[mask]
    pred = predicted[mask]
    
    chi2 = np.sum((obs - pred) ** 2 / pred)
    dof = len(obs) - 1
    
    from scipy.stats import chi2 as chi2_dist
    p_value = 1.0 - chi2_dist.cdf(chi2, dof) if dof > 0 else 1.0
    
    return {
        'chi_squared': float(chi2),
        'degrees_of_freedom': dof,
        'p_value': float(p_value),
        'significant': p_value < 0.05,
        'residuals': ((obs - pred) / np.sqrt(pred)).tolist(),
    }
