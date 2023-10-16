import numpy as np
from benchopt import BaseObjective

def smooth_hinge(u, gamma=1.0):
    loss = (1.0 - u)**2 / (2*gamma)
    loss[u>=1] = 0.0
    loss[u<=(1-gamma)] = 1 - u[u<=(1-gamma)] - gamma/2
    return np.mean(loss)

class Objective(BaseObjective):
    min_benchopt_version = "1.5"
    name = "smooth-SVM"

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
        s = self.y * np.dot(self.X, beta)
        return self.C * smooth_hinge(s) + 0.5 * np.dot(beta, beta)

    def get_objective(self):
        return dict(X=self.X, y=self.y, C=self.C)
