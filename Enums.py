from strenum import StrEnum


class NumericalMethodId(StrEnum):
    EULER = "Euler's"
    IMPROVED_EULER = "Improved Euler's"
    RUNGE_KUTTA = "Runge-Kutta's"
