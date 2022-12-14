import tkinter as tk
from tkinter import ttk

from utils import GridCounter


class Entry(ttk.Entry):
    def __init__(self, parent: tk.Widget, *args, **kwargs) -> None:
        super().__init__(parent, *args, **kwargs)
        self.parent = parent
        self.variable = tk.StringVar(self, name=f'strvar.{self.winfo_name()}')
        super().config(textvariable=self.variable)
        self.bind('<Return>', lambda event: self.parent.focus_set(), add=True)


class Checkbutton(ttk.Checkbutton):
    def __init__(self, parent: tk.Widget, *args, **kwargs) -> None:
        super().__init__(parent, *args, **kwargs)
        self.parent = parent
        self.variable = tk.BooleanVar(
            self, name=f'boolvar.{self.winfo_name()}')
        super().config(variable=self.variable)


class Togglebutton(ttk.Button):
    def __init__(
        self, parent: tk.Widget, ontext: str, offtext: str,
        variable_state: bool = False, *args, **kwargs,
    ) -> None:
        super().__init__(parent, *args, **kwargs)
        self.parent = parent
        self.ontext = ontext
        self.offtext = offtext

        self.variable = tk.BooleanVar(
            self, name=f'boolvar.{self.winfo_name()}')
        self.config(command=lambda: self.variable.set(not self.variable.get()))
        self.variable.trace_add('write', self.update_text)
        self.variable.set(variable_state)

    def update_text(
        self, variable_name: str, index: str = '', mode: str = '',
    ) -> None:
        match self.variable.get():
            case True:
                self.config(text=self.ontext)
            case False:
                self.config(text=self.offtext)


class Radiobuttons(ttk.Frame):
    def __init__(
        self, parent: tk.Widget, modes: list[str], *args, **kwargs,
    ) -> None:
        super().__init__(parent, *args, **kwargs)
        self.parent = parent
        self.modes = modes

        self.variable = tk.StringVar(
            self, name=f'strvar.{self.winfo_name()}')
        self.variable.set(self.modes[0])
        gc = GridCounter()
        for mode in modes:
            ttk.Radiobutton(
                self, text=mode, value=mode, variable=self.variable,
            ).grid(column=0, row=gc.next_row(), sticky=tk.W)
