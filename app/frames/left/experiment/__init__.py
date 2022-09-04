import tkinter as tk
from tkinter import ttk

from .capture import Capture
from .cubes import Cubes
from .phases import Phases
from utils import GridCounter


class Controller():
    def __init__(self, parent, model):
        self.parent = parent
        self.model = model


class ExperimentFrame(ttk.Frame):
    def __init__(self, parent, model):
        ttk.Frame.__init__(self, parent)
        self.model = model
        self.controller = Controller(self, self.model)

        gc = GridCounter()
        self.grid_columnconfigure(1, weight=1)

        ttk.Label(self, text='Experiment id: ').grid(
            row=gc.next_row(), column=0, padx=(10, 0), pady=(10, 0),
            sticky=tk.W,
        )
        self.entry = ttk.Entry(self)
        self.entry.grid(row=gc.get_row(), column=1, sticky=tk.EW)

        self.button = ttk.Button(
            self, text="Start recording", width=12,
            command=self.toggle_recording,
        )
        self.button.grid(row=gc.get_row(), column=2, padx=10, sticky=tk.EW)

        ExperimentControl(self, self.model, self.controller).grid(
            row=gc.next_row(), column=0, columnspan=3, sticky=tk.EW,
        )

    def toggle_recording(self):
        print(self.model.recording)
        if not self.model.recording:
            # Commence recording
            self.model.start_recording()
            self.button.config(text='Stop recording')
        else:
            # Stop recording
            filename = self.entry.get()
            self.model.stop_recording(filename)
            self.button.config(text='Start recording')
        return True


class ExperimentControl(ttk.Notebook):
    def __init__(self, parent, model, controller):
        super().__init__(parent)
        self.model = model
        self.controller = controller

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.capture_exp = Capture(self, self.model)
        self.capture_exp.grid(row=0, column=0, sticky=tk.NSEW)
        self.add(self.capture_exp, text='Camera')

        self.cubes_exp = Cubes(self, self.model)
        self.cubes_exp.grid(row=0, column=0, sticky=tk.NSEW)
        self.add(self.cubes_exp, text='Cubes')

        self.phases_exp = Phases(self, self.model)
        self.phases_exp.grid(row=0, column=0, sticky=tk.NSEW)
        self.add(self.phases_exp, text='Phases')