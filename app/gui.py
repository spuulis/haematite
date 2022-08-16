import tkinter as tk
import commands as cmnd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, 
NavigationToolbar2Tk)
# from visual.calibration import chessboard
# import visual.tracker
 

window = tk.Tk()
window.geometry("800x800")
# window.configure(background = "grey")
window.title("Pagraba spoles")
window.resizable(False, False)

frm_labels = tk.Frame(
    master=window,
    borderwidth=0
)


lbl_freq = tk.Label(
    master=frm_labels,
    text="Frequency:",
    anchor="e",
    width=10
)
lbl_amp = tk.Label(
    master=frm_labels,
    text="Amplitude:",
    anchor="e",
    width=10
)
lbl_phase = tk.Label(
    master=frm_labels,
    text="Phase:",
    anchor="e",
    width=10
)


ent_freq = tk.Entry(
    master=frm_labels,
    width=10
)
ent_amp = tk.Entry(
    master=frm_labels,
    width=10
)
ent_phase = tk.Entry(
    master=frm_labels,
    width=10
)


frm_labels.place(x=5,y=5)
lbl_freq.grid(row=0,column=0)
lbl_amp.grid(row=1,column=0)
lbl_phase.grid(row=2,column=0)

ent_freq.grid(row=0,column=1)
ent_amp.grid(row=1,column=1)
ent_phase.grid(row=2,column=1)
frm_labels.update()

# lbl_amp = tk.Label(
#     master=window,
#     text="amplitude:"
# )

btn_plot = tk.Button(
    master=window,
    text="Plot sine",
    width=20,
    height=1,
    bg="#aafaaa",
    command=lambda: plot()
)


btn_plot.place(x=5, y=frm_labels.winfo_height()+10)
btn_plot.update()



b_canvas = tk.Canvas(
    master=window,
    height=300,
    width=300,
).place(x=20,y=120)
def plot():

    fig = Figure(figsize = (10, 10), dpi = 50)        
    x,y = cmnd.get_values(ent_amp.get(),ent_freq.get(),ent_phase.get())
    plot1 = fig.add_subplot(111)
    plot1.plot(x,y)

    canvas = FigureCanvasTkAgg(
        fig,
        master = b_canvas
    )  
    canvas.draw()
    canvas.get_tk_widget().pack()
  
    toolbar = NavigationToolbar2Tk(
        canvas,
        b_canvas
    )
    toolbar.update()

    canvas.get_tk_widget().place(x=0,y=0)
# button.pack()
# label.pack()

# window.update_idletasks()

# frame.place(x=20, y=20)
print(btn_plot.winfo_rooty())
window.mainloop()