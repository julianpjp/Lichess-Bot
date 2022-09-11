from tkinter import *
from tkinter.font import *
from typing import Sized

window = Tk()
doMoves = IntVar()
showMoves = IntVar()

class controls:

    def __init__(self):
        window.title("Game Control")
        window.geometry('300x120')
        Checkbutton(window, variable=doMoves, command=self.cb).grid(row=0, column=0, padx=15, pady=10)
        fontStyle = Font(family="Lucida Grande", size=13)
        Label(window, text='do moves', font=fontStyle).grid(row=0, column=1)

        Checkbutton(window, variable=showMoves, command=self.cb).grid(row=2, column=0, padx=5, pady=10)
        fontStyle = Font(family="Lucida Grande", size=12)
        Label(window, text='show moves', font=fontStyle).grid(row=2, column=1)
        return

    def cb(self):
        print ("variable is   ", doMoves.get())


controls()
window.mainloop()