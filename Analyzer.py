import numpy as np

from Abstracts.AbstractEquation import AbstractEquation
from Solver import Solver


# View
class Analyzer:
    def __init__(self, methods, eq: AbstractEquation):
        self.eq = eq
        self.solvers = []
        for method in methods:
            self.solvers.append(Solver(method, eq))

    def prepare_data(self, xf: float, ni: int):
        step = (xf - self.eq.x0) / ni
        for solver in self.solvers:
            solver.solve(ni, step)  # TODO: Try except

    def plot_solution(self, plot, cbs):
        if cbs[0]:
            plot.plot(self.solvers[0].x_axis, self.solvers[0].y_axis_exact, label="Exact",
                      marker='o', linewidth=1, markersize=2)
        for i, solver in enumerate(self.solvers):
            if cbs[i + 1]:
                plot.plot(solver.x_axis, solver.y_axis_method, label=solver.method.id,
                          marker='o', linewidth=1, markersize=2)
        if True in cbs:
            plot.grid()
            plot.legend()

    def plot_lte(self, plot, cbs):
        for i, solver in enumerate(self.solvers):
            if cbs[i + 1]:
                plot.plot(solver.x_axis, solver.y_axis_lte, label=solver.method.id,
                          marker='o', linewidth=1, markersize=2)
        if True in cbs[1:]:
            plot.grid()
            plot.legend()

    def plot_gte(self, start: int, stop: int, plot, cbs):
        for i, solver in enumerate(self.solvers):
            if cbs[i + 1]:
                axis_size = stop + 1 - start
                if axis_size < 0:
                    start, stop = stop, start
                    axis_size = stop + 1 - start
                x_axis_gte = np.arange(start, stop + 1)  # Returns array [n0, n0 + 1, ..., nf]
                y_axis_gte = np.empty(axis_size)
                for index, ni in enumerate(range(start, stop + 1)):
                    temp_solver = solver
                    temp_x0 = self.eq.x0
                    temp_xf = solver.x_axis[len(solver.x_axis) - 1]
                    temp_step = (temp_xf - temp_x0) / ni
                    temp_solver.solve(ni, temp_step)  # TODO: Try except
                    y_axis_gte[index] = temp_solver.gte()
                plot.plot(x_axis_gte, y_axis_gte, label=solver.method.id,
                          marker='o', linewidth=1, markersize=2)
        if True in cbs[1:]:
            plot.grid()
            plot.legend()
