import json
import sys
import time
from pathlib import Path
import numpy as np

EVAL_SETS = ["test", "private_test"]


def get_train_data(data_dir):
    """Load training features and labels."""
    training_dir = data_dir / "train"
    X_train = np.load(training_dir / "X_train.npy", allow_pickle=True)
    y_train = np.load(training_dir / "y_train.npy", allow_pickle=True)
    return X_train, y_train


def evaluate_model(model, X_test):
    """Return model predictions for a given test set."""
    return model.predict(X_test)


def main(data_dir, output_dir):
    from submission import get_model

    # Load training data
    print("Loading training data...")
    X_train, y_train = get_train_data(data_dir)
    print(f"  X_train: {X_train.shape}  y_train: {y_train.shape}")

    # Train
    print("Training the model...")
    model = get_model()
    start = time.time()
    model.fit(X_train, y_train)
    train_time = time.time() - start
    print(f"  Training done in {train_time:.2f}s")

    # Predict on all eval sets
    print("-" * 10)
    print("Evaluating the model...")
    res = {}
    start = time.time()
    for eval_set in EVAL_SETS:
        X_test_path = data_dir / eval_set / f"X_{eval_set}.npy"
        X_test = np.load(X_test_path, allow_pickle=True)
        res[eval_set] = evaluate_model(model, X_test)
        print(f"  -> '{eval_set}' predicted  shape={res[eval_set].shape}")
    test_time = time.time() - start

    duration = train_time + test_time
    print(f"Completed prediction. Total duration: {duration:.2f}s")

    # Write outputs
    output_dir.mkdir(parents=True, exist_ok=True)

    with open(output_dir / "metadata.json", "w+") as f:
        json.dump(dict(train_time=train_time, test_time=test_time), f)

    for eval_set, preds in res.items():
        filepath = output_dir / f"{eval_set}_predictions.npy"
        np.save(filepath, preds)

    print()
    print("Ingestion Program finished. Moving on to scoring.")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Ingestion program for Codabench"
    )
    parser.add_argument("--data-dir",       type=str, default="/app/input_data")
    parser.add_argument("--output-dir",     type=str, default="/app/output")
    parser.add_argument("--submission-dir", type=str, default="/app/ingested_program")
    args = parser.parse_args()

    sys.path.append(args.submission_dir)
    sys.path.append(str(Path(__file__).parent.resolve()))

    main(Path(args.data_dir), Path(args.output_dir))
