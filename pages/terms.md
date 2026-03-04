<style>
  .page { font-family: 'Segoe UI', Arial, sans-serif; color: #2d3436; max-width: 860px; margin: auto; }
  .hero {
    background: linear-gradient(135deg, #2c3e50 0%, #3d5a80 100%);
    border-radius: 12px; padding: 30px 40px; color: white; margin-bottom: 28px;
  }
  .hero h1 { font-size: 1.8em; margin: 0; }
  .section { margin-bottom: 24px; }
  .section h2 {
    font-size: 1.1em; color: #2c3e50; border-left: 4px solid #3d5a80;
    padding-left: 12px; margin-bottom: 12px;
  }
  .rule-list { list-style: none; padding: 0; margin: 0; }
  .rule-list li {
    padding: 10px 14px 10px 42px; position: relative;
    border-bottom: 1px solid #eaecef; font-size: 0.94em; color: #444; line-height: 1.5;
  }
  .rule-list li:last-child { border-bottom: none; }
  .rule-list li::before {
    content: '✓'; position: absolute; left: 14px; color: #27ae60; font-weight: bold;
  }
  .rule-list.strict li::before { content: '✗'; color: #e74c3c; }
  .card {
    background: #f8f9fa; border: 1px solid #dee2e6; border-radius: 10px;
    overflow: hidden;
  }
</style>

<div class="page">

<div class="hero">
  <h1>Terms and Conditions</h1>
</div>

<div class="section">
  <h2>General rules</h2>
  <div class="card">
    <ul class="rule-list">
      <li>Participation is open to all registered users.</li>
      <li>Each participant must submit their own original code.</li>
      <li>Organizers reserve the right to review the code of top submissions.</li>
    </ul>
  </div>
</div>

<div class="section">
  <h2>Prohibited</h2>
  <div class="card">
    <ul class="rule-list strict">
      <li>Plagiarism or code sharing between competing teams — results in disqualification.</li>
      <li>Use of undeclared external data sources.</li>
      <li>Manual labeling or lookup of test samples.</li>
    </ul>
  </div>
</div>

<div class="section">
  <h2>Data usage</h2>
  <div class="card">
    <ul class="rule-list">
      <li>The provided data (crystal structures and formation energies) is sourced from the <a href="https://next-gen.materialsproject.org/api" target="_blank">Materials Project API</a>.</li>
      <li>Data is provided exclusively for use in this competition.</li>
      <li>Redistribution of the dataset is not permitted.</li>
    </ul>
  </div>
</div>

<div class="section">
  <h2>Evaluation & ranking</h2>
  <div class="card">
    <ul class="rule-list">
      <li>The final ranking is based on MAE (Mean Absolute Error) on the <b>private test set</b>.</li>
      <li>The private test set is never revealed to participants.</li>
      <li>Organizers reserve the right to disqualify suspicious submissions.</li>
    </ul>
  </div>
</div>

</div>
