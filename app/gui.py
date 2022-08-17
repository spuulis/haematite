import tkinter as tk
import commands as cmnd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure
import matplotlib.animation as anim
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, 
NavigationToolbar2Tk)
from matplotlib import style
from PIL import Image#, ImageTK
# from visual.calibration import chessboard
# import visual.tracker
 

dt = 25 #ms
anim_running = False
param = [0,0,0,np.pi/2]
window = tk.Tk()
window.geometry("800x800")
# window.configure(background = "#003050")
window.title("Pagraba spoles")
window.resizable(False, False)
style.use('ggplot')

frm_labels = tk.Frame(
    master=window,
    borderwidth=0,
    # background = "#003555"
)


lbl_freq = tk.Label(
    master=frm_labels,
    text="Frequency:",
    anchor="e",
    width=12
)
lbl_amp = tk.Label(
    master=frm_labels,
    text="Amplitude:",
    anchor="e",
    width=12
)
lbl_phase = tk.Label(
    master=frm_labels,
    text="Phase:",
    anchor="e",
    width=12
)
lbl_phase_off = tk.Label(
    master=frm_labels,
    text="Phase offset:",
    anchor="e",
    width=12
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
ent_phase.insert(0,"0")
ent_phase_off = tk.Entry(
    master=frm_labels,
    width=10
)
ent_phase_off.insert(0,"90")


frm_labels.place(x=5,y=5)
lbl_freq.grid(row=0,column=0)
lbl_amp.grid(row=1,column=0)
lbl_phase.grid(row=2,column=0)
lbl_phase_off.grid(row=3,column=0)

ent_freq.grid(row=0,column=1)
ent_amp.grid(row=1,column=1)
ent_phase.grid(row=2,column=1)
ent_phase_off.grid(row=3,column=1)
frm_labels.update()

plot_canvas = tk.Canvas(
    master=window,
    height=600,
    width=600,
    background="#fafafa"
)

btn_plot = tk.Button(
    master=window,
    text="Update plot",
    width=22,
    height=1,
    bg="#aafaaa",
    command=lambda: upd_param()
)
btn_plot.place(x=5, y=frm_labels.winfo_height()+10)
btn_plot.update()

btn_start = tk.Button(
    master=window,
    text="Start",
    width=10,
    height = 5,
    bg="#aafaaa",
    command=lambda: start_stop()
)
btn_start.place(x=195, y=5)
btn_start.update()

def clear_plot():
    for child in plot_canvas.winfo_children():
        child.destroy()

def start_stop():
    global anim_running
    if anim_running:
        anim_running = False
        btn_start["text"] = "Start"
        btn_start["bg"] = "#aafaaa"
        ani.event_source.stop()
    else:
        anim_running = True
        btn_start["text"] = "Stop"
        btn_start["bg"] = "#faaaaa"
        ani.event_source.start()


fig = Figure(figsize = (10, 10), dpi = 50)        
x = [0]
y1 = [0]
y2 = [0]
plot1 = fig.add_subplot(111)
plot1.set_xlim(-5, 0)
line1, = plot1.plot(x,y1)
line2, = plot1.plot(x,y2)


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
    x.append(t)
    y1_new = cmnd.next_sin_val(param[0],param[1],param[2],param[3],t)[0]
    y2_new = cmnd.next_sin_val(param[0],param[1],param[2],param[3],t)[1]
    y1.append(y1_new)
    y2.append(y2_new)
    
    plot1.set_xlim(x[-1]-5,x[-1])
    plot1.set_ylim(-max(np.max(y1[-1000:])*1.1,np.max(y2[-1000:])*1.1,0.5),max(np.max(y1[-1000:])*1.1,np.max(y2[-1000:])*1.1,0.5))

    line1.set_data(x,y1)
    line2.set_data(x,y2)

def upd_param():
    global param
    if (cmnd.check_num(ent_amp.get()) and cmnd.check_num(ent_freq.get()) and cmnd.check_num(ent_phase.get()) and cmnd.check_num(ent_phase_off.get())):
        param = [ent_amp.get(),ent_freq.get(),ent_phase.get(),ent_phase_off.get()]

    

# if anim_running:

ani = anim.FuncAnimation(fig, animate, interval=dt, blit=False)

if not anim_running:
    ani.event_source.start()
    ani.event_source.stop()


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

plot_canvas.place(x=20, y=155)

window.mainloop()
