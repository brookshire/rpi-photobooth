from Tkinter import *

class BoothDisplay:
    root = None
    font = "Courier"
    font_size = 46

    def __init__(self):
        self.root = Tk()
        self.root.configure(background="black")
        self.parent = Frame(root)
        self.root.overrideredirect(True)
        self.root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(), root.winfo_screenheight()))
        self.root.focus_set()
        # self.root.bind("<Escape>", lambda e: e.widget.quit())

    def display(self):
        self.parent.pack(expand=1)

    def displayReadyMessage(self):
        msg = Label(self.parent,
                    text="Push the Red Button",
                    anchor=CENTER,
                    justify=CENTER,
                    fg="white",
                    bg="black",
                    font=(self.font, self.font_size)).pack()

