import sys

import matplotlib as mpl
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import tkinter as tk
from tkinter import ttk

import coils.waveform as waveform
from model import Model
from utils import GridCounter


class Controller():
    def __init__(
        self, parent: ttk.Frame, model: Model
    ) -> None:
        self.parent = parent
        self.model = model

        self.variables = {}
        self.initialize_variables()

    def initialize_variables(self):
        parameter_variables = [
            'strvar.coils.x_amp',
            'strvar.coils.x_freq',
            'strvar.coils.x_phase',
            'strvar.coils.y_amp',
            'strvar.coils.y_freq',
            'strvar.coils.y_phase',
        ]
        for var_name in parameter_variables:
            var = tk.StringVar(self.parent, name=var_name)
            var.trace_add('write', self.change_parameters)
            self.variables[var_name] = var

        var_function = tk.StringVar(self.parent, name='strvar.coils.function')
        var_function.trace_add('write', self.change_function)
        self.variables['strvar.coils.function'] = var_function

        var_mode = tk.StringVar(self.parent, name='strvar.coils.mode')
        var_mode.trace_add('write', self.change_mode)
        self.variables['strvar.coils.mode'] = var_mode

        var_couple = tk.BooleanVar(self.parent, name='boolvar.coils.couple')
        var_couple.trace_add('write', self.toggle_coupling)
        self.variables['boolvar.coils.couple'] = var_couple

    def request_redraw(self):
        self.parent.frame_plot.redraw(
            self.model.coils.waveform.generate_profile())

    def update_all_parameters(self, event: tk.Event) -> None:
        # Generate a dictionary of values for all parameters
        parameters = {}
        for coil_name in ['x', 'y']:
            parameters[coil_name] = {}
            for parameter in ['amp', 'freq', 'phase']:
                value = float(self.variables[
                    f'strvar.coils.{coil_name}_{parameter}'].get())
                match parameter:
                    case 'freq':
                        value = value * 2 * np.pi   # Hz -> rad/s
                    case 'amp':
                        value = value * 1.e-3       # mT -> T
                    case 'phase':
                        value = np.deg2rad(value)   # deg -> rad
                parameters[coil_name][parameter] = value

        # Flush the changes to coils
        self.model.coils.update_params(parameters)

        # Redraw changes on the plot
        self.request_redraw()

    def change_parameters(
        self, variable_name: str, index: str = '', mode: str = ''
    ) -> None:
        # Determine which coil and parameter is affected
        coil_parameter = str(variable_name).split('.')[-1]
        coil = coil_parameter[0]
        parameter = coil_parameter[2:]

        # If coils are coupled make y mimic x
        if (
            self.variables['boolvar.coils.couple'].get() is True
            and coil == 'x'
        ):
            strvalue = self.variables[variable_name].get()
            if parameter == 'phase':
                value = 0.
                if strvalue != '':
                    value = (float(strvalue) + 90) % 360
                self.variables[f'strvar.coils.y_{parameter}'].set(str(value))
            else:
                self.variables[f'strvar.coils.y_{parameter}'].set(strvalue)

    def change_function(
        self, variable_name: str, index: str = '', mode: str = ''
    ) -> None:
        function_name = self.variables[variable_name].get()
        match function_name:
            case 'Sine wave':
                self.model.coils.set_function(waveform.sine)
            case 'Triangle wave':
                self.model.coils.set_function(waveform.triangle)
            case 'Sawtooth wave':
                self.model.coils.set_function(waveform.sawtooth)

        # Redraw changes on the plot
        self.request_redraw()

    def toggle_coupling(
        self, variable_name: str, index: str = '', mode: str = ''
    ) -> None:
        if self.variables[variable_name].get() is True:
            parameters = ['amp', 'freq']
            for parameter in parameters:
                self.variables[f'strvar.coils.y_{parameter}'].set(
                    self.variables[f'strvar.coils.x_{parameter}'].get()
                )
            self.variables['strvar.coils.y_phase'].set(
                str((float(
                    self.variables['strvar.coils.x_phase'].get()
                ) + 90) % 360)
            )
            self.update_all_parameters(tk.Event())

    def change_mode(
        self, variable_name: str, index: str = '', mode: str = ''
    ) -> None:
        _mode = self.variables[variable_name].get()
        match _mode:
            case 'Disabled':
                self.model.coils.waveform.hold()
            case 'Waveform':
                self.model.coils.waveform.release()
            case 'Hold at 5 mT':
                self.model.coils.waveform.hold({'x': 5.e-3, 'y': 5.e-3})

        # Redraw changes on the plot
        self.request_redraw()


class CoilControlFrame(ttk.Frame):
    def __init__(self, parent, model):
        ttk.Frame.__init__(self, parent, padding=(5, 5, 5, 5))
        self.model = model

        self.controller = Controller(self, self.model)

        self.frame_plot = CoilPlotFrame(self, self.model)
        self.frame_plot.grid(
            row=0, column=0, columnspan=3, sticky=tk.EW, padx=5, pady=5)
        self.grid_rowconfigure(0)

        self.frame_x_parameters = CoilParametersFrame(
            self, self.model, self.controller, 'x')
        self.frame_x_parameters.grid(row=1, column=0, padx=5, pady=5)

        self.frame_y_parameters = CoilParametersFrame(
            self, self.model, self.controller, 'y')
        self.frame_y_parameters.grid(row=1, column=1, padx=5, pady=5)

        self.coilrun = CoilRunFrame(
            self, self.model, self.controller)
        self.coilrun.grid(row=1, column=2, sticky=tk.NSEW, padx=5, pady=5)
        self.grid_columnconfigure(2, weight=1)

        self.controller.update_all_parameters(tk.Event())


class CoilRunFrame(ttk.LabelFrame):
    def __init__(
        self, parent: ttk.Frame, model: Model, controller: Controller
    ) -> None:
        ttk.LabelFrame.__init__(
            self, parent, text='Coil Controls', padding=(5, 5, 5, 5))
        self.model = model
        self.controller = controller

        gc = GridCounter()

        waveforms = ['Sine wave', 'Triangle wave', 'Sawtooth wave']
        self.controller.variables['strvar.coils.function'].set(waveforms[0])
        ttk.OptionMenu(
            self, self.controller.variables['strvar.coils.function'],
            waveforms[0], *waveforms,
        ).grid(column=0, row=gc.next_row(), padx=5, pady=(5, 0), sticky=tk.W)

        self.controller.variables['boolvar.coils.couple'].set(True)
        ttk.Checkbutton(
            self, text='Couple coils',
            variable=self.controller.variables['boolvar.coils.couple']
        ).grid(column=0, row=gc.next_row(), padx=5, pady=5, sticky=tk.W)

        modes = ['Disabled', 'Waveform', 'Hold at 5 mT']
        self.controller.variables['strvar.coils.mode'].set(modes[0])
        for mode in modes:
            ttk.Radiobutton(
                self, text=mode, value=mode,
                variable=self.controller.variables['strvar.coils.mode'],
            ).grid(column=0, row=gc.next_row(), padx=5, sticky=tk.W)


class CoilPlotFrame(ttk.Frame):
    def __init__(self, parent, model):
        ttk.Frame.__init__(self, parent)
        self.model = model

        self.tvalues = []
        self.xvalues = []
        self.yvalues = []

        mpl.style.use('ggplot')
        width = 500
        # For some reason on MacOS the plot is twice as big
        if sys.platform == 'darwin':
            width /= 2

        dpi = self.winfo_fpixels('1i')
        self.fig = plt.figure(
            figsize=(width / dpi, width * 0.4 / dpi),
            dpi=dpi,
            facecolor='#BBB',
        )

        self.ax = self.fig.add_axes([0, 0, 1, 1])
        self.ax.set_axis_off()

        self.plotcanvas = FigureCanvasTkAgg(self.fig, self)
        self.plotcanvas.get_tk_widget().grid(column=0, row=0)
        self.grid_columnconfigure(0, weight=1)

    def redraw(self, profile):
        # Remove old data
        self.ax.clear()

        # Plot the new data
        self.ax.set_ylim(-6, 6)
        self.ax.set_xlim(profile['ts'][0], profile['ts'][-1])
        self.ax.set_xticks(np.arange(profile['ts'][0], profile['ts'][-1] + 1))
        self.ax.set_yticks(np.arange(-5, 6, 1))
        self.ax.plot(profile['ts'], profile['xs'] * 1.e3, 'r')
        self.ax.plot(profile['ts'], profile['ys'] * 1.e3, 'b')

        # Flush changes
        self.plotcanvas.draw()


class CoilParametersFrame(ttk.LabelFrame):
    def __init__(
        self, parent: ttk.Frame, model: Model, controller: Controller,
        coil_name: str
    ) -> None:
        ttk.LabelFrame.__init__(
            self, parent, text=f'{coil_name.upper()} Coils',
            padding=(5, 5, 5, 5),
        )
        self.parent = parent
        self.model = model
        self.controller = controller

        # List of all parameters
        self.coil_name = coil_name
        self.parameters = {
            'amp': {
                'id': 'amp', 'label': 'Amplitude, mT', 'row': 0,
                'default': '1.00',
                'format': '{:0.2f}',
            },
            'freq': {
                'id': 'freq', 'label': 'Frequency, Hz', 'row': 1,
                'default': '1.00',
                'format': '{:0.2f}',
            },
            'phase': {
                'id': 'phase', 'label': 'Phase, \u00B0', 'row': 2,
                'default': '0' if self.coil_name == 'x' else '90',
                'format': '{:0.0f}',
            }
        }

        # Generate label, entry pair for each parameter
        self.entries = []
        for _id, parameter in self.parameters.items():
            var_name = f'strvar.coils.{coil_name}_{_id}'
            self.controller.variables[var_name].set(parameter['default'])

            ttk.Label(
                self, text=parameter['label'], justify='left', anchor='w',
            ).grid(column=0, row=parameter['row']*2, sticky=tk.W, padx=5)

            vcmd = (self.register(self.on_validate), '%P', '%V', '%W')
            entry = ttk.Entry(
                self, name=f'{coil_name}_{_id}', width=8,
                textvariable=self.controller.variables[var_name],
                validate='all', validatecommand=vcmd,
            )
            entry.grid(
                column=0, row=parameter['row']*2+1, sticky=tk.W,
                padx=5, pady=(0, 5),
            )
            self.entries.append(entry)

            # Remove focus from entry when the return key is pressed
            entry.bind('<Return>', lambda event: self.focus_set(), add=True)
            # Force number format when focus is removed from the entry
            entry.bind('<FocusOut>', self.on_focus_out, add=True)
            # Update parameters when focus is removed from the entry
            entry.bind(
                '<FocusOut>', self.controller.update_all_parameters, add=True,
            )
            # Select text on entry selection
            entry.bind(
                '<FocusIn>',
                lambda event: event.widget.selection_range(0, tk.END),
            )

        # Disable entries for y coils if coils are coupled
        if coil_name == 'y':
            def toggle_enable(variable_name, index, mode):
                disabled = self.controller.variables[variable_name].get()
                for entry in self.entries:
                    if disabled:
                        entry.config(state='disabled')
                    else:
                        entry.config(state='normal')
            self.controller.variables['boolvar.coils.couple'].trace_add(
                'write', toggle_enable)

    def on_focus_out(self, event):
        strvalue = event.widget.get()
        value = 0.
        if strvalue != '':
            value = float(strvalue)
        variable_name = 'strvar.coils.' + str(event.widget).split('.')[-1]
        parameter = str(event.widget).split('.')[-1][2:]
        if parameter == 'phase':
            value %= 360
        formatted = self.parameters[parameter]['format'].format(value)
        self.controller.variables[variable_name].set(formatted)

    def on_validate(self, value, reason, widget_name):
        match reason:
            case 'focusin':
                return True
            case 'focusout':
                return True
            case 'key':
                if value == '':
                    return True
                try:
                    float(value)
                    return True
                except ValueError:
                    return False
            case 'forced':
                return True
        return True