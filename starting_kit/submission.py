import numpy as np
from sklearn.base import BaseEstimator, RegressorMixin
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import RidgeCV

from materials_utils import build_feature_table, get_numeric_feature_columns


class MaterialsBaselineRegressor(BaseEstimator, RegressorMixin):
    """Baseline regressor for raw ragged atomic structures."""

    def __init__(self, alphas=None):
        self.alphas = alphas if alphas is not None else np.logspace(-3, 3, 13)

    def fit(self, X, y):
        df, self.elements_ = build_feature_table(X)
        self.feature_columns_ = get_numeric_feature_columns(df)
        X_tab = df[self.feature_columns_].to_numpy(dtype=float)
        self.model_ = make_pipeline(StandardScaler(), RidgeCV(alphas=self.alphas))
        self.model_.fit(X_tab, np.asarray(y, dtype=float))
        return self

    def predict(self, X):
        df, _ = build_feature_table(X, elements=self.elements_)
        X_tab = df[self.feature_columns_].to_numpy(dtype=float)
        return self.model_.predict(X_tab)


def get_model():
    return MaterialsBaselineRegressor()
