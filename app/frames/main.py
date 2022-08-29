import tkinter as tk
from tkinter import ttk

from .control import ControlFrame
from .output import OutputFrame


class Navbar(tk.Menu):
    def __init__(self, parent):
        tk.Menu.__init__(self, parent)
        file_menu = tk.Menu(self, tearoff=False)
        self.add_cascade(label="File", underline=0, menu=file_menu)


class MainFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.grid_rowconfigure(0, weight=1)

        self.control_frame = ControlFrame(self, self.controller)
        self.control_frame.grid(column=0, row=0, sticky=tk.NSEW)
        self.grid_columnconfigure(
            0,
            minsize=500,
        )

        ttk.Separator(
            master=self,
            orient=tk.VERTICAL,
        ).grid(column=1, row=0, sticky=tk.NS)

        self.output_frame = OutputFrame(self, self.controller)
        self.output_frame.grid(column=2, row=0, sticky=tk.NSEW)
        self.grid_columnconfigure(2, weight=1)
