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

def check_num(num):
    # ----------------------------------
    # Outputs true if num can be converted to float
    # ----------------------------------
    try:
        float(num)
        return True
    except ValueError:
        return False

def sine_wave(freq,amp,phase,time):
    # ----------------------------------
    # Generete sin from parameters
    # ----------------------------------
    return amp * np.sin(time*freq*2*np.pi + phase)

def square_wave(freq,amp,phase,time):
    # ----------------------------------
    # Generate square wave from parameters
    # ----------------------------------
    T = 1/freq
    phase = phase/2/np.pi*T
    t_spec = np.mod(time+phase,T)

    if(t_spec<=T/2):
        return amp
    else:
        return -amp

def triangle_wave(freq,amp,phase,time):
    # ----------------------------------
    # Generate triangle wave from parameters
    # ----------------------------------
    T = 1/freq
    phase = phase/2/np.pi*T
    t_spec = np.mod(time+phase,T)
    if t_spec<T/2:
        return amp - 2*amp*(t_spec*2/T)
    else:
        return -amp + 2*amp*((t_spec-T/2)*2/T)
    
def sawtooth_wave(freq,amp,phase,time):
    # ----------------------------------
    # Generate sawtooth wave from parameters
    # ----------------------------------
    T = 1/freq
    phase = phase/2/np.pi*T
    t_spec = np.mod(time+phase,T)
    return -amp + 2*amp*(t_spec/T)


def generate_signal(values,time,is_bound,signal_type):
    # ----------------------------------
    # Generates appropriate signal
    # Note: if freq=0, it uses a sin function, since other waves don't work for freq=0
    # ----------------------------------
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
    # ----------------------------------
    # Clears canvas
    # ----------------------------------
    for child in canvas.winfo_children():
        child.destroy()



class CoilParams():
    # ----------------------------------
    # Object that stores all coil parameters and reads values from entries
    # Used to avoid excessive use of global parameters
    # ----------------------------------

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
        # ----------------------------------
        # Reads values from entries and saves them
        # ----------------------------------
        for i in range(0,len(self.entries)):
            if check_num(self.entries[i].get()):
                self.values[i] = float(self.entries[i].get())
        [self.freq_x, self.amp_x, self.phase_x, self.freq_y, self.amp_y, self.phase_y, self.phase_off] = self.values

    def squeeze(self):
        # ----------------------------------
        # Puts values back in the list, in case specific values have to be changed manually (such as setting amp=0 when signal is turned off)
        # ----------------------------------
        self.values = [self.freq_x, self.amp_x, self.phase_x, self.freq_y, self.amp_y, self.phase_y, self.phase_off]


class ToolTip(object):
    # ----------------------------------
    # Object that shows tooltips when hovering over certain elements in GUI (buttons, labels, ect.)
    # ----------------------------------
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
