from Abstracts.AbstractNumericalMethod import AbstractNumericalMethod
from Abstracts.AbstractEquation import AbstractEquation
from Enums import NumericalMethodId


class Euler(AbstractNumericalMethod):
    id = NumericalMethodId.EULER

    def next(self, eq: AbstractEquation, x: float, y: float, h: float) -> float:
        return y + h * eq.f(x, y)
