#!/usr/bin/env python
import tkinter as tk
from decida.Calc import Calc

root = tk.Tk()
fl = tk.Frame(root, bd=10, relief="raised", bg="red")
fr = tk.Frame(root, bd=10, relief="raised", bg="blue")
fl.pack(side="left")
fr.pack(side="right")
Calc(fl, wait=False)
Calc(fr, wait=True)
