#! /usr/bin/env python
from decida.Balloonhelp import Balloonhelp
import tkinter as tk

root = tk.Tk()
m = tk.Message(text="Hover on Button to show Balloonhelp, close window to quit")
m.pack(padx=10, pady=10)
b = tk.Button(text="OK", command=root.quit)
b.pack(padx=100, pady=100)
w = Balloonhelp(delay=100, background="#fcf87f", place="left", offset=3)
w.help_message(b, "display\n  tooltips")
root.mainloop()
