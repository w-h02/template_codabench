import sys
from collections import Counter
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.model_selection import GroupShuffleSplit


def _load_pickle_npy(path):
    """Load .npy saved with a NumPy 2.x pickle in NumPy 1.x environments."""
    created = []
    if 'numpy._core' not in sys.modules:
        sys.modules['numpy._core'] = np.core
        created.append('numpy._core')
    if 'numpy._core.multiarray' not in sys.modules:
        sys.modules['numpy._core.multiarray'] = np.core.multiarray
        created.append('numpy._core.multiarray')
    try:
        arr = np.load(path, allow_pickle=True)
    finally:
        for key in created:
            sys.modules.pop(key, None)
    return arr


def load_raw_data(x_path='X_data_ragged.npy', y_path='y_data.npy'):
    x_path = Path(x_path)
    y_path = Path(y_path)
    X = _load_pickle_npy(x_path)
    y = np.load(y_path, allow_pickle=True).astype(float)
    return X, y


def canonical_formula(structure):
    counts = Counter(map(str, structure['nom']))
    parts = []
    for el in sorted(counts):
        count = counts[el]
        parts.append(f"{el}{count if count > 1 else ''}")
    return ''.join(parts)


def structure_to_feature_dict(structure):
    Z = np.asarray(structure['Z'], dtype=float)
    coords = np.asarray(structure['coords'], dtype=float)
    names = [str(x) for x in structure['nom']]
    n_atoms = len(structure)

    spans = coords.max(axis=0) - coords.min(axis=0)
    centroid = coords.mean(axis=0)
    radii = np.linalg.norm(coords - centroid, axis=1)

    dists = []
    for i in range(n_atoms):
        for j in range(i + 1, n_atoms):
            dists.append(float(np.linalg.norm(coords[i] - coords[j])))
    if dists:
        dists = np.asarray(dists, dtype=float)
        dist_min = float(dists.min())
        dist_mean = float(dists.mean())
        dist_std = float(dists.std())
        dist_max = float(dists.max())
    else:
        dist_min = dist_mean = dist_std = dist_max = 0.0

    counts = Counter(names)
    features = {
        'formula': canonical_formula(structure),
        'n_atoms': float(n_atoms),
        'n_unique_elements': float(len(counts)),
        'z_mean': float(Z.mean()),
        'z_std': float(Z.std()),
        'z_min': float(Z.min()),
        'z_max': float(Z.max()),
        'z_sum': float(Z.sum()),
        'span_x': float(spans[0]),
        'span_y': float(spans[1]),
        'span_z': float(spans[2]),
        'bbox_volume_proxy': float(np.prod(spans)),
        'radius_mean': float(radii.mean()),
        'radius_std': float(radii.std()),
        'radius_max': float(radii.max()),
        'dist_min': dist_min,
        'dist_mean': dist_mean,
        'dist_std': dist_std,
        'dist_max': dist_max,
    }
    return features, counts


def build_feature_table(X, elements=None):
    if elements is None:
        elements = sorted({str(el) for structure in X for el in structure['nom']})
    element_to_idx = {el: i for i, el in enumerate(elements)}

    rows = []
    elem_counts = np.zeros((len(X), len(elements)), dtype=np.float32)
    for row_idx, structure in enumerate(X):
        features, counts = structure_to_feature_dict(structure)
        rows.append(features)
        for el, value in counts.items():
            if el in element_to_idx:
                elem_counts[row_idx, element_to_idx[el]] = float(value)

    df = pd.DataFrame(rows)
    for i, el in enumerate(elements):
        df[f'elem_{el}'] = elem_counts[:, i]
    return df, elements


def get_numeric_feature_columns(df):
    return [
        c for c in df.columns
        if c != 'formula' and pd.api.types.is_numeric_dtype(df[c])
    ]


def make_group_splits(formulas, public_size=0.15, private_size=0.15, random_state=42):
    formulas = np.asarray(formulas)
    dummy_X = np.zeros((len(formulas), 1), dtype=float)
    dummy_y = np.zeros(len(formulas), dtype=float)

    gss_private = GroupShuffleSplit(n_splits=1, test_size=private_size, random_state=random_state)
    train_public_idx, private_idx = next(gss_private.split(dummy_X, dummy_y, groups=formulas))

    remaining_formulas = formulas[train_public_idx]
    public_frac_of_remaining = public_size / (1.0 - private_size)
    gss_public = GroupShuffleSplit(n_splits=1, test_size=public_frac_of_remaining, random_state=random_state)
    train_rel_idx, public_rel_idx = next(
        gss_public.split(
            np.zeros((len(train_public_idx), 1)),
            np.zeros(len(train_public_idx)),
            groups=remaining_formulas,
        )
    )

    train_idx = train_public_idx[train_rel_idx]
    public_idx = train_public_idx[public_rel_idx]
    return train_idx, public_idx, private_idx
