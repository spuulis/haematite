import tkinter as tk
from tkinter import ttk

from utils import GridCounter

from .coilcontrol import CoilControlFrame
from .experiment import ExperimentFrame


class LeftFrame(ttk.Frame):
    def __init__(self, parent, model):
        ttk.Frame.__init__(self, parent)
        self.model = model

        gc = GridCounter()
        self.grid_columnconfigure(0, weight=1)

        self.coil_frame = CoilControlFrame(self, self.model)
        self.coil_frame.grid(column=0, row=gc.next_row(), sticky=tk.EW)

        ttk.Separator(
            master=self,
            orient=tk.HORIZONTAL,
        ).grid(column=0, row=gc.next_row(), sticky=tk.EW)

        self.file_frame = ExperimentFrame(self, self.model)
        self.file_frame.grid(column=0, row=gc.next_row(), sticky=tk.NSEW)
        self.grid_rowconfigure(gc.get_row(), weight=1)
