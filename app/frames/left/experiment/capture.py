import tkinter as tk
from tkinter import ttk


class Capture(ttk.Frame):
    def __init__(self, parent, model):
        super().__init__(parent)
        self.model = model

        ttk.Label(self, text='Camera capture experiment').grid(
            row=0, column=0, sticky=tk.NSEW,
        )
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
