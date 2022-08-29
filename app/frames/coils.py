from matplotlib import pyplot as plt
from matplotlib import style
import matplotlib.animation as animation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import tkinter as tk


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

        tk.Checkbutton(self, text='Couple coils').grid(
            column=0, row=0, sticky=tk.W)
        tk.Checkbutton(self, text='Disable coils').grid(
            column=0, row=1, sticky=tk.W)


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
        self.ax1 = self.fig.add_subplot(1, 1, 1)
        self.ax1.set_ylim(-5, 5)
        self.ax1.xaxis.set_major_formatter(plt.NullFormatter())
        self.xline, = self.ax1.plot(self.tvalues, self.xvalues, 'r')
        self.yline, = self.ax1.plot(self.tvalues, self.yvalues, 'b')

        self.plotcanvas = FigureCanvasTkAgg(self.fig, self)
        self.plotcanvas.get_tk_widget().grid(column=0, row=0)
        self.ani = animation.FuncAnimation(
            self.fig, self.animate, interval=1, blit=False)

    def animate(self, i):
        field = self.controller.field
        self.tvalues.append(field['t'])
        self.xvalues.append(field['x'] * 1.e3)
        self.yvalues.append(field['y'] * 1.e3)

        self.xline.set_data(self.tvalues, self.xvalues)
        self.yline.set_data(self.tvalues, self.yvalues)
        self.ax1.set_xlim(field['t']-5, field['t'])


class CoilParametersFrame(tk.LabelFrame):
    def __init__(self, parent, controller, coil_name):
        tk.LabelFrame.__init__(
            self, parent,
            text=f'{coil_name.upper()} Coils',
        )
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
                width=6,
                validate='all',
                validatecommand=vcmd,
            )
            entry.grid(
                column=0, row=parameter['row']*2+1, sticky=tk.W,
                padx=(2, 5), pady=(0, 5),
            )

    def on_validate(self, value, reason, widget_name):
        parameter = self.parameters[widget_name.split('.')[-1]]
        # widget = self.winfo_toplevel().nametowidget(widget_name)
        match reason:
            case 'focusin':
                return True
            case 'focusout':
                v = 0.
                if value != '':
                    v = float(value)
                match parameter['id']:
                    case 'freq':
                        v = v * 2 * np.pi
                    case 'amp':
                        v = v * 1.e-3
                self.controller.coils.update_params({
                    f'{self.coil_name}': {f'{parameter["id"]}': v},
                })
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
                v = float(value)
                self.controller.coils.update_params({
                    f'{self.coil_name}': {f'{parameter["id"]}': v},
                })
                return True
        return True
