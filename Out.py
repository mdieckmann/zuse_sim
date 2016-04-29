import Tkinter as Tk


class Out(object):

    def __init__(self, master, width, height,border):
        self.height = height * 1 / 16
        self.width = width * 16 / 16
        self.master = master

        self.result_canvas = Tk.Canvas(master, bg="white", width=self.width, height=self.height, bd=border, highlightthickness=border)
        self.result_canvas.grid(row=0, column=0, rowspan=1, columnspan=16)