import tkinter as tk
from tkinter import ttk


from .coils import CoilControlFrame


class ControlFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.grid_columnconfigure(0, weight=1)

        self.coil_frame = CoilControlFrame(self, self.controller)
        self.coil_frame.grid(column=0, row=0, sticky=tk.EW, padx=5, pady=5)

        ttk.Separator(
            master=self,
            orient=tk.HORIZONTAL,
        ).grid(column=0, row=1, sticky=tk.EW)

        self.camera_frame = CameraControlFrame(self)
        self.camera_frame.grid(column=0, row=2, sticky=tk.EW, padx=5, pady=5)

        ttk.Separator(
            master=self,
            orient=tk.HORIZONTAL,
        ).grid(column=0, row=3, sticky=tk.EW)

        self.file_frame = FileControlFrame(self)
        self.file_frame.grid(column=0, row=4, sticky=tk.EW, padx=5, pady=5)

        ttk.Separator(
            master=self,
            orient=tk.HORIZONTAL,
        ).grid(column=0, row=5, sticky=tk.EW)


class CameraControlFrame(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.label = ttk.Label(self, text='Camera control frame')
        self.label.pack(ipadx=10, ipady=10)


class FileControlFrame(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.label = ttk.Label(self, text='File control frame')
        self.label.pack(ipadx=10, ipady=10)
