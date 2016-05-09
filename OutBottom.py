import Tkinter as Tk


class OutBottom(object):

    def __init__(self, master, width, height,border,border_width):
        self.height = height * 1 / 17
        self.width = width * 16 / 18
        self.master = master

        self.out_bottom_canvas = Tk.Canvas(master, bg="white", width=self.width, height=self.height, bd=border, highlightthickness=border)
        self.out_bottom_canvas.grid(row=16, column=1, rowspan=1, columnspan=16)

        self.out_bottom_canvas.create_line(0,self.height / 2, self.width, self.height / 2,width=border_width)