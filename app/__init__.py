import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showwarning

from .frames.main import MainFrame, Navbar
from visual.camera import Camera
from coils.coils import Coils
from controller import Controller


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
            self.camera.initialize(5000)
        except Exception as err:
            showwarning(
                title='Warning',
                message=f'{err}'
            )

        self.coils = Coils()
        try:
            self.coils.test()
        except Exception as err:
            showwarning(
                title='Warning',
                message=f'{err}'
            )

        self.controller = Controller(self.camera, self.coils)

        self.main_frame = MainFrame(self, self.controller)
        self.main_frame.grid(row=0, column=0, sticky=tk.NSEW)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

    def run(self):
        self.camera.start_capture()
        self.coils.start()
        self.controller.start()

    def stop(self):
        # Stop instruments
        self.controller.stop()
        self.controller.join()
        self.coils.stop()
        self.coils.join()
        self.camera.stop_capture()
