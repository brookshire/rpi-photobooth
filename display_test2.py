#!/usr/bin/python

from Tkinter import *

if __name__ == '__main__':
    root = Tk()
    parent = Frame(root)
    w = Label(parent, text="Push the Red Button",
              anchor=CENTER,
              justify=CENTER,
              fg="white",
              bg="black",
              font=("Courier", 46)).pack()
    root.overrideredirect(True)
    root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(), root.winfo_screenheight()))
    root.focus_set()  # <-- move focus to this widget
    root.bind("<Escape>", lambda e: e.widget.quit())

    parent.pack(expand=1)

    root.mainloop()

    parent = Frame(root)
    w2 = Label(parent, text="DON'T Push the Red Button",
              anchor=CENTER,
              justify=CENTER,
              fg="white",
              bg="black",
              font=("Courier", 46)).pack()
    root.overrideredirect(True)
    root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(), root.winfo_screenheight()))
    root.focus_set()  # <-- move focus to this widget
    root.bind("<Escape>", lambda e: e.widget.destroy())
    parent.pack(expand=1)

