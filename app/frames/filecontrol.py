import tkinter as tk
from tkinter import ttk


class FileControlFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.grid_columnconfigure(1, weight=1)

        ttk.Label(self, text='File name: ').grid(
            row=0, column=0, padx=(5, 0), pady=(5, 0), sticky=tk.W)
        self.entry = tk.Entry(self)
        self.entry.grid(row=0, column=1, padx=(0, 5), sticky=tk.EW)

        self.button = tk.Button(
            self, text="Start recording", width=12,
            command=self.toggle_recording,
        )
        self.button.grid(row=0, column=2, columnspan=2, padx=5, sticky=tk.EW)

    def toggle_recording(self):
        print(self.controller.recording)
        if not self.controller.recording:
            # Commence recording
            self.controller.start_recording()
            self.button.config(text='Stop recording')
        else:
            # Stop recording
            filename = self.entry.get()
            self.controller.stop_recording(filename)
            self.button.config(text='Start recording')
        return True
