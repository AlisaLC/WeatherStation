from django.db import models

import numpy as np

# Create your models here.
class LinearRegression:
    def __init__(self):
        self.W = None
        self.b = None

    def fit(self, X, y):
        X = np.array(X)
        y = np.array(y)
        self.W = np.dot(np.linalg.inv(np.dot(X.T, X)), np.dot(X.T, y))
        self.b = y.mean() - np.dot(self.W, X.mean(axis=0))

    def predict(self, X):
        return np.dot(X, self.W) + self.b