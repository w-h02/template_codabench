# Comment participer

## Objectif

Soumettez un fichier `submission.py` contenant une fonction `get_model()` qui retourne un modèle compatible avec l'API scikit-learn. Le modèle sera entraîné et évalué automatiquement sur les structures cristallines.

## Format des données

- **X** : tableau numpy ragged (allow_pickle=True) — chaque élément est un array de forme `(n_atomes, 3)` contenant les positions 3D des atomes d'un cristal (nombre d'atomes variable selon le cristal)
- **y** : tableau numpy 1D contenant l'énergie de formation en **eV/atome** (valeurs négatives = matériau stable)

## Format de soumission

Votre fichier `submission.py` doit exposer une fonction `get_model()` :

```python
def get_model():
    # Retourne un modèle compatible scikit-learn (fit / predict)
    return VotreModele()
```

Le modèle doit implémenter :
- `model.fit(X_train, y_train)` — entraînement
- `model.predict(X_test)` — prédiction des énergies de formation

## Métrique d'évaluation

La performance est mesurée par la **MAE (Mean Absolute Error)** en eV/atome. Un score plus bas est meilleur.

Voir la page "Seed" pour un exemple de point de départ.
