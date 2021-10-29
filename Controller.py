import io
import PySimpleGUI as sg
import json
from matplotlib import pyplot as plt, rcParams
from matplotlib.backends.backend_agg import FigureCanvasAgg
import re

from Equations.Equation19 import Equation19
from NumericalMethods.Euler import Euler
from NumericalMethods.ImprovedEuler import ImprovedEuler
from NumericalMethods.RungeKutta import RungeKutta
from Analyzer import Analyzer


class Controller:
    @staticmethod
    def draw_figure(element, figure):
        plt.close('all')
        canv = FigureCanvasAgg(figure)
        buf = io.BytesIO()
        canv.print_figure(buf, format='png')
        if buf is not None:
            buf.seek(0)
            element.update(data=buf.read())
            return canv
        else:
            return None

    # Controller        TODO: Is it really a controller?
    @staticmethod
    def start():
        # Setting
        def set_fig_size(fig1, fig2, fig3):
            dpi = fig1.get_dpi()
            height = size_fig[1] + 30
            width = 2 * height
            fig1.set_size_inches(width / float(dpi), height / float(dpi))
            fig2.set_size_inches(width / float(dpi), height / float(dpi))
            fig3.set_size_inches(width / float(dpi), height / float(dpi))

        def set_fig_labels(fig1, fig2, fig3):
            fig1.text(0.5, 0.01, 'x', ha='center')
            fig1.text(0.04, 0.5, 'y', va='center', rotation='vertical')
            fig2.text(0.5, 0.01, 'x', ha='center')
            fig2.text(0.04, 0.5, 'error', va='center', rotation='vertical')
            fig3.text(0.5, 0.01, 'n', ha='center')
            fig3.text(0.04, 0.5, 'maximum error', va='center', rotation='vertical')

        sg.theme('Reddit')
        pad_title = ((10, 10), (10, 0))
        pad_pb_text = ((10, 10), (10, 10))
        pad_h_sep = ((10, 10), 20)
        pad_input = ((10, 5), (5, 5))  # L R U B
        pad_column = ((10, 10), (0, 0))
        pad_tab = (0, (0, 30))
        pad_tab_group = (0, (0, 20))
        pad_btn = (10, 10)
        size_fig = (750, 350)
        size_input = (10, 1)
        font_title = ('Verdana', 14, 'bold')
        font_tab_group = ('Verdana', 11, 'normal')
        font_checkbox = ('Verdana', 10, 'normal')
        font_params = ('Verdana', 10, 'italic')
        font_btn = ('Verdana', 10, 'bold')
        font_input = ('Verdana', 10, 'bold')
        rcParams['font.sans-serif'] = ['Verdana']
        input_regexp = re.compile('[+-]?([0-9]+([.][0-9]*)?|[.][0-9]+)')

        # Interface layout
        checkboxes_layout = sg.Column(layout=[
            [sg.Checkbox(text="Euler's method", key="cb_euler", enable_events=True,
                         default=True, font=font_checkbox)],
            [sg.Checkbox(text="Improved Euler's method", key="cb_improved_euler",
                         enable_events=True,
                         font=font_checkbox)],
            [sg.Checkbox(text="Runge-Kutta's method", key="cb_runge_kutta",
                         enable_events=True, font=font_checkbox)],
            [sg.Checkbox(text="Exact solution", key="cb_exact", enable_events=True,
                         default=True, disabled=False, font=font_checkbox)]
        ], element_justification='left',
            justification='left',
            vertical_alignment='top')

        layout = [[sg.Column(layout=[
            [sg.T("Given IVP:    y' = 2x + y - 3, y(1) = 1",
                  justification='left',
                  pad=pad_title,
                  font=font_title)],
            [sg.HorizontalSeparator(pad=pad_h_sep)],
            [sg.TabGroup(enable_events=True,
                         layout=[[
                             sg.Tab(title="Solution graph", key='tab_sol', layout=[
                                 [sg.Image(key='fig_sol', size=size_fig, pad=pad_tab)]]),
                             sg.Tab(title="LTE graph", key='tab_lte', layout=[
                                 [sg.Image(key='fig_lte', size=size_fig, pad=pad_tab)]]),
                             sg.Tab(title="GTE graph", key='tab_gte', layout=[
                                 [sg.Image(key='fig_gte', size=size_fig, pad=pad_tab)]])
                         ]], font=font_tab_group, key='tab_group', pad=pad_tab_group)],
        ], justification='center',
            pad=pad_column,
            element_justification='left',
            vertical_alignment='top'),
            sg.Column(layout=[
                [sg.T("Parameters:",
                      justification='left',
                      pad=pad_title,
                      font=font_title)],
                [sg.HorizontalSeparator(pad=pad_h_sep)],
                [sg.Column(layout=[
                    [sg.T('y0', pad=pad_input, font=font_params)],
                    [sg.T('x0', pad=pad_input, font=font_params)],
                    [sg.T('X', pad=pad_input, font=font_params)],
                    [sg.T('N', pad=pad_input, font=font_params)],
                    [sg.T('n_start', pad=pad_input, font=font_params)],
                    [sg.T('n_stop', pad=pad_input, font=font_params)]
                ]),
                    sg.Column(layout=[
                        [sg.Input(tooltip="Initial value for y0",
                                  default_text='1',
                                  justification='center',
                                  enable_events=True,
                                  key='y0',
                                  size=size_input,
                                  pad=pad_input,
                                  font=font_input)],
                        [sg.Input(tooltip="Initial value for x0",
                                  default_text='1',
                                  justification='center',
                                  enable_events=True,
                                  key='x0',
                                  size=size_input,
                                  pad=pad_input,
                                  font=font_input)],
                        [sg.Input(tooltip="Stop X point",
                                  default_text='7',
                                  justification='center',
                                  enable_events=True,
                                  key='X',
                                  size=size_input,
                                  pad=pad_input,
                                  font=font_input)],
                        [sg.Input(tooltip="Number of grid steps",
                                  default_text='7',
                                  justification='center',
                                  enable_events=True,
                                  key='N',
                                  size=size_input,
                                  pad=pad_input,
                                  font=font_input)],
                        [sg.Input(tooltip="Start value of number of grid steps",
                                  default_text='7',
                                  justification='center',
                                  enable_events=True,
                                  key='n0',
                                  size=size_input,
                                  pad=pad_input,
                                  font=font_input,
                                  disabled=True)],
                        [sg.Input(tooltip="Stop value of number of grid steps",
                                  default_text='100',
                                  justification='center',
                                  enable_events=True,
                                  key='nf',
                                  size=size_input,
                                  pad=pad_input,
                                  font=font_input,
                                  disabled=True)]
                    ])],
                [sg.Button(button_text='Plot', key='plot_btn', font=font_btn, expand_x=True, pad=pad_btn)],
                [checkboxes_layout],
                [sg.T("Progress:",
                      justification='left',
                      pad=pad_pb_text,
                      font=font_title)],
                [sg.HorizontalSeparator()],
                [sg.ProgressBar(10, orientation='h', size=(10, 20), key='pb', expand_x=True)]
            ], pad=pad_column,
                element_justification='center',
                vertical_alignment='top',
                justification='center')]]

        # Creating a window
        window = sg.Window(title='Numerical Methods — Computational Practicum', layout=layout)

        while True:
            e, values = window.read()

            def plot():
                window['pb'].UpdateBar(1)
                y0_input = float(values['y0']) if input_regexp.match(values['y0']) else None
                x0_input = float(values['x0']) if input_regexp.match(values['x0']) else None
                x_input = float(values['X']) if input_regexp.match(values['X']) else None
                n_input = int(values['N']) if input_regexp.match(values['N']) else None
                n0_input = int(values['n0']) if input_regexp.match(values['n0']) else None
                nf_input = int(values['nf']) if input_regexp.match(values['nf']) else None
                input_values = (y0_input, x0_input, x_input, n_input, n0_input, nf_input)
                if None in input_values:
                    return
                window['pb'].UpdateBar(2)

                # Change equation here
                equation = Equation19(x0_input, y0_input)
                window['pb'].UpdateBar(3)
                # Add methods here
                methods = [Euler(), ImprovedEuler(), RungeKutta()]
                window['pb'].UpdateBar(4)

                checkboxes = [values["cb_exact"],
                              values["cb_euler"],
                              values["cb_improved_euler"],
                              values["cb_runge_kutta"]]
                analyzer = Analyzer(methods, equation)
                window['pb'].UpdateBar(5)
                analyzer.prepare_data(x_input, n_input)
                window['pb'].UpdateBar(6)

                plt.close('all')
                fig_sol, plot_sol = plt.subplots()
                fig_lte, plot_lte = plt.subplots()
                fig_gte, plot_gte = plt.subplots()
                set_fig_size(fig_sol, fig_lte, fig_gte)
                set_fig_labels(fig_sol, fig_lte, fig_gte)
                window['pb'].UpdateBar(7)

                if values['tab_group'] == 'tab_sol':
                    analyzer.plot_solution(plot_sol, checkboxes)
                    Controller.draw_figure(window['fig_sol'], fig_sol)
                window['pb'].UpdateBar(8)

                if values['tab_group'] == 'tab_lte':
                    analyzer.plot_lte(plot_lte, checkboxes)
                    Controller.draw_figure(window['fig_lte'], fig_lte)
                window['pb'].UpdateBar(9)

                if values['tab_group'] == 'tab_gte':
                    analyzer.plot_gte(n0_input, nf_input, plot_gte, checkboxes)
                    Controller.draw_figure(window['fig_gte'], fig_gte)
                window['pb'].UpdateBar(10)

            # Debug
            # print(e)
            # print(json.dumps(values, indent=2))

            # Working with events
            if e == sg.WIN_CLOSED:
                break
            if values['tab_group'] == 'tab_gte':
                window['n0'].update(disabled=False)
                window['nf'].update(disabled=False)
            elif values['tab_group'] != 'tab_gte':
                window['n0'].update(disabled=True)
                window['nf'].update(disabled=True)
            if values['tab_group'] != 'tab_sol':
                window['cb_exact'].update(disabled=True)
            elif values['tab_group'] == 'tab_sol':
                window['cb_exact'].update(disabled=False)
            if '' in values.values():
                window['plot_btn'].update(disabled=True)
                if values['tab_group'] != 'tab_sol':
                    window['cb_exact'].update(disabled=True)
                window['cb_euler'].update(disabled=True)
                window['cb_improved_euler'].update(disabled=True)
                window['cb_runge_kutta'].update(disabled=True)
            elif '' not in values.values():
                window['plot_btn'].update(disabled=False)
                if values['tab_group'] == 'tab_sol':
                    window['cb_exact'].update(disabled=False)
                window['cb_euler'].update(disabled=False)
                window['cb_improved_euler'].update(disabled=False)
                window['cb_runge_kutta'].update(disabled=False)
            if e in ('plot_btn', 'tab_group',
                     'cb_exact', 'cb_euler', 'cb_improved_euler', 'cb_runge_kutta'):
                plot()

        window.close()
