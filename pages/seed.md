<style>
  .page { font-family: 'Segoe UI', Arial, sans-serif; color: #2d3436; max-width: 860px; margin: auto; }
  .hero {
    background: linear-gradient(135deg, #1a1a2e 0%, #16213e 60%, #0f3460 100%);
    border-radius: 12px; padding: 30px 40px; color: white; margin-bottom: 28px;
  }
  .hero h1 { font-size: 1.8em; margin: 0 0 8px 0; }
  .hero p  { margin: 0; opacity: 0.85; font-size: 1.05em; }
  .section h2 {
    font-size: 1.2em; color: #0a3d62; border-left: 4px solid #00b4d8;
    padding-left: 12px; margin: 28px 0 12px 0;
  }
  .idea-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin-bottom: 20px; }
  .idea-card {
    background: #f0f8ff; border: 1px solid #c8e4f5; border-radius: 8px;
    padding: 14px 16px; font-size: 0.9em;
  }
  .idea-card strong { color: #0a3d62; display: block; margin-bottom: 4px; }
  pre {
    background: #1e2a38; color: #abb2bf; border-radius: 10px; padding: 20px;
    overflow-x: auto; font-size: 0.87em; line-height: 1.65; margin: 0;
  }
  .keyword { color: #c678dd; }
  .fn      { color: #61afef; }
  .string  { color: #98c379; }
  .comment { color: #5c6370; font-style: italic; }
  .code-block { border-radius: 10px; overflow: hidden; margin-bottom: 24px; }
  .code-header {
    background: #0a3d62; color: #cdd6f4; padding: 8px 18px;
    font-size: 0.82em; letter-spacing: 0.05em; font-family: monospace;
  }
  .tip {
    background: #e8f8f5; border: 1px solid #a9dfbf; border-radius: 8px;
    padding: 14px 18px; margin-bottom: 12px; font-size: 0.92em;
  }
  .tip strong { color: #1e8449; }
</style>

<div class="page">

<div class="hero">
  <h1>Starter Kit — Seed Submission</h1>
  <p>A working baseline to get you started. Copy, improve, and submit.</p>
</div>

<div class="section">
  <h2>Why feature extraction is needed</h2>
  <p>
    Each crystal in X has a <b>different number of atoms</b>, so X is a ragged array.
    Standard sklearn models require fixed-size inputs — you need to extract a feature vector of constant length from each crystal before fitting.
  </p>
  <div class="idea-grid">
    <div class="idea-card"><strong>Geometric features</strong>Number of atoms, bounding box, centroid distances, spread of positions</div>
    <div class="idea-card"><strong>Chemical features</strong>Atomic numbers Z, element counts, mean / std of Z values</div>
    <div class="idea-card"><strong>Pairwise features</strong>Min / mean / max interatomic distances, coordination statistics</div>
    <div class="idea-card"><strong>Graph / GNN features</strong>Model the crystal as a graph — stronger but more complex</div>
  </div>
</div>

<div class="section">
  <h2>Baseline submission.py</h2>

  <div class="code-block">
    <div class="code-header">submission.py</div>
<pre>
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.pipeline import Pipeline


class RaggedFeatureExtractor(BaseEstimator, TransformerMixin):
    """Extract fixed-size features from variable-size crystal structures."""

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        features = []
        for crystal in X:
            coords = np.array(crystal['coords'])  # (n_atoms, 3)
            Z      = np.array(crystal['Z'])        # (n_atoms,)
            n      = len(coords)

            centroid  = coords.mean(axis=0)
            distances = np.linalg.norm(coords - centroid, axis=1)

            feat = np.concatenate([
                [n],                       # number of atoms
                coords.mean(axis=0),       # center of mass
                coords.std(axis=0),        # positional spread
                [distances.mean(),         # mean dist to centroid
                 distances.std()],         # std dist to centroid
                [Z.mean(), Z.std(),        # atomic number stats
                 Z.min(),  Z.max()],
            ])
            features.append(feat)
        return np.array(features)


def get_model():
    return Pipeline([
        ("features",  RaggedFeatureExtractor()),
        ("regressor", RandomForestRegressor(n_estimators=100, random_state=42)),
    ])
</pre>
  </div>
</div>

<div class="section">
  <h2>Ideas to improve</h2>
  <div class="tip"><strong>Better features:</strong> Add pairwise distance histograms, Coulomb matrices, or element-specific one-hot counts.</div>
  <div class="tip"><strong>Better model:</strong> Try XGBoost, LightGBM, or a neural network on top of the extracted features.</div>
  <div class="tip"><strong>Graph models:</strong> Represent each crystal as a graph (atoms = nodes, bonds = edges) and use a GNN for direct end-to-end learning.</div>
</div>

</div>
