<style>
  .page { font-family: 'Segoe UI', Arial, sans-serif; color: #2d3436; max-width: 860px; margin: auto; }
  .hero {
    background: linear-gradient(135deg, #0a3d62 0%, #1e6fa5 100%);
    border-radius: 12px; padding: 30px 40px; color: white; margin-bottom: 32px;
  }
  .hero h1 { font-size: 1.8em; margin: 0; }
  .timeline { position: relative; padding-left: 30px; }
  .timeline::before {
    content: ''; position: absolute; left: 14px; top: 0; bottom: 0;
    width: 3px; background: linear-gradient(to bottom, #00b4d8, #1e6fa5);
    border-radius: 2px;
  }
  .phase { position: relative; margin-bottom: 32px; }
  .phase::before {
    content: ''; position: absolute; left: -22px; top: 6px;
    width: 16px; height: 16px; border-radius: 50%;
    background: #00b4d8; border: 3px solid white;
    box-shadow: 0 0 0 3px #00b4d8;
  }
  .phase-card {
    background: white; border: 1px solid #d0e8f5; border-radius: 10px;
    padding: 20px 24px; box-shadow: 0 2px 8px rgba(0,0,0,0.06);
  }
  .phase-card h2 { margin: 0 0 6px 0; font-size: 1.15em; color: #0a3d62; }
  .date-badge {
    display: inline-block; background: #e8f4fd; color: #1e6fa5;
    border: 1px solid #bee3f8; border-radius: 20px; padding: 3px 12px;
    font-size: 0.82em; font-weight: 600; margin-bottom: 12px;
  }
  .phase-card p { margin: 0; font-size: 0.95em; line-height: 1.6; color: #555; }
  .phase-card ul { margin: 10px 0 0 0; padding-left: 18px; font-size: 0.93em; color: #444; }
  .phase-card li { margin-bottom: 5px; }
  .final .phase::before { background: #e67e22; box-shadow: 0 0 0 3px #e67e22; }
  .final .date-badge { background: #fef9e7; color: #b7770d; border-color: #f9e4a0; }
  .final .phase-card h2 { color: #7d4e1b; }
</style>

<div class="page">

<div class="hero">
  <h1>Competition Timeline</h1>
</div>

<div class="timeline">

  <div class="phase">
    <div class="phase-card">
      <h2>Development Phase</h2>
      <span class="date-badge">March 8, 2026 — March 31, 2026</span>
      <p>Explore the data, experiment with models, and tune your hyperparameters.</p>
      <ul>
        <li>Train on <b>X_train / y_train</b> (80% of the data)</li>
        <li>Predictions evaluated on the <b>public test set</b> (10%)</li>
        <li>Unlimited submissions — leaderboard visible to all</li>
        <li>Use the starting kit notebook to get started quickly</li>
      </ul>
    </div>
  </div>

  <div class="phase final">
    <div class="phase-card">
      <h2>Final Evaluation (Private Test)</h2>
      <span class="date-badge">Automatic — after March 31, 2026</span>
      <p>
        At the close of the development phase, your <b>best submission</b> is automatically
        re-evaluated on the <b>private test set</b> (10% of the data, unseen during development).
        This score determines the <b>final ranking</b>.
      </p>
      <ul>
        <li>No action needed — evaluation is automatic</li>
        <li>Private test set is never visible to participants</li>
        <li>Final MAE score determines the leaderboard</li>
      </ul>
    </div>
  </div>

</div>
</div>
