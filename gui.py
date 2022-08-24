### This code is the main code to run for the GUI of the program ###
###   Imports   ####

import sys
import tkinter as tk
import tkinter.ttk
import app.commands as cmnd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure
import matplotlib.animation as anim
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,
NavigationToolbar2Tk)
from matplotlib import style
import time


from PIL import ImageTk, Image
from visual.camera import Camera
from visual.calibration import *
from visual.tracker import *
from config import *

# from visual.calibration import chessboard

# import visual.tracker

###    Setting time parameters    ###

dt = 10 #ms
fps = 30
exposure = 10000 #nanoseconds
anim_running = False
cam_running = False
chessboard = Chessboard(CHESSBOARD_SIZE,CHESSBOARD_DIM)
num_of_calib_images = 0
###   Initialising the GUI window   ###
window = tk.Tk()

window.geometry(str(window.winfo_screenwidth())+"x"+str(window.winfo_screenheight()-40))
# window.configure(background = "#003050")
window.title("Pagraba spoles")
window.resizable(True, True)
style.use('ggplot')

time_start = time.time_ns()



###  The window which encloses the parameters below
frm_labels = tk.Frame(
    master=window,
    borderwidth=0,
)
frm_cam_btn = tk.Frame(
    master=window,
    borderwidth=0,
)
frm_cam_img = tk.Frame(
    master=window,
    borderwidth=3,
    width=500,
    height=500,
    relief=tk.GROOVE
)

### Number field windows for frequency, amplitude, phase, e.c
# the text part
lbl_x = tk.Label(
    master=frm_labels,
    text="X coil control",
    anchor="c",
    width=12
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

lbl_y = tk.Label(
    master=frm_labels,
    text="Y coil control",
    anchor="c",
    width=12
)
lbl_freq_2 = tk.Label(
    master=frm_labels,
    text="Frequency:",
    anchor="e",
    width=12
)
lbl_amp_2 = tk.Label(
    master=frm_labels,
    text="Amplitude:",
    anchor="e",
    width=12
)
lbl_phase_2 = tk.Label(
    master=frm_labels,
    text="Phase:",
    anchor="e",
    width=12
)



lbl_cam_fps = tk.Label(
    master=frm_cam_btn,
    text="Camera framerate: "+str(fps),
    anchor="w",
    width=20
)
lbl_cam_exp = tk.Label(
    master=frm_cam_btn,
    text="Camera exposure: "+str(exposure/1000)+"ms",
    anchor="w",
    width=20
)
lbl_cam_img = tk.Label(
    master=frm_cam_img,
    anchor="n",
)


# the blank field part
ent_freq = tk.Entry(
    master=frm_labels,
    width=7
)
ent_amp = tk.Entry(
    master=frm_labels,
    width=7
)
ent_phase = tk.Entry(
    master=frm_labels,
    width=7
)
ent_phase_off = tk.Entry(
    master=frm_labels,
    width=7
)

ent_freq_2 = tk.Entry(
    master=frm_labels,
    width=7
)
ent_amp_2 = tk.Entry(
    master=frm_labels,
    width=7
)
ent_phase_2 = tk.Entry(
    master=frm_labels,
    width=7
)

#setting values to the blank field
ent_freq.insert(0,"1")
ent_amp.insert(0,"1")
ent_phase.insert(0,"0")
ent_freq_2.insert(0,"1")
ent_amp_2.insert(0,"1")
ent_phase_2.insert(0,"0")
ent_phase_off.insert(0,"90")

param = cmnd.CoilParams(ent_freq,ent_amp,ent_phase,ent_freq_2,ent_amp_2,ent_phase_2,ent_phase_off)


var_bind_coils = tk.BooleanVar()
var_signal_type = tk.StringVar()
signal_list = [
    "sine",
    "square",
    "triangle",
    "sawtooth"
]
var_signal_type.set(signal_list[0])

cb_bind_coils = tk.Checkbutton(
    master = frm_labels,
    text = "Bind coils",
    variable = var_bind_coils,
    onvalue= True,
    offvalue= False,
    anchor="c",
    command=lambda: toggle_bind()
)

# placement of the varios components
frm_labels.place(x=5,y=5)
lbl_x.grid(row=0,columnspan=2)
lbl_freq.grid(row=1,column=0)
lbl_amp.grid(row=2,column=0)
lbl_phase.grid(row=3,column=0)
lbl_phase_off.grid(row=4,column=0)

cb_bind_coils.grid(row=4,column=2,columnspan=2)

ent_freq.grid(row=1,column=1)
ent_amp.grid(row=2,column=1)
ent_phase.grid(row=3,column=1)
ent_phase_off.grid(row=4,column=1)

lbl_y.grid(row=0,column=2,columnspan=2)
lbl_freq_2.grid(row=1,column=2)
lbl_amp_2.grid(row=2,column=2)
lbl_phase_2.grid(row=3,column=2)

ent_freq_2.grid(row=1,column=3)
ent_amp_2.grid(row=2,column=3)
ent_phase_2.grid(row=3,column=3)

# puts together the window which encloses the parameters below
frm_labels.update()


frm_cam_btn.place(x=630,y=5)
lbl_cam_fps.grid(row=0,column=0)
lbl_cam_exp.grid(row=1,column=0)

frm_cam_btn.update()

frm_cam_img.place(x=630,y=180)
lbl_cam_img.pack()
frm_cam_img.update()
### Buttons
drop_signal = tk.OptionMenu(window, var_signal_type, *signal_list)


## Start /Stop button
btn_start = tk.Button(
    master=window,
    text="Start",
    width=12,
    height = 4,
    bg="#aafaaa",
    command=lambda:start_stop()
)
btn_start.place(x=340, y=50)
cmnd.CreateToolTip(btn_start, text =
                 'Nospiežot "Start" tiks nomainīta frekvence, amplitūda \n '
                 'un fāzes pēc tā, kas būs lauciņos norādīts,\n'
                 'padarot pogu "Update plot" par bezjēdzīgu.  \n'
                 'Sāksies grafika animācija. ',text2='Grafika animācija tiks apturēta! \n'
                 'Vai tu tiešām esi gatavs apturēt animāciju?')
btn_start.update()
drop_signal.place(x=340, y=12)


btn_record = tk.Button(
    master=window,
    text="Start \nrecording",
    width=8,
    height = 3,
    bg="#aafaaa",
    command=lambda:toggle_cam(cam)
)
btn_record.place(x=630, y=frm_cam_btn.winfo_height()+10)

cmnd.CreateToolTip(btn_record, text =
                 'Sāk bilžu uzņemšanu bildes nesaglabājot. \n'
                 ,text2='Beidz rādīt kameras attēlu'
                 )

btn_record.update()

btn_show = tk.Button(
    master=window,
    text="Show \nimage",
    width=8,
    height = 3,
    bg="#aafaaa",
    # command=lambda:cmnd.update_image(cam.grab(),lbl_cam_img)
)
btn_show.place(x=708, y=frm_cam_btn.winfo_height()+10)
cmnd.CreateToolTip(btn_show, text =
                 'Poga!!!'
                 )

btn_show.update()

btn_calib = tk.Button(
    master=window,
    text="Calibrate",
    width=8,
    height = 3,
    bg="#aafaaa",
    command=lambda:open_calib_window(cam)
)
btn_calib.place(x=785, y=frm_cam_btn.winfo_height()+10)
cmnd.CreateToolTip(btn_calib, text =
                 'Poga!!!'
                 )

btn_calib.update()

### Functions that need global variables to function ###

### Do not move to a diferent folder ###


# Remake of the start stop button
def start_stop():
    global anim_running
    global param
    if anim_running:
        anim_running = False
        btn_start["text"] = "Start"
        btn_start["bg"] = "#aafaaa"
        # ani.event_source.stop()
        param.amp_x = 0
        param.amp_y = 0
        param.squeeze()

    else:
        anim_running = True
        btn_start["text"] = "Stop"
        btn_start["bg"] = "#faaaaa"
        # ani.event_source.start()
        upd_param(lissajous_canvas)

def toggle_bind():
    if var_bind_coils.get():
        # print("izslēdz entries")
        ent_amp_2.config(state="disable")
        ent_freq_2.config(state="disable")
        ent_phase_2.config(state="disable")
        ent_phase_off.config(state="normal")
    else:
        # print("ieslēdz entries")
        ent_amp_2.config(state="normal")
        ent_freq_2.config(state="normal")
        ent_phase_2.config(state="normal")
        ent_phase_off.config(state="disable")
cb_bind_coils.invoke()

def toggle_cam(cam):
    global cam_running
    if cam_running:
        # cam.stop_capture()
        btn_record["text"] = "Start \nrecording"
        btn_record["bg"] = "#aafaaa"
    else:
        # cam.start_capture()
        btn_record["text"] = "Stop \nrecording"
        btn_record["bg"] = "#faaaaa"
    cam_running = not cam_running


def open_calib_window(cam):
    global num_of_calib_images
    num_of_calib_images = 0
    images = []
    top= tk.Toplevel(window)
    top.geometry("750x350")
    top.title("Camera calibration")
    # n = 0

    lbl_top_num = tk.Label(
        master=top,
        text="Number of pictures: 0",
        anchor="w",
        width=40,
        height=3
    )
    lbl_top_num.place(x=180,y=10)
    lbl_top_num.update()

    lbl_top_img = tk.Label(
        master=top,
    )
    lbl_top_img.place(x=10,y=100)

    btn_top_show = tk.Button(
        master=top,
        text="Take calibration picture",
        width=20,
        height = 3,
        bg="#aafaaa",
        command=lambda:[take_calib_pics(cam,lbl_top_num)]#, cmnd.update_image(cam.grab(),lbl_top_img)]
    )
    btn_top_show.place(x=10,y=10)
    # lbl_top_num.update()
    btn_top_show.update()

def take_calib_pics(cam,label):
    # img = cam.grab()
    # chessboard.add_image(img)
    global num_of_calib_images
    num_of_calib_images = num_of_calib_images+1
    label.config(text = "Number of pictures: "+str(num_of_calib_images))




def calibrate():
    for i in num_of_calib_images:
        # cb.add_image(cam.grab())
        time.sleep(1)
    ret, mtx, dist, _, _ =  chessboard.calibrate()



### Making the plot  ###
# making the background to the plot
plot_canvas = tk.Canvas(
    master=window,
    height=600,
    width=600,
    background="#fafafa"
)

# the figure
fig = Figure(figsize = (10, 10), dpi = 50)
x = [0]
y = [0]
tm = [0]
plot1 = fig.add_subplot(111)
plot1.set_xlim(-5, 0)
line1, = plot1.plot(tm,x)
line2, = plot1.plot(tm,y)


canvas = FigureCanvasTkAgg(
    fig,
    master = plot_canvas
)
canvas.draw()
canvas.get_tk_widget().pack()

# toolbar = NavigationToolbar2Tk(
#     canvas,
#     plot_canvas
# )
# toolbar.update()

#canvas.get_tk_widget().pack()

### lissajous grafiks ###
# canvas
lissajous_plot_canvas = tk.Canvas(
    master=window,
    height=150,
    width=150,
    background="#fafafa"
)

# the figure
lissajous_fig = Figure(figsize = (2, 2), dpi = 100)

lissajous_plot = lissajous_fig.add_subplot(111)

lissajous_line, =lissajous_plot.plot(x,y)
lissajous_fig.subplots_adjust(left=0.25, right=0.75, top=0.75, bottom=0.25)


lissajous_canvas = FigureCanvasTkAgg(
    lissajous_fig,
    master = lissajous_plot_canvas
)
lissajous_canvas.draw()
lissajous_canvas.get_tk_widget().pack()

def animate(i):

    # parametri, kas vajadzīgi grafikam

    t = np.around(dt*i/1000,3)
    t = (time.time_ns()-time_start)/1e9
    tm.append(t)
    x_new,y_new = cmnd.generate_signal(param.values, t,var_bind_coils.get(),var_signal_type.get())
    x.append(x_new)
    y.append(y_new)

    #limiti grafikiem
    y_test = y[int(-5000/dt):]
    y_lim =max(-np.min(y_test),np.max(y_test))*1.2
    x_lim =max(-np.min(x[int(-5000/dt):]),np.max(x[int(-5000/dt):]))*1.2

    x_lim =max(x_lim,0.5)
    y_lim =max(y_lim,0.5)
    lim_lissajous = max(x_lim,y_lim)
    #Grafika dzīvā animācija

    plot1.set_xlim(tm[-1]-5,tm[-1])
    plot1.set_ylim(-lim_lissajous,lim_lissajous)

    line1.set_data(tm[int(-5000/dt):],x[int(-5000/dt):])
    line2.set_data(tm[int(-5000/dt):],y[int(-5000/dt):])



    #lissajous grafika dzīvā animācija

    lissajous_plot.set_xlim(-lim_lissajous,lim_lissajous)
    lissajous_plot.set_ylim(-lim_lissajous, lim_lissajous)
    lissajous_line.set_data(x[int(-500/dt):],y[int(-500/dt):])



def upd_param(lissajous_canvas):
    ################### ŠĪĪĪĪĪĪĪ ##############
    param.update()


ani = anim.FuncAnimation(fig, animate, interval=dt, blit=False)
lissajous_ani = anim.FuncAnimation(lissajous_fig, animate, interval=dt, blit=False)


plot_canvas.place(x=20, y=155)
lissajous_plot_canvas.place(x=620, y=155)
#lissajous_plot_canvas.update()
#Bplot_canvas.update()

# tkinter.ttk.Separator(master=window,orient=tk.VERTICAL).pack(fill="y")


#Camera stuff
cam = 5#Camera(fps,exposure)


window.mainloop()