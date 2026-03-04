<style>
  .page { font-family: 'Segoe UI', Arial, sans-serif; color: #2d3436; max-width: 860px; margin: auto; }
  .hero {
    background: linear-gradient(135deg, #0a3d62 0%, #1e6fa5 60%, #00b4d8 100%);
    border-radius: 12px; padding: 36px 40px; color: white; margin-bottom: 32px;
  }
  .hero h1 { font-size: 2em; margin: 0 0 10px 0; }
  .hero p  { font-size: 1.1em; margin: 0; opacity: 0.9; }
  .badge {
    display: inline-block; background: rgba(255,255,255,0.2);
    border: 1px solid rgba(255,255,255,0.4); border-radius: 20px;
    padding: 4px 14px; font-size: 0.85em; margin-top: 14px;
  }
  .section { margin-bottom: 28px; }
  .section h2 {
    font-size: 1.25em; color: #0a3d62; border-left: 4px solid #00b4d8;
    padding-left: 12px; margin-bottom: 14px;
  }
  .card {
    background: #f0f8ff; border: 1px solid #d0e8f5; border-radius: 10px;
    padding: 18px 22px; margin-bottom: 14px;
  }
  .card code { background: #dceefb; padding: 2px 6px; border-radius: 4px; font-size: 0.92em; }
  .steps { counter-reset: step; list-style: none; padding: 0; }
  .steps li {
    counter-increment: step; display: flex; align-items: flex-start;
    gap: 14px; margin-bottom: 14px;
  }
  .steps li::before {
    content: counter(step); min-width: 30px; height: 30px; background: #0a3d62;
    color: white; border-radius: 50%; display: flex; align-items: center;
    justify-content: center; font-weight: bold; flex-shrink: 0;
  }
  .field-table { width: 100%; border-collapse: collapse; margin-top: 10px; }
  .field-table th {
    background: #0a3d62; color: white; padding: 9px 14px; text-align: left; font-size: 0.9em;
  }
  .field-table td { padding: 9px 14px; border-bottom: 1px solid #e0eaf2; font-size: 0.9em; }
  .field-table tr:nth-child(even) td { background: #f5faff; }
  .metric-box {
    background: linear-gradient(135deg, #e8f8f5, #d5f5e3); border: 1px solid #a9dfbf;
    border-radius: 10px; padding: 16px 22px; display: flex; align-items: center; gap: 18px;
  }
  .metric-box .formula {
    font-size: 1.4em; font-weight: bold; color: #1e8449; font-family: monospace;
  }
  pre {
    background: #1e2a38; color: #abb2bf; border-radius: 8px; padding: 18px;
    overflow-x: auto; font-size: 0.88em; line-height: 1.6;
  }
  .note {
    background: #fff8e1; border-left: 4px solid #f39c12; border-radius: 6px;
    padding: 12px 16px; font-size: 0.92em; color: #7d6608;
  }
</style>

<div class="page">

<div class="hero">
  <h1>How to Participate</h1>
  <p>Predict the formation energy of crystal structures using machine learning</p>
  <span class="badge">Regression &nbsp;|&nbsp; MAE (eV/atom) &nbsp;|&nbsp; Scikit-learn API</span>
</div>

<div class="section">
  <h2>Submission format</h2>
  <div class="card">
    Submit a file named <code>submission.py</code> exposing a single function:
<pre>def get_model():
    # Return any scikit-learn compatible model
    return YourModel()</pre>
    The model must implement <code>fit(X_train, y_train)</code> and <code>predict(X_test)</code>.
  </div>
</div>

<div class="section">
  <h2>Data format</h2>
  <p>
    <b>X</b> is a numpy ragged array (loaded with <code>allow_pickle=True</code>).
    Each element represents one crystal — an array of shape <code>(n_atoms,)</code>
    with three named fields:
  </p>
  <table class="field-table">
    <tr><th>Field</th><th>Type</th><th>Description</th></tr>
    <tr><td><code>Z</code></td><td>float</td><td>Atomic number of each atom</td></tr>
    <tr><td><code>coords</code></td><td>array (3,)</td><td>3D position in Ångströms (x, y, z)</td></tr>
    <tr><td><code>nom</code></td><td>str</td><td>Chemical element symbol (e.g. "Fe", "O")</td></tr>
  </table>
  <br>
  <p><b>y</b> is a 1D numpy array of formation energies in <b>eV/atom</b>. Negative = stable material.</p>
  <div class="note">
    Since crystals have a <b>variable number of atoms</b>, you must extract fixed-size features before applying a standard model. See the <b>Seed</b> page for an example.
  </div>
</div>

<div class="section">
  <h2>Evaluation metric</h2>
  <div class="metric-box">
    <div class="formula">MAE = mean( |y_pred − y_true| )</div>
    <div>
      Computed in <b>eV/atom</b> on both the public and private test sets.<br>
      <b>Lower is better.</b> The final ranking uses the private test MAE.
    </div>
  </div>
</div>

<div class="section">
  <h2>Workflow on Codabench</h2>
  <ol class="steps">
    <li>Your <code>submission.py</code> is uploaded to Codabench</li>
    <li>The ingestion program calls <code>get_model()</code>, trains it on <code>X_train / y_train</code></li>
    <li>Predictions are generated on <code>X_test</code> and <code>X_private_test</code></li>
    <li>The scoring program computes MAE against the hidden reference labels</li>
    <li>Your score appears on the leaderboard</li>
  </ol>
</div>

</div>
