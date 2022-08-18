import numpy as np

def sine(t, amp, freq, phase):
    return amp * np.sin(freq * t + phase)