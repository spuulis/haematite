from matplotlib import pyplot as plt
from matplotlib import style
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import tkinter as tk


import coils.waveform as waveform


class CoilControlFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, relief=tk.RAISED)
        self.controller = controller

        self.plot_frame = CoilPlotFrame(self, self.controller)
        self.plot_frame.grid(
            row=0, column=0, columnspan=3, sticky=tk.NSEW, padx=5, pady=5)
        self.grid_rowconfigure(0)

        self.x_parameters = CoilParametersFrame(
            self, self.controller, 'x')
        self.x_parameters.grid(row=1, column=0, padx=5, pady=5)

        self.y_parameters = CoilParametersFrame(
            self, self.controller, 'y')
        self.y_parameters.grid(row=1, column=1, padx=5, pady=5)

        self.coilrun = CoilRunFrame(self, self.controller)
        self.coilrun.grid(row=1, column=2, sticky=tk.NSEW, padx=5, pady=5)
        self.grid_columnconfigure(2, weight=1)


class CoilRunFrame(tk.LabelFrame):
    def __init__(self, parent, controller):
        tk.LabelFrame.__init__(self, parent, text='Coil Controls')
        self.controller = controller

        tk.Label(self, text='Waveform').grid(
            column=0, row=0, padx=5, pady=(0, 0), sticky=tk.W)
        waveforms = ['Sine wave', 'Triangle wave', 'Sawtooth wave']
        self.var_waveform = tk.StringVar()
        self.var_waveform.trace_add('write', self.change_waveform)
        self.var_waveform.set(waveforms[0])
        tk.OptionMenu(self, self.var_waveform, *waveforms).grid(
            column=0, row=1, padx=5, pady=(0, 5), sticky=tk.W)

        tk.Checkbutton(self, text='Couple coils').grid(
            column=0, row=2, padx=5, sticky=tk.W)
        tk.Checkbutton(self, text='Disable coils').grid(
            column=0, row=3, padx=5, sticky=tk.W)

    def change_waveform(self, *args):
        match self.var_waveform.get():
            case 'Sine wave':
                self.controller.coils.set_function(waveform.sine)
            case 'Triangle wave':
                self.controller.coils.set_function(waveform.triangle)
            case 'Sawtooth wave':
                self.controller.coils.set_function(waveform.sawtooth)


class CoilPlotFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.tvalues = []
        self.xvalues = []
        self.yvalues = []

        style.use('ggplot')
        self.winfo_width()
        self.fig = plt.figure(
            figsize=(7.4, 3),
            dpi=30,
            tight_layout=True,
            facecolor='#BBB',
        )
        self.ax = self.fig.add_subplot(1, 1, 1)

        self.plotcanvas = FigureCanvasTkAgg(self.fig, self)
        self.plotcanvas.get_tk_widget().grid(column=0, row=0)

    def redraw(self, profile):
        self.ax.clear()

        # Plot the new data
        self.ax.set_ylim(-5, 5)
        self.ax.set_xlim(profile['ts'][0], profile['ts'][-1])
        self.ax.xaxis.set_major_formatter(plt.NullFormatter())
        self.ax.plot(profile['ts'], profile['xs'] * 1.e3, 'r')
        self.ax.plot(profile['ts'], profile['ys'] * 1.e3, 'b')

        self.plotcanvas.draw()


class CoilParametersFrame(tk.LabelFrame):
    def __init__(self, parent, controller, coil_name):
        tk.LabelFrame.__init__(
            self, parent,
            text=f'{coil_name.upper()} Coils',
        )
        self.parent = parent
        self.controller = controller

        self.coil_name = coil_name
        self.parameters = {
            'amp': {
                'id': 'amp',
                'label': 'Amplitude, mT',
                'row': 0,
                'default': '0.000',
                'from': '0',
                'to': '5',
                'increment': '0.05',
                'format': '%4.3f',
            },
            'freq': {
                'id': 'freq',
                'label': 'Frequency, Hz',
                'row': 1,
                'default': '0.000',
                'from': '0',
                'to': '5',
                'increment': '0.05',
                'format': '%4.3f',
            },
            'phase': {
                'id': 'phase',
                'label': 'Phase, \u00B0',
                'row': 2,
                'default': '0' if self.coil_name == 'x' else '90',
                'from': '0',
                'to': '360',
                'increment': '30',
                'format': '%3.0f',
            }
        }

        for _id, parameter in self.parameters.items():
            var = tk.StringVar(
                name=f'{coil_name}_{_id}_strvar',
                value=parameter['default'],
            )

            tk.Label(
                self,
                text=parameter['label'],
                justify='left',
                anchor='w',
            ).grid(column=0, row=parameter['row']*2, sticky=tk.W, padx=(2, 5))

            vcmd = (self.register(
                self.on_validate
            ), '%P', '%V', '%W')
            entry = tk.Entry(
                self,
                name=_id,
                textvariable=var,
                width=8,
                validate='all',
                validatecommand=vcmd,
            )
            entry.grid(
                column=0, row=parameter['row']*2+1, sticky=tk.W,
                padx=(2, 5), pady=(0, 5),
            )

    def on_validate(self, value, reason, widget_name):
        parameter = self.parameters[widget_name.split('.')[-1]]

        def get_value(value, parameter_id):
            v = 0.
            if value != '':
                v = float(value)
            match parameter_id:
                case 'freq':
                    return v * 2 * np.pi
                case 'amp':
                    return v * 1.e-3
                case 'phase':
                    return np.deg2rad(v)
            return v

        match reason:
            case 'focusin':
                return True
            case 'focusout':
                v = get_value(value, parameter['id'])
                self.controller.coils.update_params({
                    f'{self.coil_name}': {f'{parameter["id"]}': v},
                })
                self.parent.plot_frame.redraw(
                    self.controller.coils.waveform.generate_profile())
                # TODO: Reformat input
                return True
            case 'key':
                if value == '':
                    return True
                try:
                    v = float(value)
                    return True
                except ValueError:
                    return False
            case 'forced':
                # TODO: Validate input
                v = get_value(value, parameter['id'])
                self.controller.coils.update_params({
                    f'{self.coil_name}': {f'{parameter["id"]}': v},
                })
                self.parent.plot_frame.redraw(
                    self.controller.coils.waveform.generate_profile())
                return True
        return True
