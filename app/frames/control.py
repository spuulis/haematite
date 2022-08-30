import tkinter as tk
from tkinter import ttk

from .coilcontrol import CoilControlFrame
from .filecontrol import FileControlFrame
from .visualcontrol import VisualControlFrame


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

        self.camera_frame = VisualControlFrame(self, self.controller)
        self.camera_frame.grid(column=0, row=2, sticky=tk.EW, padx=5, pady=5)

        ttk.Separator(
            master=self,
            orient=tk.HORIZONTAL,
        ).grid(column=0, row=3, sticky=tk.EW)

        self.file_frame = FileControlFrame(self, self.controller)
        self.file_frame.grid(column=0, row=4, sticky=tk.EW, padx=5, pady=5)

        ttk.Separator(
            master=self,
            orient=tk.HORIZONTAL,
        ).grid(column=0, row=5, sticky=tk.EW)

        self.framerate_frame = FramerateControlFrame(self, self.controller)
        self.framerate_frame.grid(
            column=0, row=6, sticky=tk.EW, padx=5, pady=5)

        ttk.Separator(
            master=self,
            orient=tk.HORIZONTAL,
        ).grid(column=0, row=7, sticky=tk.EW)


class FramerateControlFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

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
        fps_controller = self.controller.frame_rate.fps
        self.l_controller.config(text='{:4.2f}'.format(fps_controller))

        fps_coils = self.controller.coils.frame_rate.fps
        self.l_coils.config(text='{:4.2f}'.format(fps_coils))

        self.after(2000, self.update_fps)
