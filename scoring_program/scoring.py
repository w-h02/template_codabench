import json
import sys
from pathlib import Path
import numpy as np

EVAL_SETS = ["test", "private_test"]


def compute_mae(predictions, targets):
    """Compute Mean Absolute Error. Lower is better."""
    preds = np.array(predictions, dtype=float).flatten()
    targs = np.array(targets,     dtype=float).flatten()

    nan_mask = np.isnan(preds)
    if nan_mask.any():
        print(f"  WARNING: {nan_mask.sum()} NaN predictions replaced with 1e6")
        preds[nan_mask] = 1e6

    return float(np.mean(np.abs(preds - targs)))


def main(reference_dir, prediction_dir, output_dir):
    scores = {}

    for eval_set in EVAL_SETS:
        print(f"Scoring {eval_set}...")

        predictions = np.load(
            prediction_dir / f"{eval_set}_predictions.npy", allow_pickle=True
        )
        targets = np.load(
            reference_dir / f"y_{eval_set}.npy", allow_pickle=True
        )

        scores[eval_set] = compute_mae(predictions, targets)
        print(f"  MAE ({eval_set}): {scores[eval_set]:.6f} eV/atom")

    json_durations = (prediction_dir / "metadata.json").read_text()
    durations = json.loads(json_durations)
    scores.update(**durations)

    print(scores)

    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "scores.json").write_text(json.dumps(scores))

    print("Scoring Program finished.")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Scoring program for Codabench"
    )
    parser.add_argument("--reference-dir",  type=str, default="/app/input/ref")
    parser.add_argument("--prediction-dir", type=str, default="/app/input/res")
    parser.add_argument("--output-dir",     type=str, default="/app/output")
    args = parser.parse_args()

    main(
        Path(args.reference_dir),
        Path(args.prediction_dir),
        Path(args.output_dir),
    )
