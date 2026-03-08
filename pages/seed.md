<div style="font-family: 'Segoe UI', Arial, sans-serif; color: #2d3436; max-width: 900px; margin: auto; line-height: 1.7;">

<!-- LOGOS -->
<div style="text-align: center;">
    <a href="https://www.hi-paris.fr/">
        <img border="0" src="https://www.hi-paris.fr/wp-content/uploads/2020/09/logo-hi-paris-retina.png" width="25%"></a>
    <a href="https://www.dataia.eu/">
        <img border="0" src="https://github.com/ramp-kits/template-kit/raw/main/img/DATAIA-h.png" width="70%"></a>
</div>

<!-- WELCOME -->
<div style="font-size: 1.01em; color: #2d3436; margin-bottom: 32px; padding: 0 4px;">
  This page provides a <strong>fully functional starter kit</strong> to get you up and running immediately.
  The baseline submission below is designed to help you understand the data format and submission pipeline —
  copy it, experiment, and improve.
</div>

<!-- OVERVIEW -->
<h2 style="font-size: 1.45em; font-weight: 700; color: #111; border-bottom: 2px solid #e0eaf2; padding-bottom: 6px; margin: 36px 0 16px 0;">Overview</h2>

<p style="margin: 0 0 14px 0; font-size: 0.98em; color: #3a3a3a;">
  The key challenge of this competition is that crystal structures have a <strong>variable number of atoms</strong>.
  Standard machine learning models (sklearn, XGBoost, neural networks with fixed input layers) require
  vectors of constant size. You therefore need to <strong>extract fixed-size features</strong> from each
  crystal before fitting any model.
</p>
<p style="margin: 0 0 14px 0; font-size: 0.98em; color: #3a3a3a;">
  The baseline below implements a simple hand-crafted feature extractor using geometric and chemical
  statistics. It is intentionally simple — a strong starting point to understand the pipeline
  before exploring more powerful approaches.
</p>

<!-- CONTEXT -->
<h2 style="font-size: 1.45em; font-weight: 700; color: #111; border-bottom: 2px solid #e0eaf2; padding-bottom: 6px; margin: 36px 0 16px 0;">Context — Why feature extraction?</h2>

<p style="margin: 0 0 14px 0; font-size: 0.98em; color: #3a3a3a;">
  Each crystal in <code style="background: #dceefb; padding: 1px 5px; border-radius: 3px;">X</code> is an array of shape <code style="background: #dceefb; padding: 1px 5px; border-radius: 3px;">(n_atoms,)</code> — the number of atoms
  varies from structure to structure. A crystal with 4 atoms and another with 128 atoms cannot be fed
  directly into the same model without first summarizing them into a common representation.
</p>

<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin: 16px 0;">
  <div style="background: #f8fbff; border: 1px solid #d0e4f5; border-radius: 8px; padding: 14px 16px; font-size: 0.92em;">
    <strong style="color: #0a3d62; display: block; margin-bottom: 4px;">Geometric features</strong>
    Number of atoms, centroid, bounding box, mean distance to center, positional spread
  </div>
  <div style="background: #f8fbff; border: 1px solid #d0e4f5; border-radius: 8px; padding: 14px 16px; font-size: 0.92em;">
    <strong style="color: #0a3d62; display: block; margin-bottom: 4px;">Chemical features</strong>
    Mean and std of atomic number Z, element counts, electronegativity statistics
  </div>
  <div style="background: #f8fbff; border: 1px solid #d0e4f5; border-radius: 8px; padding: 14px 16px; font-size: 0.92em;">
    <strong style="color: #0a3d62; display: block; margin-bottom: 4px;">Pairwise features</strong>
    Min / mean / max interatomic distances, coordination numbers, radial distribution
  </div>
  <div style="background: #f8fbff; border: 1px solid #d0e4f5; border-radius: 8px; padding: 14px 16px; font-size: 0.92em;">
    <strong style="color: #0a3d62; display: block; margin-bottom: 4px;">Graph / GNN features</strong>
    Model the crystal as a graph (atoms = nodes, bonds = edges) — end-to-end learning
  </div>
</div>

<!-- IDEAS TO IMPROVE -->
<h2 style="font-size: 1.45em; font-weight: 700; color: #111; border-bottom: 2px solid #e0eaf2; padding-bottom: 6px; margin: 36px 0 16px 0;">Structure — Ideas to improve</h2>

<div style="background: #f0fdf4; border: 1px solid #a9dfbf; border-radius: 8px; padding: 14px 18px; margin-bottom: 12px; font-size: 0.94em; display: flex; gap: 12px; align-items: flex-start;">
  <span style="font-size: 1.1em; flex-shrink: 0; margin-top: 2px; color: #1e8449; font-weight: bold;">+</span>
  <div><strong style="color: #1e8449;">Better features:</strong> Add pairwise distance histograms, Coulomb matrix eigenvalues,
  or element-specific one-hot counts. The Coulomb matrix [1] is a well-known fixed-size representation
  of molecular geometry.</div>
</div>
<div style="background: #f0fdf4; border: 1px solid #a9dfbf; border-radius: 8px; padding: 14px 18px; margin-bottom: 12px; font-size: 0.94em; display: flex; gap: 12px; align-items: flex-start;">
  <span style="font-size: 1.1em; flex-shrink: 0; margin-top: 2px; color: #1e8449; font-weight: bold;">+</span>
  <div><strong style="color: #1e8449;">Better model:</strong> Try XGBoost, LightGBM, or a multi-layer neural network on top of
  your hand-crafted features. These often outperform Random Forests on tabular chemistry data.</div>
</div>
<div style="background: #f0fdf4; border: 1px solid #a9dfbf; border-radius: 8px; padding: 14px 18px; margin-bottom: 12px; font-size: 0.94em; display: flex; gap: 12px; align-items: flex-start;">
  <span style="font-size: 1.1em; flex-shrink: 0; margin-top: 2px; color: #1e8449; font-weight: bold;">+</span>
  <div><strong style="color: #1e8449;">Graph models:</strong> Represent each crystal as a graph where atoms are nodes and
  bonds/neighbors are edges. Graph Neural Networks (GNNs) such as MEGNet [2] or CGCNN [3] are
  state-of-the-art for crystal property prediction.</div>
</div>

<div style="background: #fff8e1; border-left: 4px solid #f39c12; border-radius: 6px; padding: 12px 16px; font-size: 0.92em; color: #7d6608; margin: 12px 0;">
  <strong>Tip:</strong> The scoring is based solely on the output of <code style="background: #ffe8a0; padding: 1px 5px; border-radius: 3px;">get_model()</code>.
  You can import any library available in the environment. The model is trained and tested
  automatically by the ingestion program — no need to handle train/test splitting yourself.
</div>

</div>
