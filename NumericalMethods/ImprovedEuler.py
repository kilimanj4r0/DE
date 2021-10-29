from Abstracts.AbstractNumericalMethod import AbstractNumericalMethod
from Abstracts.AbstractEquation import AbstractEquation
from Enums import NumericalMethodId


class ImprovedEuler(AbstractNumericalMethod):
    id = NumericalMethodId.IMPROVED_EULER

    def next(self, eq: AbstractEquation, x: float, y: float, h: float) -> float:
        k1 = h * eq.f(x, y)
        k2 = h * eq.f(x + h, y + k1)
        return y + 0.5 * (k1 + k2)
