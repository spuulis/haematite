import tkinter as tk
from tkinter import ttk

from .calibrate import Calibrate
from .capture import Capture
from .cubes import Cubes
from .phases import Phases
import app.widgets as ctk
from model import Model
from utils import GridCounter


class Controller():
    def __init__(self, parent: tk.Widget, model: Model) -> None:
        self.parent = parent
        self.model = model

    def change_experiment(self, event: tk.Event) -> None:
        experiment_name = event.widget.tab(event.widget.select(), 'text')
        self.model.change_experiment(experiment_name)
        match experiment_name:
            case 'Calibrate':
                (self.parent.experiment_control.calibrate_exp
                    .initialize_experiment())
            case 'Camera':
                (self.parent.experiment_control.capture_exp
                    .initialize_experiment())
            case 'Cubes':
                (self.parent.experiment_control.cubes_exp
                    .initialize_experiment())
            case 'Phases':
                (self.parent.experiment_control.phases_exp
                    .initialize_experiment())


class ExperimentFrame(ttk.Frame):
    def __init__(self, parent: tk.Widget, model: Model) -> None:
        ttk.Frame.__init__(self, parent)
        self.model = model
        self.controller = Controller(self, self.model)

        gc = GridCounter()
        self.grid_columnconfigure(1, weight=1)

        ttk.Label(self, text='Experiment id: ').grid(
            row=gc.next_row(), column=0, padx=(10, 0), pady=(10, 0),
            sticky=tk.W,
        )
        self.id_entry = ctk.Entry(self)
        self.id_entry.grid(
            row=gc.get_row(), column=1, padx=(0, 10), pady=(10, 0),
            sticky=tk.EW,
        )

        self.experiment_control = ExperimentControl(
            self, self.model, self.controller, self.id_entry,
        )
        self.experiment_control.grid(
            row=gc.next_row(), column=0, columnspan=2, pady=(10, 0),
            sticky=tk.NSEW,
        )
        self.grid_rowconfigure(gc.get_row(), weight=1)


class ExperimentControl(ttk.Notebook):
    def __init__(
        self, parent: tk.Widget, model: Model, controller: Controller,
        id_entry: ctk.Entry,
    ) -> None:
        super().__init__(parent)
        self.model = model
        self.controller = controller
        self.id_entry = id_entry

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.calibrate_exp = Calibrate(self, self.model, self.id_entry)
        self.calibrate_exp.grid(row=0, column=0, sticky=tk.NSEW)
        self.add(self.calibrate_exp, text='Calibrate')

        self.capture_exp = Capture(self, self.model, self.id_entry)
        self.capture_exp.grid(row=0, column=0, sticky=tk.NSEW)
        self.add(self.capture_exp, text='Camera')

        self.cubes_exp = Cubes(self, self.model, self.id_entry)
        self.cubes_exp.grid(row=0, column=0, sticky=tk.NSEW)
        self.add(self.cubes_exp, text='Cubes')

        self.phases_exp = Phases(self, self.model, self.id_entry)
        self.phases_exp.grid(row=0, column=0, sticky=tk.NSEW)
        self.add(self.phases_exp, text='Phases')

        self.bind(
            '<<NotebookTabChanged>>', self.controller.change_experiment,
            add=True,
        )
