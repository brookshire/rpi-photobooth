#!/usr/bin/python

from Tkinter import *

root = Tk()

root.configure(background="black")

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