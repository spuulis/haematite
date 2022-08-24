import tkinter as tk
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure
import matplotlib.animation as anim
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,
NavigationToolbar2Tk)
from matplotlib import style
from PIL import ImageTk, Image
import sys

# from ..visual.camera import Camera
def fnc_lblUpdate(label):
    n = label["text"]
    label["text"] = str(int(n)+1)

    label.update()

def check_num(num):
    try:
        float(num)
        return True
    except ValueError:
        return False

def get_values(amp, freq, phase, phase_off):
    if(check_num(amp) and check_num(freq) and check_num(phase) and check_num(phase_off)):
        x = np.linspace(0, 5,1001)

        y = float(amp) * np.sin(x*float(freq)*2*np.pi+float(phase))
        return(x,y)
    else:
        return([1],[1])

def next_sin_val(amp, freq, phase, phase_off, time):
    if(check_num(amp) and check_num(freq) and check_num(phase) and check_num(phase_off)):
        phase = np.deg2rad(float(phase))
        phase_off = np.deg2rad(float(phase_off))
        return (float(amp) * np.sin(time*float(freq)*2*np.pi+phase),float(amp) * np.sin(time*float(freq)*2*np.pi+phase+phase_off))
    else:
        return 0.0

# def sines(freq_x,amp_x,phase_x,freq_y,amp_y,phase_y,phase_off,time,is_bound):
    

#     x = amp_x * np.sin(time*freq_x*2*np.pi+phase_x)
#     if is_bound:
#         y = amp_x * np.sin(time*freq_x*2*np.pi+phase_x + phase_off)
        
#     else:
#         y = amp_y * np.sin(time*freq_y*2*np.pi+phase_y)
        

#     return x,y


def sine_wave(freq,amp,phase,time):
    return amp * np.sin(time*freq*2*np.pi + phase)

def square_wave(freq,amp,phase,time):
    T = 1/freq
    phase = phase/2/np.pi*T
    t_spec = np.mod(time+phase,T)

    if(t_spec<=T/2):
        return amp
    else:
        return -amp

def triangle_wave(freq,amp,phase,time):
    T = 1/freq
    phase = phase/2/np.pi*T
    t_spec = np.mod(time+phase,T)
    if t_spec<T/2:
        return amp - 2*amp*(t_spec*2/T)
    else:
        return -amp + 2*amp*((t_spec-T/2)*2/T)
    
def sawtooth_wave(freq,amp,phase,time):
    T = 1/freq
    phase = phase/2/np.pi*T
    t_spec = np.mod(time+phase,T)
    return -amp + 2*amp*(t_spec/T)


def generate_signal(values,time,is_bound,signal_type):
    [freq_x,amp_x,phase_x,freq_y,amp_y,phase_y,phase_off] = values
    phase_x = np.deg2rad(phase_x)
    phase_y = np.deg2rad(phase_y)
    phase_off = np.deg2rad(phase_off)

    if is_bound:
        freq_y = freq_x
        amp_y = amp_x
        phase_y = phase_x + phase_off

    match signal_type:
        case "sine":
            x = sine_wave(freq_x,amp_x,phase_x,time)
            y = sine_wave(freq_y,amp_y,phase_y,time)
        case "square":
            if freq_x == 0:
                x = sine_wave(freq_x,amp_x,phase_x,time)
            else:
                x = square_wave(freq_x,amp_x,phase_x,time)
            if freq_y == 0:
                y = sine_wave(freq_y,amp_y,phase_y,time)
            else:
                y = square_wave(freq_y,amp_y,phase_y,time)
        case "triangle":
            if freq_x == 0:
                x = sine_wave(freq_x,amp_x,phase_x,time)
            else:
                x = triangle_wave(freq_x,amp_x,phase_x,time)
            if freq_y == 0:
                y = sine_wave(freq_y,amp_y,phase_y,time)
            else:
                y = triangle_wave(freq_y,amp_y,phase_y,time)
        case "sawtooth":
            if freq_x == 0:
                x = sine_wave(freq_x,amp_x,phase_x,time)
            else:
                x = sawtooth_wave(freq_x,amp_x,phase_x,time)
            if freq_y == 0:
                y = sine_wave(freq_y,amp_y,phase_y,time)
            else:
                y = sawtooth_wave(freq_y,amp_y,phase_y,time)
    return x, y


def clear_canvas(canvas):
    for child in canvas.winfo_children():
        child.destroy()

def update_image(image, label):
    img = Image.fromarray(image)
    # img_tk = ImageTK.PhotoImage()


# Tip text box that appears when hovering hovering
class CoilParams():

    def __init__(self,e_fx,e_ax,e_px,e_fy,e_ay,e_py,e_poff):
        self.amp_x = 0
        self.freq_x = 1
        self.phase_x = 1

        self.amp_y = 0
        self.freq_y = 1
        self.phase_y = 1

        self.phase_off = 90

        self.values = [self.freq_x, self.amp_x, self.phase_x, self.freq_y, self.amp_y, self.phase_y, self.phase_off]
        self.entries = [e_fx, e_ax, e_px, e_fy, e_ay, e_py, e_poff]

    def update(self):
        for i in range(0,len(self.entries)):
            if check_num(self.entries[i].get()):
                self.values[i] = float(self.entries[i].get())
        [self.freq_x, self.amp_x, self.phase_x, self.freq_y, self.amp_y, self.phase_y, self.phase_off] = self.values

    def squeeze(self):
        self.values = [self.freq_x, self.amp_x, self.phase_x, self.freq_y, self.amp_y, self.phase_y, self.phase_off]


class ToolTip(object):

    def __init__(self, widget):
        self.widget = widget
        self.tipwindow = None
        self.id = None
        self.x = self.y = 0
        #elf.comment_id=0

    def showtip(self, text,text2):
        #"Display text in tooltip window"
        # print(self.widget['bg'])
        if self.widget['bg'] == "#faaaaa":
            text=text2


        self.text = text
        if self.tipwindow or not self.text:
            return
        x, y, cx, cy = self.widget.bbox("insert")
        x = x + self.widget.winfo_rootx() + 57
        y = y + cy + self.widget.winfo_rooty() +27
        self.tipwindow = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(1)
        tw.wm_geometry("+%d+%d" % (x, y))
        label = tk.Label(tw, text=self.text,justify=tk.LEFT ,
                      background="#ffffe0", relief=tk.SOLID, borderwidth=1,
                      font=("tahoma", "8", "normal"))  #anchor='w'## justify=LEFT
        label.pack(ipadx=1)

    def hidetip(self):
        tw = self.tipwindow
        self.tipwindow = None
        if tw:
            tw.destroy()

def CreateToolTip(widget, text,text2="Error"):
    toolTip = ToolTip(widget)
    def enter(event):
        toolTip.showtip(text, text2)
    def leave(event):
        toolTip.hidetip()
    widget.bind('<Enter>', enter)
    widget.bind('<Leave>', leave)
