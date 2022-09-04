import json

import tkinter as tk
from tkinter import ttk


class VisualControlFrame(ttk.Frame):
    def __init__(self, parent, model):
        ttk.Frame.__init__(self, parent, padding=(5, 5, 5, 5))
        self.model = model

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        CameraControls(self, self.model).grid(
            row=0, column=0, padx=5, pady=(0, 5), sticky=tk.NSEW)
        ImageControls(self, self.model).grid(
            row=0, column=1, padx=5, pady=(0, 5), sticky=tk.NSEW)


class CameraControls(ttk.LabelFrame):
    def __init__(self, parent, model):
        ttk.LabelFrame.__init__(self, parent, text='Camera controls')
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


class ImageControls(ttk.LabelFrame):
    def __init__(self, parent, model):
        ttk.LabelFrame.__init__(self, parent, text='Image controls')
        self.model = model

        ttk.Checkbutton(self, text='Show markers').grid(
            column=0, row=0, padx=5, sticky=tk.NW)
        ttk.Checkbutton(self, text='Draw cubes').grid(
            column=0, row=1, padx=5, sticky=tk.NW)
