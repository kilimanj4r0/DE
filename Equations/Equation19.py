from Abstracts.AbstractEquation import AbstractEquation
from numpy import exp


class Equation19(AbstractEquation):
    # Constructor for the 19th equation
    def __init__(self, x0: float, y0: float):
        # Initial values y(1) = 1
        self.x0 = x0
        self.y0 = y0

    # Integral constant coefficient = (y0 - 1 + 2 * x0) / exp(x0)
    def const(self) -> float:
        return (self.y0 - 1 + 2 * self.x0) / exp(self.x0)

    # Given function y' = f(x, y) = 2x + y - 3
    def f(self, x: float, y: float) -> float:
        return 2 * x + y - 3

    # Solution y = 1 - 2x + const * exp(x)
    def y(self, x: float) -> float:
        return 1 - 2 * x + self.const() * exp(x)
