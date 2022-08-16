import tkinter as tk

def btn_test(label):
    n = label["text"]
    label["text"] = str(int(n)+1)

    label.update()