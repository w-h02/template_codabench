# Seed (starter example)

Below is a minimal `submission.py` using a Random Forest as a baseline.
Since X is a **ragged array** (each crystal has a different number of atoms), fixed-size features must be extracted before applying a standard model.

```python
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.pipeline import Pipeline


class RaggedFeatureExtractor(BaseEstimator, TransformerMixin):
    """Extracts fixed-size features from variable-size crystal structures."""

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        features = []
        for crystal in X:
            crystal = np.array(crystal)  # (n_atoms, 3)
            feat = np.concatenate([
                [len(crystal)],                              # number of atoms
                crystal.mean(axis=0),                        # center of mass
                crystal.std(axis=0),                         # spread
                crystal.min(axis=0),                         # min bounds
                crystal.max(axis=0),                         # max bounds
                crystal.max(axis=0) - crystal.min(axis=0),  # bounding box size
            ])
            features.append(feat)
        return np.array(features)


def get_model():
    return Pipeline([
        ("features", RaggedFeatureExtractor()),
        ("regressor", RandomForestRegressor(n_estimators=100, random_state=42)),
    ])
```
