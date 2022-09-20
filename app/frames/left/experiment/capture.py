from datetime import datetime

import tkinter as tk
from tkinter import ttk

import app.widgets as ctk
from model import Model
from utils import GridCounter


class Controller():
    def __init__(self, parent: tk.Widget, model: Model) -> None:
        self.parent = parent
        self.model = model

        self.recording = False

    def toggle_recording(
        self, variable_name: str, index: str = '', mode: str = '',
    ) -> None:
        match self.parent.record_button.variable.get():
            case True:
                experiment_id = self.parent.id_entry.get()
                if experiment_id == '':
                    experiment_id = (
                        f'{datetime.now().strftime("%Y.%m.%d, %H.%M.%S")}'
                        ' - capture'
                    )
                self.model.experiment.start_recording(experiment_id)
            case False:
                self.model.experiment.stop_recording(None)

    def pulse_capture(self):
        experiment_id = self.parent.id_entry.get()
        if experiment_id == '':
            experiment_id = (
                f'{datetime.now().strftime("%Y.%m.%d, %H.%M.%S")}'
                ' - cubes'
            )
        self.model.experiment.capture(experiment_id)


class Capture(ttk.Frame):
    def __init__(
        self, parent: tk.Widget, model: Model, id_entry: ctk.Entry,
    ) -> None:
        super().__init__(parent, padding=(5, 5, 5, 5))
        self.model = model
        self.id_entry = id_entry
        self.controller = Controller(self, self.model)

        gc = GridCounter()

        ttk.Button(
            self, text='Capture', command=self.controller.pulse_capture,
        ).grid(
            row=gc.next_row(), column=gc.next_column(), sticky=tk.W)

        self.record_button = ctk.Togglebutton(
            self, ontext='Stop continuous capture',
            offtext='Start continuous capture',
        )
        self.record_button.grid(
            row=gc.next_row(), column=gc.next_column(), sticky=tk.W)
        self.record_button.variable.trace_add(
            'write', self.controller.toggle_recording)
        self.grid_columnconfigure(0, weight=1)

    def initialize_experiment(self) -> None:
        self.id_entry.config(state='normal')
