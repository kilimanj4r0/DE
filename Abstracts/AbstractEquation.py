from abc import ABC, abstractmethod


# Abstract class for given equation
class AbstractEquation(ABC):
    # there are might be characteristics of a function (e.g. array of points of discontinuity)

    @abstractmethod
    def const(self) -> float:
        pass

    @abstractmethod
    def f(self, x: float, y: float) -> float:
        pass

    @abstractmethod
    def y(self, x: float) -> float:
        pass
