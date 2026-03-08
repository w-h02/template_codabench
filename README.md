<div align="center">

# Formation Energy Prediction for Materials Discovery

**M2 Data Science — Group Project — Codabench Challenge**

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white)
![Scikit-learn](https://img.shields.io/badge/Scikit--learn-compatible-F7931E?logo=scikit-learn&logoColor=white)
![Metric](https://img.shields.io/badge/Metric-MAE%20(eV%2Fatom)-27AE60)
![Task](https://img.shields.io/badge/Task-Regression-8E44AD)
![Data](https://img.shields.io/badge/Source-Materials%20Project-1A5276)

</div>

---

## Scientific context

The discovery of new crystalline materials drives technological innovation: high-density batteries, more efficient solar panels, and superconducting materials.

A material is **stable** when its formation energy **Ef is negative and low** (eV/atom).
Traditionally, Ef is computed via **DFT (Density Functional Theory)** — highly accurate but extremely slow (several hours per structure).

> **Challenge goal**: train an AI model to predict formation energy in **milliseconds**, using only the 3D positions of atoms.

---

## Team 23

| Name | GitHub |
|---|---|
| BAMOU Ilyass | [@IlyassBamou](https://github.com/IlyassBamou) |
| HAOUAMI Wissal | [@w-h02](https://github.com/w-h02) |
| HADJ TAIEB Mahdi | [@mahdiht](https://github.com/mahdiht) |
| MANSOUR Rayen | [@Rayen-MANSOUR](https://github.com/Rayen-MANSOUR) |
| OUALY Ossama | [@OUALYoss](https://github.com/OUALYoss) |
| ZARGUI Rayen | [@zarguirayen](https://github.com/zarguirayen) |

---

## Dataset

**Source**: [Materials Project API](https://next-gen.materialsproject.org/api)

| Property | Value |
|---|---|
| Number of structures | 10,000 |
| Atoms per structure | 2 – 20 (mean ≈ 11) |
| Distinct elements | 82 |
| Target (Ef) range | −5.15 to +5.47 eV/atom |
| Target mean | −1.34 eV/atom |

Each structure is a numpy ragged array with three fields:

| Field | Description |
|---|---|
| `Z` | Atomic number |
| `coords` | 3D positions in Ångströms |
| `nom` | Element symbol (e.g. `"Fe"`, `"O"`) |

**Split strategy**: 80% train / 10% public test / 10% private test, **grouped by chemical formula** to prevent data leakage.

---

## Evaluation

```
MAE = mean( |y_pred − y_true| )   [eV/atom]   ← lower is better
```

MAE was chosen for its direct interpretability in eV/atom and robustness to outliers.

---

## Repository structure

```
.
├── competition.yaml          # Codabench competition config
├── ingestion_program/        # Loads submission, trains model, generates predictions
├── scoring_program/          # Computes MAE vs. reference labels
├── solution/                 # Baseline submission (XGBoost + geometric features)
├── starting_kit/             # Exploration notebook + baseline for participants
├── pages/                    # HTML/CSS competition pages
└── tools/
    ├── setup_data.py         # Load & split data from .npy files
    ├── create_bundle.py      # Build the Codabench .zip bundle
    ├── Dockerfile            # Docker image for ingestion/scoring
    └── run_docker.py         # Helper to build & test locally
```

---

## Running locally

<details>
<summary><b>1. Generate data</b></summary>

```bash
python tools/setup_data.py
```
</details>

<details>
<summary><b>2. Test ingestion</b></summary>

```bash
python ingestion_program/ingestion.py \
  --data-dir dev_phase/input_data/ \
  --output-dir ingestion_res/ \
  --submission-dir solution/
```
</details>

<details>
<summary><b>3. Test scoring</b></summary>

```bash
python scoring_program/scoring.py \
  --reference-dir dev_phase/reference_data/ \
  --prediction-dir ingestion_res/ \
  --output-dir scoring_res/
```
</details>

<details>
<summary><b>4. Build & upload bundle</b></summary>

```bash
python tools/create_bundle.py
```

Upload `bundle.zip` on [codabench.org/competitions/upload](https://www.codabench.org/competitions/upload/).
</details>

<details>
<summary><b>5. Test with Docker</b></summary>

```bash
pip install docker
python tools/run_docker.py
```
</details>
