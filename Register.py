import Tkinter as Tk


class Register(object):
    def __init__(self, master, width, height, border, entry_height, arrow_width):
        self.height = height * 5 / 17
        self.width = width * 3 / 18
        self.master = master
        self.arrow_width = arrow_width
        self.register_canvas = Tk.Canvas(master, bg="white", width=self.width, height=self.height, bd=border,
                                         highlightthickness=border)
        self.register_canvas.grid(row=11, column=3, rowspan=5, columnspan=3)

        self.lines = [[] for i in range(3)]

        self.a_text = self.register_canvas.create_text(self.width * 2 / 5, self.height * 2 / 16,
                                                  font=('Helvetica', self.height / 12), text='A = 0')
        self.b_text = self.register_canvas.create_text(self.width * 2 / 5, self.height * 7 / 16,
                                                   font=('Helvetica', self.height / 12), text='B = 0')
        a_coords = self.register_canvas.coords(self.a_text)
        b_coords = self.register_canvas.coords(self.b_text)
        self.A_box = self.register_canvas.create_rectangle(a_coords[0] - self.width / 4,
                                                           a_coords[1] - self.height / 10,
                                                           a_coords[0] + self.width / 4,
                                                           a_coords[1] + self.height / 10)
        self.B_box = self.register_canvas.create_rectangle(b_coords[0] - self.width / 4,
                                                           b_coords[1] - self.height / 10,
                                                           b_coords[0] + self.width / 4,
                                                           b_coords[1] + self.height / 10)

        self.a_box_coords = self.register_canvas.coords(self.A_box)
        self.b_box_coords = self.register_canvas.coords(self.B_box)

        self.create_line(self.width * 5 / 6, entry_height, self.width, entry_height,10,0,0,'',(7,3))
        self.create_line(self.width * 5 / 6, a_coords[1], self.width * 5 / 6, entry_height,0,10,1,'',(7,3))
        self.create_line(self.a_box_coords[2], a_coords[1],self.width * 5 / 6, a_coords[1],10,0,2,'',(7,3))

        self.current_line = 0
        self.iterator = iter(self.lines[self.current_line])

        self.pr_flag_color = 0xf66
        self.box_color = 0xfff
        self.cable_color = 'red'
        self.direction = 'FADE'
        self.pr_flag = self.register_canvas.create_text(self.a_box_coords[0], (self.a_box_coords[1] + self.a_box_coords[3]) / 2,
                                                   font=('Helvetica', self.height / 20), text='Pr', anchor=Tk.E)
        pr_tuple = self.register_canvas.bbox(self.pr_flag)
        self.register_canvas.coords(self.pr_flag,self.a_box_coords[0] - (pr_tuple[2] - pr_tuple[0]) / 2, (self.a_box_coords[1] + self.a_box_coords[3]) / 2)
        pr_tuple = self.register_canvas.bbox(self.pr_flag)
        self.pr_box = self.register_canvas.create_polygon(pr_tuple[0], pr_tuple[1] - ((pr_tuple[3] - pr_tuple[1]) / 2),
                                            pr_tuple[2] + ((pr_tuple[2] - pr_tuple[0]) / 2),
                                            pr_tuple[1] + ((pr_tuple[3] - pr_tuple[1]) / 2),
                                            pr_tuple[0], pr_tuple[3] + ((pr_tuple[3] - pr_tuple[1]) / 2), fill='#' + str(hex(self.pr_flag_color))[2:5])

        self.current_box = self.A_box
        self.flag_toggle_done = Tk.BooleanVar(0)
        self.flag_move_done = Tk.BooleanVar(0)
        self.color_blink_done = Tk.BooleanVar(0)
        self.flow_done = Tk.BooleanVar(0)
        self.pr_flag_state = 0
        self.pr_flag_target = None
        self.A_state = 0
        self.B_state = 0
        self.register_canvas.tag_raise(self.pr_flag)
        self.register_canvas.tag_raise(self.a_text)
        self.register_canvas.tag_raise(self.b_text)

    def set_register(self,register,value):
        if register == 'A':
            self.current_box = self.A_box
            self.register_canvas.itemconfigure(self.a_text,text='A = %d' % value)
            self.A_state = value
        elif register == 'B':
            self.current_box = self.B_box
            self.register_canvas.itemconfigure(self.b_text,text='B = %d' % value)
            self.B_state = value
        self.toggle_blink()

    def toggle_blink(self):
        self.direction = 'SOLIDIFY'
        self.box_color = 0xfff
        self.color_blink_done.set(0)
        self.animate_color_blink()
        self.master.wait_variable(self.color_blink_done)

    def set_flag(self,target):
        if self.pr_flag_state != target:
            self.direction = 'FADE'
            self.pr_flag_target = target
            self.flag_toggle_done.set(0)
            self.flag_move_done.set(0)
            self.animate_flag()

    def set_flow(self, color):
        self.cable_color = color
        self.flow_done.set(0)
        self.animate_flow()
        if self.flow_done.get() == 0:
            self.master.wait_variable(self.flow_done)

    def animate_flag(self):
        self.flag_color_toggle()
        if self.flag_toggle_done.get() == 0:
            self.master.wait_variable(self.flag_toggle_done)
        self.move_flag()
        if self.flag_move_done.get() == 0:
            self.master.wait_variable(self.flag_move_done)
        self.flag_toggle_done.set(0)
        self.flag_color_toggle()
        if self.flag_toggle_done.get() == 0:
            self.master.wait_variable(self.flag_toggle_done)

    def move_flag(self):
        current_pos_text = self.register_canvas.coords(self.pr_flag)
        current_pos_box = self.register_canvas.coords(self.pr_box)
        if self.pr_flag_state < self.pr_flag_target and current_pos_text[1] < (self.b_box_coords[1] + self.b_box_coords[3]) / 2:
            self.register_canvas.coords(self.pr_box,current_pos_box[0],current_pos_box[1] + 1,current_pos_box[2],current_pos_box[3] + 1,current_pos_box[4],current_pos_box[5] + 1)
            self.register_canvas.coords(self.pr_flag,current_pos_text[0],current_pos_text[1] + 1)
            self.master.after(20,self.move_flag)
        elif self.pr_flag_state > self.pr_flag_target and current_pos_text[1] > (self.a_box_coords[1] + self.a_box_coords[3]) / 2:
            self.register_canvas.coords(self.pr_box,current_pos_box[0],current_pos_box[1] - 1,current_pos_box[2],current_pos_box[3] - 1,current_pos_box[4],current_pos_box[5] - 1)
            self.register_canvas.coords(self.pr_flag,current_pos_text[0],current_pos_text[1] - 1)
            self.master.after(20,self.move_flag)
        else:
            self.pr_flag_state = self.pr_flag_target
            self.flag_move_done.set(1)

    def animate_color_blink(self):
        color = '#' + str(hex(self.box_color))[2:5]
        self.register_canvas.itemconfigure(self.current_box, fill=color)
        if self.direction == 'SOLIDIFY':
            self.box_color -= 0x101
            if self.box_color <= 0x9f9:
                self.direction = 'FADE'
            self.master.after(30, self.animate_color_blink)

        elif self.direction == 'FADE':
            self.box_color += 0x101
            if self.box_color > 0xfff:
                self.color_blink_done.set(1)
            else:
                self.master.after(30, self.animate_color_blink)

    def flag_color_toggle(self):
        if self.direction == 'SOLIDIFY':
            self.pr_flag_color -= 0x011
            if self.pr_flag_color <= 0xf66:
                self.flag_toggle_done.set(1)
                self.direction = 'FADE'
            else:
                self.master.after(30, self.flag_color_toggle)
        elif self.direction == 'FADE':
            self.pr_flag_color += 0x011
            if self.pr_flag_color > 0xfbb:
                self.flag_toggle_done.set(1)
                self.direction = 'SOLIDIFY'
            else:
                self.master.after(30, self.flag_color_toggle)
        color = '#' + str(hex(self.pr_flag_color))[2:5]
        self.register_canvas.itemconfigure(self.pr_box, fill=color)

    def create_line(self, start_width, start_height, end_width, end_height, seg_len_w, seg_len_h, index, arrow, dash):
        i = 0
        j = 0
        while abs(i + seg_len_w) <= end_width - start_width and abs(j + seg_len_h) <= end_height - start_height:
            self.lines[index].append(self.register_canvas.create_line(start_width + i, start_height + j,
                                                                  start_width + (i + seg_len_w),
                                                                  start_height + (j + seg_len_h),
                                                                  width=self.arrow_width, tags='frame', dash=dash))
            i += seg_len_w
            j += seg_len_h
        self.lines[index].append(self.register_canvas.create_line(start_width + i, start_height + j, end_width, end_height,
                                                              width=self.arrow_width, tags='frame', arrow=arrow,
                                                              dash=dash))
    def animate_flow(self):
        try:
            self.register_canvas.itemconfigure(next(self.iterator), fill=self.cable_color)
            self.master.after(20, self.animate_flow)
        except StopIteration:
            self.next_line()
            if self.flow_done.get() == 0:
                self.master.after(20, self.animate_flow)

    def next_line(self):
        if self.current_line == 0:
            self.current_line = 1
        elif self.current_line == 1:
            self.current_line = 2
        elif self.current_line == 2:
            self.current_line = 0
            self.flow_done.set(1)
        self.iterator = iter(reversed(self.lines[self.current_line]))