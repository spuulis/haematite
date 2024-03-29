import cv2
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import ttk

from .systemcontrol import SystemFrame
import config
from utils import FrameRate


class RightFrame(ttk.Frame):
    def __init__(self, parent, model):
        ttk.Frame.__init__(self, parent)
        self.model = model
        self.parent = parent

        self.grid_columnconfigure(0, weight=1)

        self.image_frame = ImageFrame(self, model)
        self.image_frame.grid(row=0, column=0, sticky=tk.NSEW)
        self.grid_rowconfigure(0, weight=1)

        self.show_image = tk.BooleanVar(
            self.parent, name='boolvar.image.show')
        self.show_image.trace_add('write', self.toggle_image)
        self.show_image.set(True)
        ttk.Checkbutton(
            self,
            variable=self.show_image,
        ).grid(column=0, row=0, sticky=tk.SE)

        ttk.Separator(
            master=self,
            orient=tk.HORIZONTAL,
        ).grid(row=1, column=0, sticky=tk.EW)

        self.system_frame = SystemFrame(self, self.model)
        self.system_frame.grid(row=2, column=0, sticky=tk.NSEW)
        self.grid_rowconfigure(2, minsize=200)

    def toggle_image(
        self, variable_name: str, index: str = '', mode: str = ''
    ) -> None:
        self.image_frame.show_image = self.show_image.get()
        if self.show_image.get() is True:
            self.image_frame.show_frame()


class ImageFrame(ttk.Frame):
    def __init__(self, parent, model):
        ttk.Frame.__init__(self, parent)
        self.model = model

        self.frame_rate = FrameRate()
        self.frame_rate.set_target_fps(config.IMAGE_FPS)

        self.label = tk.Label(self)
        self.label.grid(row=0, column=0, sticky=tk.NS)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # self.show_frame()
        self.show_image = False

    def show_frame(self):
        # Get the latest frame and convert into Image
        img = self.model.img
        img_height, img_width, _ = img.shape
        cv2image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        frame = Image.fromarray(cv2image)
        frame = frame.resize((
            min(
                self.winfo_width(),
                max(int(self.winfo_height() / img_height * img_width), 1),
            ),
            min(
                self.winfo_height(),
                max(int(self.winfo_width() / img_width * img_height), 1),
            ),
        ), Image.NEAREST)

        # Convert image to PhotoImage
        imgtk = ImageTk.PhotoImage(image=frame)
        self.label.imgtk = imgtk
        self.label.configure(image=imgtk)

        if self.show_image is True:
            self.after(
                # tkinter.after requires time in ms
                int(self.frame_rate.imitate_throttle() * 1.e3),
                self.show_frame,
            )
