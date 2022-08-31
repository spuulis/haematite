import cv2
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import ttk


class OutputFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.grid_columnconfigure(0, weight=1)

        self.image_frame = ImageFrame(self, controller)
        self.image_frame.grid(row=0, column=0, sticky=tk.NSEW)
        self.grid_rowconfigure(0, weight=1)

        ttk.Separator(
            master=self,
            orient=tk.HORIZONTAL,
        ).grid(row=1, column=0, sticky=tk.EW)

        self.data_frame = DataFrame(self)
        self.data_frame.grid(row=2, column=0, sticky=tk.NSEW)
        self.grid_rowconfigure(2, minsize=200)


class ImageFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.label = tk.Label(self)
        self.label.grid(row=0, column=0, sticky='NS')
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.show_frame()

    def show_frame(self):
        # Get the latest frame and convert into Image
        img = self.controller.img
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
        ))
        # Convert image to PhotoImage
        imgtk = ImageTk.PhotoImage(image=frame)
        self.label.imgtk = imgtk
        self.label.configure(image=imgtk)
        self.after(20, self.show_frame)


class DataFrame(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)

        self.label = ttk.Label(self, text='Data frame')
        self.label.pack(ipadx=10, ipady=10)
