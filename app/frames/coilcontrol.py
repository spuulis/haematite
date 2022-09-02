import sys

import matplotlib as mpl
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import tkinter as tk

import coils.waveform as waveform
from model import Model


class Controller():
    def __init__(
        self, parent: tk.Frame, model: Model
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

        var_couple = tk.BooleanVar(self.parent, name='boolvar.coils.couple')
        var_couple.trace_add('write', self.toggle_coupling)
        self.variables['boolvar.coils.couple'] = var_couple

        var_disable = tk.BooleanVar(self.parent, name='boolvar.coils.disable')
        var_disable.trace_add('write', self.toggle_coils)
        self.variables['boolvar.coils.disable'] = var_disable

    def change_parameters(
        self, variable_name: str, index: str = '', mode: str = ''
    ) -> None:
        # Determine which coil and parameter is affected
        coil_parameter = str(variable_name).split('.')[-1]
        coil = coil_parameter[0]
        parameter = coil_parameter[2:]

        # Read and format the value to match units
        strvalue = self.variables[variable_name].get()
        value = 0.
        if strvalue != '':
            value = float(strvalue)
        match parameter:
            case 'freq':
                value = value * 2 * np.pi   # Hz -> rad/s
            case 'amp':
                value = value * 1.e-3       # mT -> T
            case 'phase':
                value = np.deg2rad(value)   # deg -> rad

        # Update the parameter on coils
        self.model.coils.update_params({f'{coil}': {f'{parameter}': value}})
        if (
            self.variables['boolvar.coils.couple'].get() is True
            and coil == 'x'
            and parameter != 'phase'
        ):
            self.variables[f'strvar.coils.y_{parameter}'].set(strvalue)

        # Redraw changes on the plot
        self.parent.frame_plot.redraw(
            self.model.coils.waveform.generate_profile())

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
        self.parent.frame_plot.redraw(
            self.model.coils.waveform.generate_profile())

    def toggle_coupling(
        self, variable_name: str, index: str = '', mode: str = ''
    ) -> None:
        parameters = ['amp', 'freq']
        for parameter in parameters:
            self.variables[f'strvar.coils.y_{parameter}'].set(
                self.variables[f'strvar.coils.x_{parameter}'].get()
            )
        self.variables['strvar.coils.x_phase'].set('0')
        self.variables['strvar.coils.y_phase'].set('90')

    def toggle_coils(
        self, variable_name: str, index: str = '', mode: str = ''
    ) -> None:
        pass


class CoilControlFrame(tk.Frame):
    def __init__(self, parent, model):
        tk.Frame.__init__(self, parent, relief=tk.RAISED)
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


class CoilRunFrame(tk.LabelFrame):
    def __init__(
        self, parent: tk.Frame, model: Model, controller: Controller
    ) -> None:
        tk.LabelFrame.__init__(self, parent, text='Coil Controls')
        self.model = model
        self.controller = controller

        tk.Label(self, text='Waveform').grid(
            column=0, row=0, padx=5, pady=(0, 0), sticky=tk.W)

        waveforms = ['Sine wave', 'Triangle wave', 'Sawtooth wave']
        self.controller.variables['strvar.coils.function'].set(waveforms[0])
        tk.OptionMenu(
            self, self.controller.variables['strvar.coils.function'],
            *waveforms
        ).grid(column=0, row=1, padx=5, pady=(0, 5), sticky=tk.W)

        self.controller.variables['boolvar.coils.couple'].set(True)
        tk.Checkbutton(
            self, text='Couple coils',
            variable=self.controller.variables['boolvar.coils.couple']
        ).grid(column=0, row=2, padx=5, sticky=tk.W)

        self.controller.variables['boolvar.coils.disable'].set(False)
        tk.Checkbutton(
            self, text='Disable coils',
            variable=self.controller.variables['boolvar.coils.disable']
        ).grid(column=0, row=3, padx=5, sticky=tk.W)


class CoilPlotFrame(tk.Frame):
    def __init__(self, parent, model):
        tk.Frame.__init__(self, parent)
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
            figsize=(width / dpi, width * 0.3 / dpi),
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
        self.ax.set_ylim(-5, 5)
        self.ax.set_xlim(profile['ts'][0], profile['ts'][-1])
        self.ax.set_xticks(np.arange(profile['ts'][0], profile['ts'][-1] + 1))
        self.ax.set_yticks(np.arange(-5, 5, 1))
        self.ax.plot(profile['ts'], profile['xs'] * 1.e3, 'r')
        self.ax.plot(profile['ts'], profile['ys'] * 1.e3, 'b')

        # Flush changes
        self.plotcanvas.draw()


class CoilParametersFrame(tk.LabelFrame):
    def __init__(
        self, parent: tk.Frame, model: Model, controller: Controller,
        coil_name: str
    ) -> None:
        tk.LabelFrame.__init__(
            self, parent,
            text=f'{coil_name.upper()} Coils',
        )
        self.parent = parent
        self.model = model
        self.controller = controller

        # List of all parameters
        self.coil_name = coil_name
        self.parameters = {
            'amp': {
                'id': 'amp', 'label': 'Amplitude, mT', 'row': 0,
                'default': '0.00',
                'format': '{:0.2f}',
            },
            'freq': {
                'id': 'freq', 'label': 'Frequency, Hz', 'row': 1,
                'default': '0.00',
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

            tk.Label(
                self, text=parameter['label'], justify='left', anchor='w',
            ).grid(column=0, row=parameter['row']*2, sticky=tk.W, padx=(2, 5))

            vcmd = (self.register(self.on_validate), '%P', '%V', '%W')
            entry = tk.Entry(
                self, name=f'{coil_name}_{_id}', width=8,
                textvariable=self.controller.variables[var_name],
                validate='all', validatecommand=vcmd,
            )
            entry.grid(
                column=0, row=parameter['row']*2+1, sticky=tk.W,
                padx=(2, 5), pady=(0, 5),
            )
            self.entries.append(entry)

            # Remove focus from entry when the return key is pressed
            entry.bind('<Return>', lambda event: self.focus_set())
            # Force number format when focus is removed from the entry
            entry.bind('<FocusOut>', self.on_focus_out)

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
