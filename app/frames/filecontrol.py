import tkinter as tk
from tkinter import ttk


class FileControlFrame(ttk.Frame):
    def __init__(self, parent, model):
        ttk.Frame.__init__(self, parent)
        self.model = model

        self.grid_columnconfigure(1, weight=1)

        ttk.Label(self, text='File name: ').grid(
            row=0, column=0, padx=(5, 0), pady=(5, 0), sticky=tk.W)
        self.entry = ttk.Entry(self)
        self.entry.grid(row=0, column=1, padx=(0, 5), sticky=tk.EW)

        self.button = ttk.Button(
            self, text="Start recording", width=12,
            command=self.toggle_recording,
        )
        self.button.grid(row=0, column=2, columnspan=2, padx=5, sticky=tk.EW)

    def toggle_recording(self):
        print(self.model.recording)
        if not self.model.recording:
            # Commence recording
            self.model.start_recording()
            self.button.config(text='Stop recording')
        else:
            # Stop recording
            filename = self.entry.get()
            self.model.stop_recording(filename)
            self.button.config(text='Start recording')
        return True
