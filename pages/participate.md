# How to participate

## Objective

Submit a `submission.py` file containing a `get_model()` function that returns a scikit-learn compatible model. The model will be automatically trained and evaluated on crystal structures.

## Data format

- **X**: numpy ragged array (loaded with `allow_pickle=True`) — each element is an array of shape `(n_atoms, 3)` containing the 3D atomic positions of a crystal (variable number of atoms per crystal)
- **y**: 1D numpy array containing the formation energy in **eV/atom** (negative values = stable material)

## Submission format

Your `submission.py` must expose a `get_model()` function:

```python
def get_model():
    # Returns a scikit-learn compatible model (fit / predict)
    return YourModel()
```

The model must implement:
- `model.fit(X_train, y_train)` — training
- `model.predict(X_test)` — predicting formation energies

## Evaluation metric

Performance is measured by **MAE (Mean Absolute Error)** in eV/atom. A lower score is better.

See the "Seed" page for a working starter example.
