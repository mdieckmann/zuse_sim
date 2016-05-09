import Tkinter as Tk


class OutLeft(object):

    def __init__(self, master, width, height,border,border_width):
        self.height = height * 17 / 17
        self.width = width * 1 / 18
        self.master = master

        self.out_left_canvas = Tk.Canvas(master, bg="white", width=self.width, height=self.height, bd=border, highlightthickness=border)
        self.out_left_canvas.grid(row=0, column=0, rowspan=17, columnspan=1)

        self.out_left_canvas.create_line(self.width / 2,self.height / 34,self.width / 2,self.height * 33 / 34,width=border_width)
        self.out_left_canvas.create_line(self.width / 2,self.height / 34,self.width, self.height / 34,width=border_width)
        self.out_left_canvas.create_line(self.width / 2, self.height * 33 / 34, self.width,self.height * 33 / 34,width=border_width)
