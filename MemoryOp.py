import Tkinter as Tk
import math as math
import operator


class MemoryOp(object):
    def __init__(self, master, width, height, arrow_width, border):
        self.height = height * 6 / 17
        self.width = width * 3 / 18
        self.master = master
        self.arrow_width = arrow_width
        self.memop_canvas = Tk.Canvas(master, bg="white", width=self.width, height=self.height, bd=border,
                                      highlightthickness=border)
        self.memop_canvas.grid(row=5, column=3, rowspan=6, columnspan=3)

        self.entry_width = self.width - arrow_width
        self.switch_animation_done = True
        self.switch_done = Tk.BooleanVar()
        self.color_blink_done = Tk.BooleanVar()
        self.flow_done = Tk.BooleanVar()

        self.switch_state = 0
        self.target_state = None
        self.switch_length = 8 * arrow_width
        load_text = self.memop_canvas.create_text(self.width * 2 / 5, self.height * 5 / 16,
                                                  font=('Helvetica', self.height / 15), text='LOAD')
        store_text = self.memop_canvas.create_text(self.width * 2 / 5, self.height * 5 / 8,
                                                   font=('Helvetica', self.height / 15), text='STORE')
        load_coords = self.memop_canvas.coords(load_text)
        store_coords = self.memop_canvas.coords(store_text)
        self.load_box = self.memop_canvas.create_rectangle(load_coords[0] - self.width / 4,
                                                           load_coords[1] - self.height / 10,
                                                           load_coords[0] + self.width / 4,
                                                           load_coords[1] + self.height / 10)
        self.store_box = self.memop_canvas.create_rectangle(store_coords[0] - self.width / 4,
                                                            store_coords[1] - self.height / 10,
                                                            store_coords[0] + self.width / 4,
                                                            store_coords[1] + self.height / 10)

        self.lines = [[] for i in range(7)]
        self.create_line(self.entry_width, 0, self.entry_width, self.height * 15 / 32, 0, 10, 0)
        self.create_line(self.entry_width, self.height * 15 / 32, self.width - 3 * arrow_width, self.height * 15 / 32,
                         10, 0, 1)

        self.memop_canvas.create_oval(self.width - 5 * arrow_width, self.height * 15 / 32 - arrow_width,
                                      self.width - 3 * arrow_width, self.height * 15 / 32 + arrow_width)

        end_x = (self.width - 5 * arrow_width) + self.switch_length * math.cos(math.radians(215))
        end_y_load = (self.height * 15 / 32) + self.switch_length * math.sin(math.radians(215))
        end_y_store = (self.height * 15 / 32) + self.switch_length * math.sin(math.radians(145))
        self.memop_switch = self.memop_canvas.create_line(self.width - 5 * arrow_width, self.height * 15 / 32, end_x,
                                                          end_y_load, width=arrow_width, tags='frame')

        load_box_coords = self.memop_canvas.coords(self.load_box)
        self.create_line(end_x, (load_box_coords[3] + load_box_coords[1]) / 2, end_x, end_y_load, 0, 10, 2)
        self.create_line(load_box_coords[2], (load_box_coords[3] + load_box_coords[1]) / 2, end_x,
                         (load_box_coords[3] + load_box_coords[1]) / 2, 10, 0, 3)

        store_box_coords = self.memop_canvas.coords(self.store_box)
        self.create_line(end_x, (store_box_coords[3] + store_box_coords[1]) / 2, end_x, end_y_store, 0, 10, 4)
        self.create_line(store_box_coords[2], (store_box_coords[3] + store_box_coords[1]) / 2, end_x,
                         (store_box_coords[3] + store_box_coords[1]) / 2, 10, 0, 5)

        self.switch_text = self.memop_canvas.create_text(end_x - 2 * arrow_width, (end_y_load + end_y_store) / 2,
                                                         text='0', anchor=Tk.E, font=('Helvetica', 10))
        self.memop_canvas.create_text(end_x - 5 * arrow_width, (end_y_load + end_y_store) / 2, text='t2 = ',
                                      anchor=Tk.E, font=('Helvetica', 10))

        self.memop_canvas.tag_raise(load_text)
        self.memop_canvas.tag_raise(store_text)
        self.current_box = self.load_box
        self.color = None
        self.direction = None
        self.flow_animation_done = False
        self.cable_color = 'red'
        self.current_line = 0
        self.iterator = iter(self.lines[self.current_line])

    def set_switch(self, target):
        self.target_state = target
        self.switch_done.set(0)
        self.animate_switch()

    def toggle_blink(self):
        self.direction = 'SOLIDIFY'
        self.color = 0xfff
        self.color_blink_done.set(0)
        self.animate_color_blink()
        if self.color_blink_done.get() == 0:
            self.master.wait_variable(self.color_blink_done)


    def set_flow(self, color):
        self.cable_color = color
        if color == 'black':
            for line in self.lines:
                for line_fragment in line:
                    self.memop_canvas.itemconfigure(line_fragment, fill=self.cable_color)
            self.memop_canvas.itemconfigure(self.memop_switch, fill=self.cable_color)
            self.flow_done.set(1)
        else:
            self.flow_done.set(0)
            self.animate_flow()
            if self.flow_done.get() == 0:
                self.master.wait_variable(self.flow_done)


    def create_line(self, start_width, start_height, end_width, end_height, seg_len_w, seg_len_h, index):
        i = 0
        j = 0
        while abs(i + seg_len_w) <= end_width - start_width and abs(j + seg_len_h) <= end_height - start_height:
            self.lines[index].append(self.memop_canvas.create_line(start_width + i, start_height + j,
                                                                   start_width + (i + seg_len_w),
                                                                   start_height + (j + seg_len_h), width=self.arrow_width))
            i += seg_len_w
            j += seg_len_h
        self.lines[index].append(
            self.memop_canvas.create_line(start_width + i, start_height + j, end_width, end_height, width=self.arrow_width))

    def next_line(self):
        reverse = False
        if self.current_line == 0:
            reverse = True
            self.current_line = 1
        elif self.current_line == 1:
            reverse = True
            if self.switch_state == 0:
                self.current_line = 2
            else:
                self.current_line = 4
            self.memop_canvas.itemconfigure(self.memop_switch, fill=self.cable_color)
        elif self.current_line == 2:
            reverse = True
            self.current_line = 3
        elif self.current_line == 4:
            reverse = True
            self.current_line = 5
        elif self.current_line == 3 or self.current_line == 5:
            self.current_line = 0
            self.flow_done.set(1)
        if reverse:
            self.iterator = iter(reversed(self.lines[self.current_line]))
        else:
            self.iterator = iter(self.lines[self.current_line])

    def rotate_switch(self, length, target_angle, op, speed, quadrant):
        current = self.memop_canvas.coords(self.memop_switch)
        current_acos = math.degrees(math.acos((current[2] - current[0]) / length))
        current_asin = math.degrees(math.asin((current[3] - current[1]) / length))
        if current_asin < 0:
            current_angle = 360 - current_acos
        else:
            current_angle = current_acos
        new_angle = current_angle + speed
        end_x = current[0] + length * math.cos(math.radians(new_angle))
        end_y = current[1] + length * math.sin(math.radians(new_angle))
        self.memop_canvas.coords(self.memop_switch, current[0], current[1], end_x, end_y)
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
            self.memop_canvas.itemconfigure(self.switch_text, text='%d' % self.target_state)
            if self.switch_state == 0:
                self.current_box = self.load_box
            else:
                self.current_box = self.store_box

    def animate_switch(self):
        if self.switch_state < self.target_state:
            self.switch_animation_done = False
            self.rotate_switch(self.switch_length, 35, operator.gt, -1, 2)
        elif self.switch_state > self.target_state:
            self.switch_animation_done = False
            self.rotate_switch(self.switch_length, -35, operator.lt, 1, 3)

        if not self.switch_animation_done:
            self.switch_animation_done = True
            self.master.after(5, self.animate_switch)
        else:
            self.switch_done.set(1)

    def animate_color_blink(self):
        color = '#' + str(hex(self.color))[2:5]
        self.memop_canvas.itemconfigure(self.current_box, fill=color)
        if self.direction == 'SOLIDIFY':
            self.color -= 0x101
            if self.color <= 0x9f9:
                self.direction = 'FADE'
            self.master.after(30, self.animate_color_blink)

        elif self.direction == 'FADE':
            self.color += 0x101
            if self.color > 0xfff:
                self.color_blink_done.set(1)
            else:
                self.master.after(30, self.animate_color_blink)

    def animate_flow(self):
        try:
            self.memop_canvas.itemconfigure(next(self.iterator), fill=self.cable_color)
            self.master.after(3, self.animate_flow)
        except StopIteration:
            self.next_line()
            if self.flow_done.get() == 0:
                self.master.after(3, self.animate_flow)
