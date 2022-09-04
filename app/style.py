import sys

import tkinter as tk
from tkinter import ttk


class Style(ttk.Style):
    def __init__(self, parent: tk.Tk) -> None:
        super().__init__(parent)
        self.theme_use()

        # Set the default style
        match sys.platform:
            case 'darwin':
                self.theme_use('aqua')
            case 'win32':
                self.theme_use('winnative')

        # Initialize all modifications to default styles
        self.initialize_styles()

    def initialize_styles(self):
        pass
