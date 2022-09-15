import tkinter as tk
from tkinter import ttk

import app.widgets as ctk
from model import Model
from utils import GridCounter


class Calibrate(ttk.Frame):
    def __init__(
        self, parent: tk.Widget, model: Model, id_entry: ctk.Entry,
    ) -> None:
        super().__init__(parent, padding=(5, 5, 5, 5))
        self.model = model
        self.id_entry = id_entry

        gc = GridCounter()

        ttk.Label(self, text='Chessboard dimensions: ').grid(
            row=gc.next_row(), column=gc.next_column(), sticky=tk.W,
        )
        dimensions_frame = ttk.Frame(self)
        dimensions_frame.grid(
            row=gc.get_row(), column=gc.next_column(), sticky=tk.W)
        ttk.Entry(dimensions_frame, width=3).grid(
            row=0, column=0, sticky=tk.W,
        )
        ttk.Label(dimensions_frame, text=' x ').grid(
            row=0, column=1, sticky=tk.W,
        )
        ttk.Entry(dimensions_frame, width=3).grid(
            row=0, column=2, sticky=tk.W,
        )

        ttk.Label(self, text='Square edge length: ').grid(
            row=gc.next_row(), column=gc.next_column(), sticky=tk.W,
        )
        edge_frame = ttk.Frame(self)
        edge_frame.grid(
            row=gc.get_row(), column=gc.next_column(), sticky=tk.W,
        )
        ttk.Entry(edge_frame, width=5).grid(
            row=0, column=0, sticky=tk.W,
        )
        ttk.Label(edge_frame, text='mm').grid(
            row=0, column=1, sticky=tk.W,
        )

        ttk.Label(self, text='Number of images taken: ').grid(
            row=gc.next_row(), column=gc.next_column(), sticky=tk.W,
            pady=(10, 0),
        )
        ttk.Label(self, text='0').grid(
            row=gc.get_row(), column=gc.next_column(), sticky=tk.W,
            pady=(10, 0),
        )

        ttk.Label(self, text='Calibration accuracy: ').grid(
            row=gc.next_row(), column=gc.next_column(), sticky=tk.W,
            pady=(0, 10),
        )
        ttk.Label(self, text='?.?????').grid(
            row=gc.get_row(), column=gc.next_column(), sticky=tk.W,
            pady=(0, 10),
        )

        buttons_frame = ttk.Frame(self)
        buttons_frame.grid(
            row=gc.next_row(), column=gc.next_column(), columnspan=2,
            sticky=tk.EW,
        )

        ttk.Button(buttons_frame, text='Capture').grid(
            row=0, column=0, sticky=tk.EW,
        )
        buttons_frame.grid_columnconfigure(0, weight=1)
        ttk.Button(buttons_frame, text='Calibrate').grid(
            row=0, column=1, sticky=tk.EW,
        )
        buttons_frame.grid_columnconfigure(1, weight=1)
        ttk.Button(buttons_frame, text='Save').grid(
            row=0, column=2, sticky=tk.EW,
        )
        buttons_frame.grid_columnconfigure(2, weight=1)
        ttk.Button(buttons_frame, text='Reset').grid(
            row=0, column=3, sticky=tk.EW,
        )
        buttons_frame.grid_columnconfigure(3, weight=1)

        self.grid_columnconfigure(1, weight=1)

    def initialize_experiment(self) -> None:
        self.id_entry.config(state='disabled')
