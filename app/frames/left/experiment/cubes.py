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
                self.model.experiment.start_recording()
            case False:
                experiment_id = self.parent.id_entry.get()
                if experiment_id == '':
                    experiment_id = (
                        f'{datetime.now().strftime("%Y.%m.%d, %H.%M.%S")}'
                        ' - cubes'
                    )
                self.model.experiment.stop_recording(experiment_id)

    def toggle_drawcubes(
        self, variable_name: str, index: str = '', mode: str = '',
    ) -> None:
        self.model.experiment.draw_cubes = (
            self.parent.drawcubes_button.variable.get())

    def toggle_drawmarkers(
        self, variable_name: str, index: str = '', mode: str = '',
    ) -> None:
        self.model.experiment.draw_markers = (
            self.parent.drawmarkers_button.variable.get())

    def change_markertype(
        self, variable_name: str, index: str = '', mode: str = '',
    ) -> None:
        match self.parent.markertype_buttons.variable.get():
            case '1x1 marker':
                self.model.experiment.set_marker_type('1x1')
            case '2x2 marker':
                self.model.experiment.set_marker_type('2x2')


class Cubes(ttk.Frame):
    def __init__(
        self, parent: tk.Widget, model: Model, id_entry: ctk.Entry,
    ) -> None:
        super().__init__(parent, padding=(5, 5, 5, 5))
        self.model = model
        self.id_entry = id_entry
        self.controller = Controller(self, self.model)

        gc = GridCounter()
        self.grid_columnconfigure(0, weight=1)

        self.markertype_buttons = ctk.Radiobuttons(
            self, ['1x1 marker', '2x2 marker'])
        self.markertype_buttons.grid(
            row=gc.next_row(), column=gc.next_column(), sticky=tk.NW)
        self.markertype_buttons.variable.trace_add(
            'write', self.controller.change_markertype)

        self.drawcubes_button = ctk.Checkbutton(self, text='Draw cubes')
        self.drawcubes_button.grid(
            row=gc.next_row(), column=gc.next_column(), sticky=tk.NW)
        self.drawcubes_button.variable.trace_add(
            'write', self.controller.toggle_drawcubes)

        self.drawmarkers_button = ctk.Checkbutton(self, text='Draw markers')
        self.drawmarkers_button.grid(
            row=gc.next_row(), column=gc.next_column(), sticky=tk.NW)
        self.drawmarkers_button.variable.trace_add(
            'write', self.controller.toggle_drawmarkers)

        self.record_button = ctk.Togglebutton(
            self, ontext='Stop recording', offtext='Start recording',
        )
        self.record_button.grid(
            row=gc.next_row(), column=gc.next_column(), sticky=tk.NW)
        self.record_button.variable.trace_add(
            'write', self.controller.toggle_recording)

    def initialize_experiment(self) -> None:
        self.id_entry.config(state='normal')
        self.record_button.variable.set(False)
        self.drawcubes_button.variable.set(True)
        self.drawmarkers_button.variable.set(True)
