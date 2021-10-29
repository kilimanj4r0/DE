import numpy as np
from Abstracts import AbstractEquation, AbstractNumericalMethod


# Model
class Solver:
    # Constructor for
    def __init__(self, method: AbstractNumericalMethod, eq: AbstractEquation):
        self.method: AbstractNumericalMethod = method
        self.eq: AbstractEquation = eq

        self.x_axis = np.array([self.eq.x0])
        self.y_axis_exact = np.array([self.eq.y0])
        self.y_axis_method = np.array([self.eq.y0])
        self.y_axis_lte = np.array([0.])

    # Allocate memory for each array of points, fill it with init values
    def set_axis_size(self, ni: int):
        self.x_axis = np.empty(ni)
        self.y_axis_exact = np.empty(ni)
        self.y_axis_method = np.empty(ni)
        self.y_axis_lte = np.zeros(ni)

        self.x_axis[0] = self.eq.x0
        self.y_axis_exact[0] = self.eq.y0
        self.y_axis_method[0] = self.eq.y0

    # Fill the arrays with values
    def solve(self, ni: int, step: float):  # TODO: If we need only GTE it's not effective
        self.set_axis_size(ni + 1)

        for i in range(1, ni + 1):
            self.x_axis[i] = self.x_axis[i - 1] + step
            self.y_axis_exact[i] = self.eq.y(self.x_axis[i])
            self.y_axis_method[i] = self.method.next(self.eq, self.x_axis[i - 1], self.y_axis_method[i - 1], step)
            self.y_axis_lte[i] = self.y_axis_exact[i] - self.y_axis_method[i]

    # Get the maximum of all local truncation errors (GTE)
    def gte(self):
        assert len(self.y_axis_lte) > 1, "Solver have not solved yet"
        return max(self.y_axis_lte)
