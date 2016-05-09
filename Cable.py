import Tkinter as Tk
import math as math
import operator


class Cable(object):
    def __init__(self, master, width, height, arrow_width, border, exit_width_processor, exit_width_memop,
                 entry_height_wheel):
        self.height = height * 3 / 17
        self.width = width * 10 / 18
        self.master = master
        self.arrow_width = arrow_width
        self.switch_length = 8 * arrow_width

        self.cable_canvas = Tk.Canvas(master, bg="white", width=self.width, height=self.height, bd=border,
                                      highlightthickness=border)
        self.cable_canvas.grid(row=2, column=3, rowspan=3, columnspan=10)

        self.switch_done = Tk.BooleanVar()
        self.flow_done = Tk.BooleanVar()
        self.switch_state = 0
        self.target_state = None
        self.switch_animation_done = True
        self.lines = [[] for i in range(10)]
        self.color = 'red'
        self.create_line(self.width * 4 / 5, entry_height_wheel, self.width,
                         entry_height_wheel, 10, 0, 0)

        self.create_line(self.width * 4 / 5, entry_height_wheel, self.width * 4 / 5, self.height / 3,
                         0, 10, 8)
        self.create_line(self.width / 2, self.height / 3, self.width * 4 / 5, self.height / 3, 10, 0, 9)

        self.create_line(self.width / 2, self.height / 3, self.width / 2, self.height / 3 + 4 * arrow_width, 0, 10, 1)

        self.current_line = 0
        self.iterator = iter(reversed(self.lines[self.current_line]))

        self.cable_canvas.create_oval(self.width / 2 - arrow_width, self.height / 3 + 4 * arrow_width,
                                      self.width / 2 + arrow_width, self.height / 3 + 6 * arrow_width)

        end_x_memop = (self.width / 2) + self.switch_length * math.cos(math.radians(135))
        end_x_processor = (self.width / 2) + self.switch_length * math.cos(math.radians(55))
        end_y = (self.height / 3 + 6 * arrow_width) + self.switch_length * math.sin(math.radians(135))
        self.cable_switch = self.cable_canvas.create_line(self.width / 2, self.height / 3 + 6 * arrow_width,
                                                          end_x_processor, end_y, width=arrow_width)

        self.create_line(end_x_memop, end_y, end_x_memop, end_y + 3 * arrow_width, 0, 10, 2)
        self.create_line(end_x_processor, end_y, end_x_processor, end_y + 3 * arrow_width, 0, 10, 3)

        self.create_line(exit_width_memop, end_y + 3 * arrow_width, end_x_memop, end_y + 3 * arrow_width, 10, 0, 4)
        self.create_line(end_x_processor, end_y + 3 * arrow_width,
                         exit_width_processor[0] + self.width * 3 / 10, end_y + 3 * arrow_width, 10, 0, 5)

        self.create_line(exit_width_memop, end_y + 3 * arrow_width, exit_width_memop, self.height, 0, 10, 6,)
        self.create_line(exit_width_processor[0] + self.width * 3 / 10, end_y + 3 * arrow_width,
                         exit_width_processor[0] + self.width * 3 / 10, self.height, 0, 10, 7)

        switch_coords = self.cable_canvas.coords(self.cable_switch)
        self.cable_canvas.create_text(switch_coords[0] - 8 * arrow_width, switch_coords[1] + arrow_width, text='t1 = ',
                                      anchor=Tk.E)
        self.switch_text = self.cable_canvas.create_text(switch_coords[0] - 6 * arrow_width,
                                                         switch_coords[1] + arrow_width, text='0', anchor=Tk.E)

    def create_line(self, start_width, start_height, end_width, end_height, seg_len_w, seg_len_h, index):
        i = 0
        j = 0
        while abs(i + seg_len_w) <= end_width - start_width and abs(j + seg_len_h) <= end_height - start_height:
            self.lines[index].append(self.cable_canvas.create_line(start_width + i, start_height + j,
                                                                   start_width + (i + seg_len_w),
                                                                   start_height + (j + seg_len_h), width=self.arrow_width))
            i += seg_len_w
            j += seg_len_h
        self.lines[index].append(
            self.cable_canvas.create_line(start_width + i, start_height + j, end_width, end_height, width=self.arrow_width))

    def set_switch(self, target):
        self.target_state = target
        self.switch_done.set(0)
        self.animate_switch()

    def set_flow(self, color):
        self.color = color
        self.flow_done.set(0)
        self.animate_flow()
        if self.flow_done.get() == 0:
            self.master.wait_variable(self.flow_done)

    def rotate_switch(self, length, target_angle, op, speed, quadrant):
        current = self.cable_canvas.coords(self.cable_switch)
        current_acos = math.degrees(math.acos((current[2] - current[0]) / length))
        current_asin = math.degrees(math.asin((current[3] - current[1]) / length))
        if current_asin < 0:
            current_angle = 360 - current_acos
        else:
            current_angle = current_acos
        new_angle = current_angle + speed
        end_x = current[0] + length * math.cos(math.radians(new_angle))
        end_y = current[1] + length * math.sin(math.radians(new_angle))
        self.cable_canvas.coords(self.cable_switch, current[0], current[1], end_x, end_y)
        if current_asin > 0 and (90 > current_acos > 0):
            current_quadrant = 1
        elif current_asin > 0 and (180 > current_acos > 90):
            current_quadrant = 2
        elif current_asin < 0 and (180 > current_acos > 90):
            current_quadrant = 3
        elif current_asin < 0 and (90 > current_acos > 0):
            current_quadrant = 4
        else:
            current_quadrant = 0
        if quadrant == current_quadrant and op(current_asin, target_angle):
            self.switch_state = self.target_state
            self.cable_canvas.itemconfigure(self.switch_text, text='%d' % self.target_state)

    def next_line(self):
        reverse = False
        if self.current_line == 0:
            reverse = True
            self.current_line = 8
        elif self.current_line == 8:
            reverse = True
            self.current_line = 9
        elif self.current_line == 9:
            self.current_line = 1
        elif self.current_line == 1:
            if self.switch_state == 1:
                self.current_line = 2
            else:
                self.current_line = 3
            self.cable_canvas.itemconfigure(self.cable_switch, fill=self.color)
        elif self.current_line == 2:
            self.current_line = 4
            reverse = True
        elif self.current_line == 3:
            self.current_line = 5
        elif self.current_line == 4:
            self.current_line = 6
        elif self.current_line == 5:
            self.current_line = 7
        elif self.current_line in (6, 7):
            self.current_line = 0
            reverse = True
            self.flow_done.set(1)
        if reverse:
            self.iterator = iter(reversed(self.lines[self.current_line]))
        else:
            self.iterator = iter(self.lines[self.current_line])

    def animate_switch(self):
        if self.switch_state < self.target_state:
            self.switch_animation_done = False
            self.rotate_switch(self.switch_length, 55, operator.lt, 1, 2)
        elif self.switch_state > self.target_state:
            self.switch_animation_done = False
            self.rotate_switch(self.switch_length, 55, operator.lt, -1, 1)

        if not self.switch_animation_done:
            self.switch_animation_done = True
            self.master.after(10, self.animate_switch)
        else:
            self.switch_done.set(1)

    def animate_flow(self):
        try:
            self.cable_canvas.itemconfigure(next(self.iterator), fill=self.color)
            self.master.after(20, self.animate_flow)
        except StopIteration:
            self.next_line()
            if self.flow_done.get() == 0:
                self.master.after(20, self.animate_flow)
