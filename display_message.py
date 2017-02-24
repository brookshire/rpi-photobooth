#!/usr/bin/python

from Tkinter import *
from boothconfig import *

root = Tk()

root.configure(background=background_color)

parent = Frame(root, bg=background_color)

push_label = Label(parent, text="Push the Red Button",
                   anchor=CENTER,
                   justify=CENTER,
                   fg=main_text_color,
                   bg=background_color,
                   font=("Courier", 46)).pack()
wait_label = Label(parent, text="Then wait {0} seconds".format(button_delay),
                   anchor=CENTER,
                   justify=CENTER,
                   fg=ans_text_color,
                   bg=background_color,
                   font=("Courier", 36)).pack()

if upload_images:
    upload_label = Label(parent, text="Picture will be uploaded to",
                        anchor=CENTER,
                       justify=CENTER,
                       fg=ans_text_color,
                       bg=background_color,
                       font=("Courier", 20)).pack()
    upload2_label = Label(parent, text=remote_url,
                          anchor=CENTER,
                          justify=CENTER,
                          fg=ans_text_color,
                          bg=background_color,
                          font=("Courier", 20)).pack()

root.overrideredirect(True)
root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(), root.winfo_screenheight()))
root.focus_set()  # <-- move focus to this widget
root.bind("<Escape>", lambda e: e.widget.quit())
parent.pack(expand=1)

root.mainloop()