from pathlib import Path
import numpy as np
from sklearn.model_selection import train_test_split

ROOT_DIR = Path(__file__).parent.parent

# Dossiers cibles pour Codabench
DATA_DIR = ROOT_DIR / 'dev_phase' / 'input_data'
REF_DIR  = ROOT_DIR / 'dev_phase' / 'reference_data'

def save_data(data, filepath):
    """Sauvegarde les données au format .npy (indispensable pour tes Ragged Arrays)"""
    filepath.parent.mkdir(parents=True, exist_ok=True)
    # On utilise allow_pickle=True car X contient des objets de tailles variables
    np.save(filepath, data, allow_pickle=True)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='Load real Crystal data for the benchmark')
    parser.add_argument('--seed', type=int, default=42, help='Random seed for split')
    args = parser.parse_args()

    # 1. CHARGEMENT DE TES VRAIES DONNÉES
    print("Chargement des cristaux réels...")
    try:
        X = np.load(ROOT_DIR / "X_data_ragged.npy", allow_pickle=True)
        y = np.load(ROOT_DIR / "y_data.npy")
    except FileNotFoundError:
        print("Erreur : Les fichiers X_data_ragged.npy ou y_data.npy sont introuvables à la racine du projet !")
        exit()

    # 2. SPLIT DES DONNÉES (Train 80% / Test 10% / Private Test 10%)
    # On fait 80% pour le train et 20% pour le reste
    X_train, X_temp, y_train, y_temp = train_test_split(
        X, y, test_size=0.2, random_state=args.seed
    )
    
    # On coupe les 20% restants en deux (Test public et Test privé)
    X_test, X_private_test, y_test, y_private_test = train_test_split(
        X_temp, y_temp, test_size=0.5, random_state=args.seed
    )

    # 3. STOCKAGE DANS LES DOSSIERS CODABENCH
    # Note : On utilise .npy car le CSV ne gère pas les tableaux structurés avec noms
    splits = [
        ('train', X_train, y_train),
        ('test', X_test, y_test),
        ('private_test', X_private_test, y_private_test),
    ]

    for name, X_split, y_split in splits:
        # Dossier pour les features (toujours dans input_data)
        feat_path = DATA_DIR / f'X_{name}.npy'
        save_data(X_split, feat_path)
        
        # Dossier pour les labels : 
        # - Train va dans input_data (visible par les participants)
        # - Test et Private vont dans reference_data (caché)
        if name == "train":
            label_path = DATA_DIR / f'y_{name}.npy'
        else:
            label_path = REF_DIR / f'y_{name}.npy'
            
        save_data(y_split, label_path)

    print(f"Setup terminé avec succès !")
    print(f"Train: {len(X_train)} | Test: {len(X_test)} | Private: {len(X_private_test)}")