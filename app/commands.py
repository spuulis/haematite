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
