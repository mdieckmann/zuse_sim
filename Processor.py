import Tkinter as Tk
import math as math
import operator


class Processor(object):
    def __init__(self, master, width, height, arrow_width, border):
        self.arrow_width = arrow_width
        self.font_size = 10

        self.height = height * 11 / 17
        self.width = width * 7 / 18
        self.master = master

        self.proc_canvas = Tk.Canvas(master, bg="white", width=self.width, height=self.height, bd=border,
                                     highlightthickness=border)
        self.proc_canvas.grid(row=5, column=6, rowspan=11, columnspan=7)

        self.entry_width = None
        self.exit_height = None
        self.switches = [None] * 7
        self.switch_states = [0] * 7
        self.target_states = [None] * 7
        self.switch_text = [None] * 7
        self.switch_length = 8 * arrow_width
        self.animation_done = True

        self.lines = [[] for i in range(32)]
        self.draw_processor(arrow_width)
        self.switch_done = Tk.BooleanVar()
        self.flow_done = Tk.BooleanVar()
        self.current_line = 0
        self.iterator = iter(self.lines[self.current_line])
        self.cable_color = 'red'

    def set_switch(self, target):
        self.target_states = target
        self.switch_done.set(0)
        self.animate_switch()

    def set_flow(self, color):
        self.cable_color = color
        self.flow_done.set(0)
        self.animate_flow()
        if self.flow_done.get() == 0:
            self.master.wait_variable(self.flow_done)


    def draw_processor(self, arrow_width):
        switch_length = 7.21 * arrow_width
        # vertical
        self.create_line(self.width * 2 / 5, self.height * 13 / 100, self.width * 2 / 5, self.height * 2 / 10, 0, 10, 0,
                         '', '')

        self.create_line(self.width * 2 / 5 - 4 * arrow_width, self.height * 2 / 10 + 8 * arrow_width,
                         self.width * 2 / 5 - 4 * arrow_width, self.height * 2 / 10 + 11 * arrow_width, 0, 10, 1, '',
                         '')
        self.create_line(self.width * 2 / 5 + 4 * arrow_width, self.height * 2 / 10 + 8 * arrow_width,
                         self.width * 2 / 5 + 4 * arrow_width, self.height * 2 / 10 + 11 * arrow_width, 0, 10, 2, '',
                         '')

        self.create_line(self.width * 1 / 10, self.height * 2 / 10 + 11 * arrow_width,
                         self.width * 1 / 10, self.height * 8 / 20, 0, 10, 3, '', '')

        self.create_line(self.width * 1 / 10, self.height * 8 / 20,
                         self.width * 1 / 10, self.height * 53 / 100, 0, 10, 30, '', '')

        self.create_line(self.width * 1 / 10, self.height * 53 / 100 + switch_length + 2 * arrow_width,
                         self.width * 1 / 10, self.height * 14 / 20, 0, 10, 4, '', '')
        self.create_line(self.width * 6 / 10, self.height * 8 / 20,
                         self.width * 6 / 10, self.height * 53 / 100 + switch_length - 6 * arrow_width, 0, 10, 5, '',
                         '')

        self.create_line(self.width * 7 / 10, self.height * 53 / 100,
                         self.width * 7 / 10, self.height * 8 / 20, 0, 10, 6, '', '')

        self.create_line(self.width * 7 / 10, self.height * 53 / 100 + switch_length + 2 * arrow_width,
                         self.width * 7 / 10, self.height * 14 / 20, 0, 10, 7, '', '')

        self.create_line(self.width * 9 / 10, self.height * 14 / 20,
                         self.width * 9 / 10, self.height * 18 / 20, 0, 10, 8, '', (7, 3))

        self.create_line(self.width * 2 / 10 + 8 * arrow_width, self.height * 8 / 20 - 7 * arrow_width,
                         self.width * 2 / 10 + 8 * arrow_width, self.height * 8 / 20 - 4 * arrow_width,
                         0, 10, 9, '', '')
        self.create_line(self.width * 2 / 10 + 8 * arrow_width, self.height * 8 / 20 + 7 * arrow_width,
                         self.width * 2 / 10 + 8 * arrow_width, self.height * 8 / 20 + 4 * arrow_width,
                         0, 10, 10, '', '')
        self.create_line(self.width * 9 / 20, self.height * 8 / 20 - 7 * arrow_width,
                         self.width * 9 / 20, self.height * 8 / 20 - 4 * arrow_width,
                         0, 10, 11, '', '')
        self.create_line(self.width * 9 / 20, self.height * 8 / 20 + 7 * arrow_width,
                         self.width * 9 / 20, self.height * 8 / 20 + 4 * arrow_width,
                         0, 10, 12, '', '')

        self.create_line(self.width * 2 / 10 + 8 * arrow_width, self.height * 14 / 20 - 7 * arrow_width,
                         self.width * 2 / 10 + 8 * arrow_width, self.height * 14 / 20 - 4 * arrow_width,
                         0, 10, 13, '', '')
        self.create_line(self.width * 2 / 10 + 8 * arrow_width, self.height * 14 / 20 + 7 * arrow_width,
                         self.width * 2 / 10 + 8 * arrow_width, self.height * 14 / 20 + 4 * arrow_width,
                         0, 10, 14, '', '')
        self.create_line(self.width * 9 / 20, self.height * 14 / 20 - 7 * arrow_width,
                         self.width * 9 / 20, self.height * 14 / 20 - 4 * arrow_width,
                         0, 10, 15, '', '')
        self.create_line(self.width * 9 / 20, self.height * 14 / 20 + 7 * arrow_width,
                         self.width * 9 / 20, self.height * 14 / 20 + 4 * arrow_width,
                         0, 10, 16, '', '')

        # horizontal

        self.create_line(self.width * 2 / 5 + 4 * arrow_width, self.height * 2 / 10 + 11 * arrow_width,
                         self.width * 6 / 10, self.height * 2 / 10 + 11 * arrow_width,
                         10, 0, 17, Tk.LAST, '')
        self.create_line(self.width * 1 / 10, self.height * 2 / 10 + 11 * arrow_width,
                         self.width * 2 / 5 - 4 * arrow_width, self.height * 2 / 10 + 11 * arrow_width,
                         10, 0, 18, '', '')

        self.create_line(self.width * 1 / 10, self.height * 8 / 20,
                         self.width * 2 / 10, self.height * 8 / 20, 10, 0, 19, '', '')

        self.create_line(self.width * 2 / 10 + 8 * arrow_width, self.height * 8 / 20 - 7 * arrow_width,
                         self.width * 9 / 20, self.height * 8 / 20 - 7 * arrow_width, 10, 0, 20, '', '')
        self.create_line(self.width * 2 / 10 + 8 * arrow_width, self.height * 8 / 20 + 7 * arrow_width,
                         self.width * 9 / 20, self.height * 8 / 20 + 7 * arrow_width, 10, 0, 21, '', '')

        self.create_line(self.width * 9 / 20 + 8 * arrow_width, self.height * 8 / 20,
                         self.width * 6 / 10, self.height * 8 / 20, 10, 0, 22, '', '')
        self.create_line(self.width * 6 / 10, self.height * 8 / 20,
                         self.width * 7 / 10, self.height * 8 / 20, 10, 0, 31, '', '')

        self.create_line(self.width * 1 / 10 + 4 * arrow_width,
                         self.height * 53 / 100 + switch_length - 6 * arrow_width,
                         self.width * 6 / 10, self.height * 53 / 100 + switch_length - 6 * arrow_width, 10, 0, 23, '',
                         '')

        self.create_line(self.width * 1 / 10, self.height * 14 / 20,
                         self.width * 2 / 10, self.height * 14 / 20, 10, 0, 24, '', '')
        self.create_line(self.width * 2 / 10 + 8 * arrow_width, self.height * 14 / 20 - 7 * arrow_width,
                         self.width * 9 / 20, self.height * 14 / 20 - 7 * arrow_width, 10, 0, 25, '', '')
        self.create_line(self.width * 2 / 10 + 8 * arrow_width, self.height * 14 / 20 + 7 * arrow_width,
                         self.width * 9 / 20, self.height * 14 / 20 + 7 * arrow_width, 10, 0, 26, '', '')
        self.create_line(self.width * 9 / 20 + 8 * arrow_width, self.height * 14 / 20,
                         self.width * 7 / 10, self.height * 14 / 20, 10, 0, 27, '', '')

        self.create_line(self.width * 7 / 10, self.height * 14 / 20,
                         self.width * 9 / 10, self.height * 14 / 20, 10, 0, 28, '', (7, 3))
        self.create_line(self.width * -9 / 100, self.height * 18 / 20,
                         self.width * 9 / 10, self.height * 18 / 20, 10, 0, 29, '', (7, 3))

        # oval
        self.proc_canvas.create_oval(self.width * 2 / 5 - arrow_width, self.height * 2 / 10,
                                     self.width * 2 / 5 + arrow_width, self.height * 2 / 10 + 2 * arrow_width,
                                     tags='frame')

        self.proc_canvas.create_oval(self.width * 2 / 10, self.height * 8 / 20 - arrow_width,
                                     self.width * 2 / 10 + 2 * arrow_width, self.height * 8 / 20 + arrow_width,
                                     tags='frame')
        self.proc_canvas.create_oval(self.width * 9 / 20 + 6 * arrow_width, self.height * 8 / 20 - arrow_width,
                                     self.width * 9 / 20 + 8 * arrow_width, self.height * 8 / 20 + arrow_width,
                                     tags='frame')

        self.proc_canvas.create_oval(self.width * 2 / 10, self.height * 14 / 20 - arrow_width,
                                     self.width * 2 / 10 + 2 * arrow_width, self.height * 14 / 20 + arrow_width,
                                     tags='frame')
        self.proc_canvas.create_oval(self.width * 9 / 20 + 6 * arrow_width, self.height * 14 / 20 - arrow_width,
                                     self.width * 9 / 20 + 8 * arrow_width, self.height * 14 / 20 + arrow_width,
                                     tags='frame')

        self.proc_canvas.create_oval(self.width * 1 / 10 - arrow_width,
                                     self.height * 53 / 100 + switch_length + 2 * arrow_width,
                                     self.width * 1 / 10 + arrow_width, self.height * 53 / 100 + switch_length,
                                     tags='frame')
        self.proc_canvas.create_oval(self.width * 7 / 10 - arrow_width, self.height * 53 / 100,
                                     self.width * 7 / 10 + arrow_width, self.height * 53 / 100 + 2 * arrow_width,
                                     tags='frame')

        # switch
        self.create_switch(0, self.switch_length, 325, self.width * 2 / 10 + 2 * arrow_width, self.height * 8 / 20,
                           arrow_width)
        self.create_switch(1, self.switch_length, 325, self.width * 2 / 10 + 2 * arrow_width, self.height * 14 / 20,
                           arrow_width)
        self.create_switch(2, self.switch_length, 55, self.width * 2 / 5, self.height * 2 / 10 + 2 * arrow_width,
                           arrow_width)
        self.create_switch(3, self.switch_length, 305, self.width * 1 / 10, self.height * 53 / 100 + switch_length,
                           arrow_width)
        self.create_switch(4, self.switch_length, 215, self.width * 9 / 20 + 6 * arrow_width, self.height * 8 / 20,
                           arrow_width)
        self.create_switch(5, self.switch_length, 215, self.width * 9 / 20 + 6 * arrow_width, self.height * 14 / 20,
                           arrow_width)
        self.create_switch(6, self.switch_length, 55, self.width * 7 / 10, self.height * 53 / 100 + 2 * arrow_width,
                           arrow_width)

        # move construct
        self.move_obj('frame', self.width * 9 / 100, self.height * 13 / 100)

        # save entry/exit
        entry_point = self.proc_canvas.coords(self.lines[0][0])
        self.entry_width = entry_point
        exit_point = self.proc_canvas.coords(self.lines[29][0])
        self.exit_height = exit_point[1] - (self.height * 6 / 11)
        # text
        nop_text_coords = self.proc_canvas.coords(self.lines[17][len(self.lines[17]) - 1])
        self.proc_canvas.create_text(nop_text_coords[2], nop_text_coords[3],
                                     anchor=Tk.W,
                                     text='NOP', font=('Helvetica', self.font_size))
        self.create_switch_text(0, 'A = ', 0, -3 * arrow_width)
        self.create_switch_text(1, 'B = ', 0, -3 * arrow_width)
        self.create_switch_text(2, 't2 = ', -4 * arrow_width, 0)
        self.create_switch_text(3, 't3 = ', -4 * arrow_width, 0)
        self.create_switch_text(4, 't4 = ', 5 * arrow_width, -3 * arrow_width)
        self.create_switch_text(5, 't5 = ', 5 * arrow_width, -3 * arrow_width)
        self.create_switch_text(6, 't3 = ', 12 * arrow_width, 4 * arrow_width)

    def create_line(self, start_width, start_height, end_width, end_height, seg_len_w, seg_len_h, index, arrow, dash):
        i = 0
        j = 0
        while abs(i + seg_len_w) <= end_width - start_width and abs(j + seg_len_h) <= end_height - start_height:
            self.lines[index].append(self.proc_canvas.create_line(start_width + i, start_height + j,
                                                                  start_width + (i + seg_len_w),
                                                                  start_height + (j + seg_len_h),
                                                                  width=self.arrow_width, tags='frame', dash=dash))
            i += seg_len_w
            j += seg_len_h
        self.lines[index].append(self.proc_canvas.create_line(start_width + i, start_height + j, end_width, end_height,
                                                              width=self.arrow_width, tags='frame', arrow=arrow,
                                                              dash=dash))

    def create_switch_text(self, nr, text, off_x, off_y):
        coords = self.proc_canvas.coords(self.switches[nr])
        self.proc_canvas.create_text(coords[0] + off_x, coords[1] + off_y, anchor=Tk.SE,
                                     text=text, font=('Helvetica', self.font_size))
        self.switch_text[nr] = self.proc_canvas.create_text(coords[0] + off_x, coords[1] + off_y, anchor=Tk.SW,
                                                            text='0', font=('Helvetica', self.font_size))

    def create_switch(self, nr, length, angle, center_x, center_y, arrow_width):
        end_x = center_x + length * math.cos(math.radians(angle))
        end_y = center_y + length * math.sin(math.radians(angle))
        self.switches[nr] = self.proc_canvas.create_line(center_x, center_y, end_x, end_y, width=arrow_width,
                                                         tags='frame')

    def rotate_switch(self, nr, length, target_angle, op, speed, quadrant):
        current = self.proc_canvas.coords(self.switches[nr])
        current_acos = math.degrees(math.acos((current[2] - current[0]) / length))
        current_asin = math.degrees(math.asin((current[3] - current[1]) / length))
        if current_asin < 0:
            current_angle = 360 - current_acos
        else:
            current_angle = current_acos
        new_angle = current_angle + speed
        end_x = current[0] + length * math.cos(math.radians(new_angle))
        end_y = current[1] + length * math.sin(math.radians(new_angle))
        self.proc_canvas.coords(self.switches[nr], current[0], current[1], end_x, end_y)
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
            self.switch_states[nr] = self.target_states[nr]
            self.proc_canvas.itemconfigure(self.switch_text[nr], text='%d' % self.target_states[nr])

    def next_line(self):
        reverse = False
        if self.current_line == 0:
            if self.switch_states[2] == 1:
                self.current_line = 1
            else:
                self.current_line = 2
            self.proc_canvas.itemconfigure(self.switches[2], fill=self.cable_color)
        elif self.current_line == 1:
            reverse = True
            self.current_line = 18
        elif self.current_line == 2:
            self.current_line = 17
        elif self.current_line == 3:
            if self.switch_states[0] == self.switch_states[4] or self.switch_states[3] == 0:
                self.current_line = 19
            else:
                self.current_line = 30
        elif self.current_line == 4:
            self.current_line = 24
        elif self.current_line == 5:
            reverse = True
            self.current_line = 23
        elif self.current_line == 6:
            self.current_line = 7
            self.proc_canvas.itemconfigure(self.switches[6], fill=self.cable_color)
        elif self.current_line == 7:
            self.current_line = 28
        elif self.current_line == 8:
            reverse = True
            self.current_line = 29
        elif self.current_line == 9:
            self.current_line = 20
        elif self.current_line == 10:
            self.current_line = 21
        elif self.current_line == 11:
            if self.switch_states[4] == 0:
                self.current_line = 22
                self.proc_canvas.itemconfigure(self.switches[4], fill=self.cable_color)
            else:
                self.current_line = 0
                self.flow_done.set(1)
        elif self.current_line == 12:
            if self.switch_states[4] == 1:
                self.current_line = 22
                self.proc_canvas.itemconfigure(self.switches[4], fill=self.cable_color)
            else:
                self.current_line = 0
                self.flow_done.set(1)
        elif self.current_line == 13:
            self.current_line = 25
        elif self.current_line == 14:
            self.current_line = 26
        elif self.current_line == 15:
            if self.switch_states[5] == 0:
                self.current_line = 27
                self.proc_canvas.itemconfigure(self.switches[5], fill=self.cable_color)
            else:
                self.current_line = 0
                self.flow_done.set(1)
        elif self.current_line == 16:
            if self.switch_states[5] == 1:
                self.current_line = 27
                self.proc_canvas.itemconfigure(self.switches[5], fill=self.cable_color)
            else:
                self.current_line = 0
                self.flow_done.set(1)
        elif self.current_line == 17:
            self.switch_done.set(1)
        elif self.current_line == 18:
            self.current_line = 3
        elif self.current_line == 19:
            if self.switch_states[0] == 0:
                reverse = True
                self.current_line = 9
            else:
                self.current_line = 10
            self.proc_canvas.itemconfigure(self.switches[0], fill=self.cable_color)
        elif self.current_line == 20:
            self.current_line = 11
        elif self.current_line == 21:
            self.current_line = 12
        elif self.current_line == 22:
            if self.switch_states[6] == 1:
                self.current_line = 31
            else:
                self.current_line = 5
        elif self.current_line == 23:
            self.current_line = 4
            self.proc_canvas.itemconfigure(self.switches[3], fill=self.cable_color)
        elif self.current_line == 24:
            if self.switch_states[1] == 0:
                reverse = True
                self.current_line = 13
            else:
                self.current_line = 14
            self.proc_canvas.itemconfigure(self.switches[1], fill=self.cable_color)
        elif self.current_line == 25:
            self.current_line = 15
        elif self.current_line == 26:
            self.current_line = 16
        elif self.current_line == 27:
            self.current_line = 28
        elif self.current_line == 28:
            self.current_line = 8
        elif self.current_line == 29:
            self.current_line = 0
            self.flow_done.set(1)
        elif self.current_line == 30:
            self.current_line = 4
            self.proc_canvas.itemconfigure(self.switches[3], fill=self.cable_color)
        elif self.current_line == 31:
            self.current_line = 6

        if reverse:
            self.iterator = iter(reversed(self.lines[self.current_line]))
        else:
            self.iterator = iter(self.lines[self.current_line])

    def animate_flow(self):
        try:
            self.proc_canvas.itemconfigure(next(self.iterator), fill=self.cable_color)
            self.master.after(20, self.animate_flow)
        except StopIteration:
            self.next_line()
            if self.flow_done.get() == 0:
                self.master.after(20, self.animate_flow)

    def animate_switch(self):
        if self.switch_states[0] < self.target_states[0]:
            self.animation_done = False
            self.rotate_switch(0, self.switch_length, 25, operator.gt, 1, 1)
        elif self.switch_states[0] > self.target_states[0]:
            self.animation_done = False
            self.rotate_switch(0, self.switch_length, -35, operator.lt, -1, 4)

        if self.switch_states[1] < self.target_states[1]:
            self.animation_done = False
            self.rotate_switch(1, self.switch_length, 25, operator.gt, 1, 1)
        elif self.switch_states[1] > self.target_states[1]:
            self.animation_done = False
            self.rotate_switch(1, self.switch_length, -35, operator.lt, -1, 4)

        if self.switch_states[2] < self.target_states[2]:
            self.animation_done = False
            self.rotate_switch(2, self.switch_length, 60, operator.lt, 1, 2)
        elif self.switch_states[2] > self.target_states[2]:
            self.animation_done = False
            self.rotate_switch(2, self.switch_length, 60, operator.lt, -1, 1)

        if self.switch_states[3] < self.target_states[3]:
            self.animation_done = False
            self.rotate_switch(3, self.switch_length, -88, operator.lt, -1, 4)
        elif self.switch_states[3] > self.target_states[3]:
            self.animation_done = False
            self.rotate_switch(3, self.switch_length, -55, operator.gt, 1, 4)

        if self.switch_states[4] < self.target_states[4]:
            self.animation_done = False
            self.rotate_switch(4, self.switch_length, 25, operator.gt, -1, 2)
        elif self.switch_states[4] > self.target_states[4]:
            self.animation_done = False
            self.rotate_switch(4, self.switch_length, -25, operator.lt, 1, 3)

        if self.switch_states[5] < self.target_states[5]:
            self.animation_done = False
            self.rotate_switch(5, self.switch_length, 25, operator.gt, -1, 2)
        elif self.switch_states[5] > self.target_states[5]:
            self.animation_done = False
            self.rotate_switch(5, self.switch_length, -25, operator.lt, 1, 3)

        if self.switch_states[6] < self.target_states[6]:
            self.animation_done = False
            self.rotate_switch(6, self.switch_length, 89, operator.gt, 1, 1)
        elif self.switch_states[6] > self.target_states[6]:
            self.animation_done = False
            self.rotate_switch(6, self.switch_length, 55, operator.lt, -1, 1)

        if not self.animation_done:
            self.animation_done = True
            self.master.after(10, self.animate_switch)
        else:
            self.switch_done.set(1)

    def move_obj(self, tag, x, y):
        objects = self.proc_canvas.find_withtag(tag)
        for obj in objects:
            current = self.proc_canvas.coords(obj)
            self.proc_canvas.coords(obj, current[0] + x, current[1] - y, current[2] + x, current[3] - y)
