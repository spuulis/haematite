import tkinter as tk
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure
import matplotlib.animation as anim
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,
NavigationToolbar2Tk)
from matplotlib import style
from PIL import Image#, ImageTK

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


def update_image(image, label):
    img = Image.fromarray(image)
    # img_tk = ImageTK.PhotoImage()

# Tip text box that appears when hovering hovering


class ToolTip(object):

    def __init__(self, widget):
        self.widget = widget
        self.tipwindow = None
        self.id = None
        self.x = self.y = 0
        #elf.comment_id=0

    def showtip(self, text,text2):
        #"Display text in tooltip window"
        #print(self.widget['bg'])
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
