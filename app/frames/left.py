import tkinter as tk
from tkinter import ttk

from .coilcontrol import CoilControlFrame
from .filecontrol import FileControlFrame
from .visualcontrol import VisualControlFrame


class LeftFrame(ttk.Frame):
    def __init__(self, parent, model):
        ttk.Frame.__init__(self, parent)
        self.model = model

        self.grid_columnconfigure(0, weight=1)

        self.coil_frame = CoilControlFrame(self, self.model)
        self.coil_frame.grid(column=0, row=0, sticky=tk.EW)

        ttk.Separator(
            master=self,
            orient=tk.HORIZONTAL,
        ).grid(column=0, row=1, sticky=tk.EW)

        self.camera_frame = VisualControlFrame(self, self.model)
        self.camera_frame.grid(column=0, row=2, sticky=tk.EW)

        ttk.Separator(
            master=self,
            orient=tk.HORIZONTAL,
        ).grid(column=0, row=3, sticky=tk.EW)

        self.file_frame = FileControlFrame(self, self.model)
        self.file_frame.grid(column=0, row=4, sticky=tk.EW)

        ttk.Separator(
            master=self,
            orient=tk.HORIZONTAL,
        ).grid(column=0, row=5, sticky=tk.EW)

        self.framerate_frame = FramerateControlFrame(self, self.model)
        self.framerate_frame.grid(
            column=0, row=6, sticky=tk.EW)

        ttk.Separator(
            master=self,
            orient=tk.HORIZONTAL,
        ).grid(column=0, row=7, sticky=tk.EW)


class FramerateControlFrame(ttk.Frame):
    def __init__(self, parent, model):
        ttk.Frame.__init__(self, parent, padding=(5, 5, 5, 5))
        self.model = model

        self.grid_columnconfigure(0, minsize=150)
        self.grid_columnconfigure(1, weight=1)

        ttk.Label(self, text='Controller fps').grid(
            row=0, column=0, padx=5, sticky=tk.W)
        self.l_controller = ttk.Label(self, text='???.??')
        self.l_controller.grid(row=0, column=1, padx=5, sticky=tk.W)

        ttk.Label(self, text='Image fps').grid(
            row=1, column=0, padx=5, sticky=tk.W)
        self.l_image = ttk.Label(self, text='???.??')
        self.l_image.grid(row=1, column=1, padx=5, sticky=tk.W)

        ttk.Label(self, text='Coils fps').grid(
            row=2, column=0, padx=5, sticky=tk.W)
        self.l_coils = ttk.Label(self, text='???.??')
        self.l_coils.grid(row=2, column=1, padx=5, sticky=tk.W)

        self.after(1000, self.update_fps)

    def update_fps(self):
        fps_controller = self.model.frame_rate.fps
        self.l_controller.config(text='{:4.2f}'.format(fps_controller))

        fps_coils = self.model.coils.frame_rate.fps
        self.l_coils.config(text='{:4.2f}'.format(fps_coils))

        self.after(2000, self.update_fps)
