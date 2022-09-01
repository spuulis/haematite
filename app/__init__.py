import tkinter as tk
from tkinter.messagebox import showwarning

from .frames.main import MainFrame, Navbar
from visual.camera import Camera
from coils.coils import Coils
import coils.waveform
from model import Model


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry('1200x800')
        self.title('Haematite')
        self.resizable(True, True)

        self.navbar = Navbar(self)
        self.config(
            menu=self.navbar,
        )

        self.camera = Camera()
        try:
            self.camera.initialize(10000)
        except Exception as err:
            showwarning(
                title='Warning',
                message=f'{err}'
            )

        self.coils = Coils()
        self.coils.set_function(coils.waveform.sine)
        self.coils.update_params({
            'x': {'amp': 0., 'freq': 0., 'phase': 0.},
            'y': {'amp': 0., 'freq': 0., 'phase': 0.},
        }, override=True)
        try:
            self.coils.initialize()
        except Exception as err:
            showwarning(
                title='Warning',
                message=f'{err}'
            )

        self.model = Model(self.camera, self.coils)

        self.main_frame = MainFrame(self, self.model)
        self.main_frame.grid(row=0, column=0, sticky=tk.NSEW)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

    def run(self):
        self.camera.start_capture()
        self.coils.start()
        self.model.start()

    def stop(self):
        # Stop instruments
        self.model.stop()
        self.model.join()
        self.coils.stop()
        self.coils.join()
        self.camera.stop_capture()
