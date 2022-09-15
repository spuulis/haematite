import tkinter as tk
from tkinter import ttk

import app.widgets as ctk
from model import Model


class Capture(ttk.Frame):
    def __init__(
        self, parent: tk.Widget, model: Model, id_entry: ctk.Entry,
    ) -> None:
        super().__init__(parent, padding=(5, 5, 5, 5))
        self.model = model
        self.id_entry = id_entry

        ttk.Label(self, text='Camera capture experiment').grid(
            row=0, column=0, sticky=tk.NSEW,
        )
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

    def initialize_experiment(self) -> None:
        self.id_entry.config(state='normal')
