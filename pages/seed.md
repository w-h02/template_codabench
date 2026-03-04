# Seed (point de départ)

Voici un exemple minimal de `submission.py` utilisant un Random Forest comme baseline.
Les données X sont des **ragged arrays** : chaque cristal a un nombre d'atomes différent, donc il faut extraire des features de taille fixe avant d'appliquer un modèle classique.

```python
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.pipeline import Pipeline


class RaggedFeatureExtractor(BaseEstimator, TransformerMixin):
    """Extrait des features de taille fixe depuis les structures cristallines."""

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        features = []
        for crystal in X:
            crystal = np.array(crystal)  # (n_atoms, 3)
            feat = np.concatenate([
                [len(crystal)],              # nombre d'atomes
                crystal.mean(axis=0),        # centre de masse
                crystal.std(axis=0),         # dispersion
                crystal.min(axis=0),         # bornes min
                crystal.max(axis=0),         # bornes max
                crystal.max(axis=0) - crystal.min(axis=0),  # taille de la boîte
            ])
            features.append(feat)
        return np.array(features)


def get_model():
    return Pipeline([
        ("features", RaggedFeatureExtractor()),
        ("regressor", RandomForestRegressor(n_estimators=100, random_state=42)),
    ])
```
