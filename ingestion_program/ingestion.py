import json
import sys
import time
from pathlib import Path
import numpy as np
import pandas as pd


EVAL_SETS = ["test", "private_test"]


def evaluate_model(model, X_test):

    y_pred = model.predict(X_test)
    return y_pred # On retourne l'array numpy directement


def get_train_data(data_dir):
    data_dir = Path(data_dir)
    X_train = np.load(data_dir / "X_train.npy", allow_pickle=True)
    y_train = np.load(data_dir / "y_train.npy", allow_pickle=True)
    return X_train, y_train


def main(data_dir, output_dir):
    # Here, you can import info from the submission module, to evaluate the
    # submission
    from submission import get_model

    X_train, y_train = get_train_data(data_dir)

    print("Training the model")

    model = get_model()

    start = time.time()
    model.fit(X_train, y_train)
    train_time = time.time() - start
    print("-" * 10)
    print("Evaluate the model")
    start = time.time()
    res = {}
    for eval_set in EVAL_SETS:
        # Chargement des fichiers X_test.npy et X_private_test.npy
        X_test_path = data_dir / f"X_{eval_set}.npy"
        X_test = np.load(X_test_path, allow_pickle=True)
        res[eval_set] = evaluate_model(model, X_test)
    test_time = time.time() - start
    print("-" * 10)
    duration = train_time + test_time
    print(f"Completed Prediction. Total duration: {duration}")

    # Write output files
    output_dir.mkdir(parents=True, exist_ok=True)
    with open(output_dir / "metadata.json", "w+") as f:
        json.dump(dict(train_time=train_time, test_time=test_time), f)
    # Sauvegarde des prédictions en .csv pour le scoring_program
    for eval_set in EVAL_SETS:
        filepath = output_dir / f"{eval_set}_predictions.csv"
        pd.DataFrame(res[eval_set]).to_csv(filepath, index=False)
    print()
    print("Ingestion Program finished. Moving on to scoring")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Ingestion program for codabench"
    )
    parser.add_argument(
        "--data-dir",
        type=str,
        default="/app/input_data",
        help="",
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default="/app/output",
        help="",
    )
    parser.add_argument(
        "--submission-dir",
        type=str,
        default="/app/ingested_program",
        help="",
    )

    args = parser.parse_args()
    sys.path.append(args.submission_dir)
    sys.path.append(Path(__file__).parent.resolve())

    main(Path(args.data_dir), Path(args.output_dir))
