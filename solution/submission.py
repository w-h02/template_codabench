import numpy as np
from xgboost import XGBRegressor


class CrystalFeatureExtractor:
    """
        Converts variable-size crystal coordinates into fixed-size features.
        In this case the features are:
            - the mean of coordinates (x, y, z) and their std variations
            - the centroid of atoms: mean of their coordinates, elmnt in (x_mean, y_mean, y_mean)
            - the distances of the atoms to the centroid
    """
    def transform(self, X):
        features = []

        for crystal in X:
            coords = np.array(crystal)

            num_atoms = len(coords)

            mean_coords = coords.mean(axis=0)
            std_coords = coords.std(axis=0)

            centroid = mean_coords
            distances = np.linalg.norm(coords - centroid, axis=1)

            mean_dist = distances.mean()
            std_dist = distances.std()

            feature_vector = np.concatenate([
                [num_atoms],
                mean_coords,
                std_coords,
                [mean_dist, std_dist]
            ])

            features.append(feature_vector)

        return np.array(features)


class CrystalModel:

    def __init__(self):
        self.extractor = CrystalFeatureExtractor()
        self.model = XGBRegressor(
            n_estimators=200,
            max_depth=6,
            learning_rate=0.1,
            random_state=42
        )

    def fit(self, X, y):
        X_features = self.extractor.transform(X)
        self.model.fit(X_features, y)

    def predict(self, X):
        X_features = self.extractor.transform(X)
        return self.model.predict(X_features)


def get_model():
    return CrystalModel()   