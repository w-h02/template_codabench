from pathlib import Path
import numpy as np
from sklearn.model_selection import train_test_split

PHASE    = 'dev_phase'
DATA_DIR = Path(PHASE) / 'input_data'
REF_DIR  = Path(PHASE) / 'reference_data'


def save_npy(data, filepath: Path):
    """Save numpy array, creating parent directories as needed."""
    filepath.parent.mkdir(parents=True, exist_ok=True)
    np.save(filepath, data, allow_pickle=True)
    print(f"  Saved : {filepath}  shape={np.asarray(data, dtype=object).shape}")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description='Load crystal data and create Codabench splits'
    )
    parser.add_argument('--seed', type=int, default=42,
                        help='Random seed for reproducible splits')
    parser.add_argument('--input-x', type=str, default='X_data_ragged.npy',
                        help='Path to crystal feature file (.npy)')
    parser.add_argument('--input-y', type=str, default='y_data.npy',
                        help='Path to formation energy labels (.npy)')
    args = parser.parse_args()

    # 1. Load
    input_x = Path(args.input_x)
    input_y = Path(args.input_y)

    if not input_x.exists() or not input_y.exists():
        raise FileNotFoundError(
            f"Source files not found.\n"
            f"  Expected: {input_x.resolve()}\n"
            f"            {input_y.resolve()}\n"
            f"  Run from the project root where the .npy files are located."
        )

    print(f"Loading {input_x} ...")
    X = np.load(input_x, allow_pickle=True)
    y = np.load(input_y, allow_pickle=False)
    print(f"  X : {len(X)} samples")
    print(f"  y : {y.shape}  range=[{y.min():.3f}, {y.max():.3f}] eV/atom")

    # 2. Split: 80% train / 10% test / 10% private_test
    rng = np.random.RandomState(args.seed)

    X_train, X_temp, y_train, y_temp = train_test_split(
        X, y, test_size=0.2, random_state=rng
    )
    X_test, X_private_test, y_test, y_private_test = train_test_split(
        X_temp, y_temp, test_size=0.5, random_state=rng
    )

    # 3. Store
    # train labels → input_data/train/  (visible by participants)
    # test labels  → reference_data/    (hidden)
    for split, X_split, y_split in [
        ('train',        X_train,        y_train),
        ('test',         X_test,         y_test),
        ('private_test', X_private_test, y_private_test),
    ]:
        split_dir = DATA_DIR / split

        save_npy(X_split, split_dir / f'X_{split}.npy')

        label_dir = split_dir if split == 'train' else REF_DIR
        save_npy(y_split, label_dir / f'y_{split}.npy')

    # 4. Summary
    print()
    print("Setup complete!")
    print(f"  Total   : {len(X)}")
    print(f"  Train   : {len(X_train)}  ({len(X_train)/len(X)*100:.0f}%)")
    print(f"  Test    : {len(X_test)}   ({len(X_test)/len(X)*100:.0f}%)")
    print(f"  Private : {len(X_private_test)}   ({len(X_private_test)/len(X)*100:.0f}%)")
