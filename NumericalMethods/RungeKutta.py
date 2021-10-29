from Abstracts.AbstractNumericalMethod import AbstractNumericalMethod
from Abstracts.AbstractEquation import AbstractEquation
from Enums import NumericalMethodId


class RungeKutta(AbstractNumericalMethod):
    id = NumericalMethodId.RUNGE_KUTTA

    def next(self, eq: AbstractEquation, x: float, y: float, h: float) -> float:
        k = [0] * 4
        # TODO: add possibility to change the number of k's
        k[0] = h * eq.f(x, y)
        k[1] = h * eq.f(x + 0.5 * h, y + 0.5 * k[0])
        k[2] = h * eq.f(x + 0.5 * h, y + 0.5 * k[1])
        k[3] = h * eq.f(x + h, y + k[2])
        return y + (k[0] + 2 * k[1] + 2 * k[2] + k[3]) / 6
