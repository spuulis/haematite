import json

import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showwarning

import config
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
        self.var_camexpt = tk.StringVar(
            self, name='strvar.system.camexpt')
        self.var_camexpt.set(config.CAMERA_EXPOSURE_TIME)
        self.entry_camexpt = ttk.Entry(
            self,
            textvariable=self.var_camexpt,
            width=8,
            validate='all',
            validatecommand=vcmd,
        )
        self.entry_camexpt.grid(
            column=0, row=1, sticky=tk.W,
            padx=5, pady=(0, 5),
        )
        self.entry_camexpt.bind(
            '<Return>', lambda event: self.focus_set(), add=True)
        self.entry_camexpt.bind('<FocusOut>', self.set_exposure_time, add=True)

        ttk.Button(
            self,
            text='Load calibration',
            command=self.load_calib,
        ).grid(row=2, column=0, padx=5, pady=(0, 5), sticky=tk.NW)

    def validate_exposure_time(self, value, reason, widget_name):
        if value != '':
            try:
                _ = int(value)
            except ValueError:
                return False
        return True

    def set_exposure_time(self, event: tk.Event):
        strvalue = self.var_camexpt.get()
        value = 0
        if strvalue != '':
            value = int(strvalue)
        self.model.camera.set_exposure_time(value)

    def load_calib(self):
        try:
            with open('calibration.json', 'r') as json_file:
                calib = json.load(json_file)
                self.model.camera.calibrate(calib['mtx'], calib['dist'])
        except FileNotFoundError as err:
            showwarning(
                title='Warning',
                message=f'Camera could not be calibrated:\n\n{err}'
            )


class FramerateFrame(ttk.LabelFrame):
    def __init__(self, parent, model):
        super().__init__(
            parent, text='System statistics', padding=(5, 5, 5, 5))
        self.model = model

        gc = GridCounter()
        self.grid_columnconfigure(0, minsize=150)
        self.grid_columnconfigure(1, minsize=100)
        self.grid_columnconfigure(2, weight=1)

        ttk.Label(self, text='Model fps').grid(
            row=gc.next_row(), column=gc.next_column(), padx=5, sticky=tk.W)
        self.l_model_fps = ttk.Label(self, text='???.??')
        self.l_model_fps.grid(
            row=gc.get_row(), column=gc.next_column(), padx=5, sticky=tk.W)
        self.l_model_usage = ttk.Label(self, text='???%')
        self.l_model_usage.grid(
            row=gc.get_row(), column=gc.next_column(), padx=5, sticky=tk.W)

        ttk.Label(self, text='Image fps').grid(
            row=gc.next_row(), column=gc.next_column(), padx=5, sticky=tk.W)
        self.l_image_fps = ttk.Label(self, text='???.??')
        self.l_image_fps.grid(
            row=gc.get_row(), column=gc.next_column(), padx=5, sticky=tk.W)
        self.l_image_usage = ttk.Label(self, text='???%')
        self.l_image_usage.grid(
            row=gc.get_row(), column=gc.next_column(), padx=5, sticky=tk.W)

        self.after(100, self.update_fps)

    def update_fps(self):
        fps_model = self.model.frame_rate.fps
        self.l_model_fps.config(text='{:0.2f}'.format(fps_model))
        usage_model = self.model.frame_rate.usage * 100
        self.l_model_usage.config(
            text=f'{"{:3.0f}".format(usage_model)}%')

        # TODO: Rework reading frame_rate of ImageFrame
        fps_image = self.nametowidget(
            '.!mainframe.!rightframe.!imageframe').frame_rate.fps
        self.l_image_fps.config(text='{:0.2f}'.format(fps_image))
        usage_image = self.nametowidget(
            '.!mainframe.!rightframe.!imageframe').frame_rate.usage * 100
        self.l_image_usage.config(
            text=f'{"{:3.0f}".format(usage_image)}%')

        self.after(2000, self.update_fps)
