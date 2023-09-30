import numpy as np
from benchopt import BaseObjective

class Objective(BaseObjective):
    min_benchopt_version = "1.5"
    name = "SVM"

    parameters = {
        'C': [1.],
    }

    def __init__(self, C):
        self.C = C

    def set_data(self, X, y):
        self.X, self.y = X, y

    def get_one_result(self):
        return np.zeros(self.X.shape[1])

    def evaluate_result(self, beta):
        n, d = self.X.shape
        s = np.dot(self.X, beta)
        return self.C * np.sum(np.maximum(1.0 - self.y * s, 0.)) / self.X.shape[0] + 0.5 * np.dot(beta, beta)

    def get_objective(self):
        return dict(X=self.X, y=self.y, C=self.C)
