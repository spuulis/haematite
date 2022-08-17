import tkinter as tk
import commands as cmnd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure
import matplotlib.animation as anim
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, 
NavigationToolbar2Tk)
from matplotlib import style
# from visual.calibration import chessboard
# import visual.tracker
 

dt = 25 #ms
anim_running = False
param = [0,0,0]
window = tk.Tk()
window.geometry("800x800")
# window.configure(background = "grey")
window.title("Pagraba spoles")
window.resizable(False, False)
style.use('ggplot')

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

plot_canvas = tk.Canvas(
    master=window,
    height=600,
    width=600,
    background="#ffffff"
)

btn_plot = tk.Button(
    master=window,
    text="Update plot",
    width=20,
    height=1,
    bg="#aafaaa",
    command=lambda: upd_param()
)

btn_plot.place(x=5, y=frm_labels.winfo_height()+10)
btn_plot.update()

def clear_plot():
    for child in plot_canvas.winfo_children():
        child.destroy()


fig = Figure(figsize = (10, 10), dpi = 50)        
x = []
y = []
plot1 = fig.add_subplot(111)
plot1.set_xlim(-5, 0)
line, = plot1.plot(x,y)


canvas = FigureCanvasTkAgg(
    fig,
    master = plot_canvas
)  
canvas.draw()
canvas.get_tk_widget().pack()
  
toolbar = NavigationToolbar2Tk(
    canvas,
    plot_canvas
)
toolbar.update()

canvas.get_tk_widget().pack()


def animate(i):
    
    t = np.around(dt*i/1000,3)
    y_new = cmnd.next_sin_val(param[0],param[1],param[2],t)
    
    plot1.set_xlim(t-5,t)
    x.append(t)
    y.append(y_new)
    plot1.set_ylim(-max(np.max(y[-1000:])*1.1,0.5),max(np.max(y[-1000:])*1.1,0.5))

    line.set_data(x,y)

def upd_param():
    global param
    if (cmnd.check_num(ent_amp.get()) and cmnd.check_num(ent_freq.get()) and cmnd.check_num(ent_phase.get())):
        param = [ent_amp.get(),ent_freq.get(),ent_phase.get()]

    

ani = anim.FuncAnimation(fig, animate, interval=dt, blit=False)
# if anim_running:
#     ani.

def plot():
    fig = Figure(figsize = (10, 10), dpi = 50)        
    x,y = cmnd.get_values(ent_amp.get(),ent_freq.get(),ent_phase.get())
    plot1 = fig.add_subplot(111)
    plot1.plot(x,y)

    canvas = FigureCanvasTkAgg(
        fig,
        master = plot_canvas
    )  
    canvas.draw()
    canvas.get_tk_widget().pack()
  
    toolbar = NavigationToolbar2Tk(
        canvas,
        plot_canvas
    )
    toolbar.update()

    canvas.get_tk_widget().pack()

plot_canvas.place(x=20, y=140)

window.mainloop()