import json

import tkinter as tk
from tkinter import ttk

from utils import GridCounter


class SystemFrame(ttk.Frame):
    def __init__(self, parent, model):
        super().__init__(parent, padding=(5, 5, 5, 5))
        self.model = model

        gc = GridCounter()
        self.grid_rowconfigure(0, weight=1)

        CameraControls(self, self.model).grid(
            column=gc.next_column(), row=0, padx=5, pady=5, sticky=tk.NS)

        FramerateFrame(self, self.model).grid(
            column=gc.next_column(), row=0, padx=5, pady=5, sticky=tk.NSEW)
        self.grid_columnconfigure(gc.get_column(), weight=1)


class CameraControls(ttk.LabelFrame):
    def __init__(self, parent, model):
        super().__init__(parent, text='Camera controls', padding=(5, 5, 5, 5))
        self.model = model

        self.grid_columnconfigure(0, weight=1)

        ttk.Label(
            self,
            text='Exposure time, \u03BCs',
            justify='left',
            anchor='w',
        ).grid(row=0, column=0, padx=5, sticky=tk.W)
        vcmd = (self.register(
            self.validate_exposure_time
        ), '%P', '%V', '%W')
        ttk.Entry(
            self,
            textvariable=tk.StringVar(self, value='10000'),
            width=8,
            validate='all',
            validatecommand=vcmd,
        ).grid(
            column=0, row=1, sticky=tk.W,
            padx=5, pady=(0, 5),
        )

        ttk.Button(
            self,
            text='Load calibration',
            command=self.load_calib,
        ).grid(row=2, column=0, padx=5, pady=(0, 5), sticky=tk.NW)

    def validate_exposure_time(self, value, reason, widget_name):
        match reason:
            case 'focusin':
                pass
            case 'focusout':
                v = int(value)
                self.model.camera.set_exposure_time(v)
            case 'key':
                if value == '':
                    return True
                try:
                    _ = int(value)
                except ValueError:
                    return False
            case 'forced':
                pass
        return True

    def load_calib(self):
        with open('calibration.json', 'r') as json_file:
            calib = json.load(json_file)
            self.model.camera.calibrate(calib['mtx'], calib['dist'])


class FramerateFrame(ttk.LabelFrame):
    def __init__(self, parent, model):
        super().__init__(
            parent, text='System statistics', padding=(5, 5, 5, 5))
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
