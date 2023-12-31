from benchopt import BaseDataset, safe_import_context
from sklearn.preprocessing import StandardScaler
import numpy as np

with safe_import_context() as import_ctx:
    from benchopt.datasets import make_correlated_data

class Dataset(BaseDataset):

    name = "Classification_sim"

    parameters = {
        'n_samples, n_features': [
            (100, 10),
            (300, 10),
            (500, 10),
            (700, 10),
            (1000, 10)]
    }

    def __init__(self, n_samples=10, n_features=50, random_state=42):
        self.n_samples = n_samples
        self.n_features = n_features
        self.random_state = random_state

    def get_data(self):
        X, y, _ = make_correlated_data(
            n_samples=self.n_samples, n_features=self.n_features,
            random_state=self.random_state
        )
        y = 2*(y > 0) - 1

        scaler = StandardScaler()
        X = scaler.fit_transform(X)

        n, d = X.shape
        x_sensitive = X[:,np.random.randint(d)]
        x_sensitive = x_sensitive - np.mean(x_sensitive)
        data = dict(X=X, y=y, Z=x_sensitive)

        return data
