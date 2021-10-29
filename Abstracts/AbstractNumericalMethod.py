from abc import ABC, abstractmethod
from Abstracts.AbstractEquation import AbstractEquation
from Enums import NumericalMethodId


# Abstracts class for any numerical method
class AbstractNumericalMethod(ABC):
    id = NumericalMethodId

    @abstractmethod
    def next(self, eq: AbstractEquation, x: float, y: float, h: float) -> float:
        pass
