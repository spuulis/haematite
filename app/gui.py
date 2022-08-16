import tkinter as tk
import commands as cmnd
# from visual.calibration import chessboard
# import visual.tracker
 

window = tk.Tk()
# window.geometry("800x800")
window.configure(background = "grey")
window.title("Pagraba spoles")
window.resizable(True, True)

frame = tk.Frame(
    master=window,
    relief=tk.RAISED,
    borderwidth=5
)


label = tk.Label(
    master=frame,
    text="0"
)

button = tk.Button(
    master=frame,
    text="count up",
    width=10,
    height=2,
    bg="#fafafa",
    command=lambda: cmnd.btn_test(label)
)

button.pack()
label.pack()

window.update_idletasks()

frame.place(x=20, y=20)
window.mainloop()