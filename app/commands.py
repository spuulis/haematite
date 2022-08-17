import tkinter as tk
import numpy as np

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

def get_values(amp, freq, phase):
    if(check_num(amp) and check_num(freq) and check_num(phase)):
        x = np.linspace(0, 5,1001)
        y = float(amp) * np.sin(x*float(freq)*2*np.pi+float(phase))
        return(x,y)
    else:
        return([1],[1])

def next_sin_val(amp, freq, phase, time):
    if(check_num(amp) and check_num(freq) and check_num(phase)):
        return float(amp) * np.sin(time*float(freq)*2*np.pi+float(phase))
    else:
        return 0.0

        