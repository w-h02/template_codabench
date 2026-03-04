# Formation Energy Prediction for Materials Discovery

Codabench Challenge — M2 Data Science Group Project

**Team 23:**
- OUALY Ossama ([@OUALYoss](https://github.com/OUALYoss))
- BAMOU Ilyass ([@IlyassBamou](https://github.com/IlyassBamou))
- Wissal HAOUAMI ([@w-h02](https://github.com/w-h02))
- Rayen ZARGUI ([@zarguirayen](https://github.com/zarguirayen))
- Mahdi Hadj Taieb ([@mahdiht](https://github.com/mahdiht))
- Rayen Mansour ([@Rayen-MANSOUR](https://github.com/Rayen-MANSOUR))

---

## Scientific context

The discovery of new crystalline materials drives technological innovation: high-density batteries, more efficient solar panels, superconducting materials.

A material is considered **stable** when its formation energy (Ef) is **negative and low** (in eV/atom). Traditionally, this energy is computed via **DFT (Density Functional Theory)**, a highly accurate but extremely slow quantum simulation (several hours per structure).

**Challenge goal**: train an AI model capable of predicting the formation energy of a crystal structure in milliseconds, using only the 3D positions of its atoms.

---

## Data

**Source**: [Materials Project API](https://next-gen.materialsproject.org/api)

The dataset contains **10,000 crystal structures** stored as numpy ragged arrays. Each structure is an array of shape `(n_atoms,)` with the following fields:

| Field | Description |
|---|---|
| `Z` | Atomic number |
| `coords` | 3D atomic positions (in Å) |
| `nom` | Chemical element symbol |

Dataset statistics:
- Atoms per structure: 2 to 20 (mean ≈ 11)
- Distinct elements: 82
- Formation energy (target): from −5.15 to +5.47 eV/atom (mean ≈ −1.34)

**Split**: 80% train / 10% public test / 10% private test, grouped by **chemical formula** to prevent data leakage between train and test sets.

---

## Evaluation metric

**MAE (Mean Absolute Error)** in eV/atom — lower is better.

MAE was chosen because:
- it is directly interpretable in eV/atom,
- it is robust to outliers compared to squared-error metrics,
- it is the standard metric for regression tasks in materials science.

---

## Repository structure

- `competition.yaml`: Codabench competition configuration (phases, tasks, leaderboard)
- `ingestion_program/`: loads submissions, trains the model and generates predictions
- `scoring_program/`: computes MAE between predictions and reference labels
- `solution/`: example baseline submission (XGBoost + geometric feature extraction)
- `tools/setup_data.py`: script to load and split data from `.npy` files
- `tools/create_bundle.py`: generates the `.zip` bundle for Codabench upload
- `pages/`: markdown files rendered as web pages on the challenge platform
- `starting_kit/`: exploration notebook and baseline for participants

---

## Running locally

**Generate data:**
```bash
python tools/setup_data.py
```

**Test ingestion:**
```bash
python ingestion_program/ingestion.py \
  --data-dir dev_phase/input_data/ \
  --output-dir ingestion_res/ \
  --submission-dir solution/
```

**Test scoring:**
```bash
python scoring_program/scoring.py \
  --reference-dir dev_phase/reference_data/ \
  --prediction-dir ingestion_res/ \
  --output-dir scoring_res/
```

**Create Codabench bundle:**
```bash
python tools/create_bundle.py
```

Then upload `bundle.zip` on [codabench.org](https://www.codabench.org/competitions/upload/).
