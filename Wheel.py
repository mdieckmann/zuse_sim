import Tkinter as Tk
import operator


class Wheel(object):
    def __init__(self, master, width, height, border, arrow_width):
        self.height = height * 13 / 17
        self.width = width * 4 / 18
        self.master = master
        self.arrow_width=arrow_width
        self.font_size = 6
        self.fs_data_up = [self.font_size * 3]
        self.fs_data_down = [self.font_size * 5]

        self.wheel_canvas = Tk.Canvas(master, bg="white", width=self.width, height=self.height, bd=border,
                                      highlightthickness=border)
        self.wheel_canvas.grid(row=2, column=13, rowspan=13, columnspan=4)

        self.wheel_canvas.create_polygon(self.width / 12, self.height * 15 / 32,
                                         self.width / 12, self.height * 17 / 32,
                                         self.width / 6, self.height / 2, fill="White", outline="Black")

        self.lines = [[] for i in range(3)]
        self.current_line = 0
        self.iterator = iter(self.lines[self.current_line])

        self.create_line(2 * arrow_width, self.height / 2, self.width / 12, self.height / 2, 10, 0, 0)
        self.create_line(2 * arrow_width, self.height / 8, 2 * arrow_width, self.height / 2, 0, 10, 1)
        self.create_line(0, self.height / 8, 2 * arrow_width, self.height / 8, 10, 0, 2)

        exit_point = self.wheel_canvas.coords(self.lines[2][0])
        self.exit_height = exit_point[1]

        # ringbuffer[8] is active, ringbuffer[7] is enlargen, ringbuffer[16] is delete, ringbuffer[0] is create
        self.ringbuffer_box = [None] * 15
        self.ringbuffer_data = [None] * 15
        self.command_sequence = []
        self.command_sequence_size = 0
        self.command_sequence_ptr = 0
        self.ringbuffer_ptr = 7
        self.shrunk = False
        self.enlarged = False
        self.target = 0
        self.cable_color = 'red'
        self.wheel_done = Tk.BooleanVar()
        self.flow_done = Tk.BooleanVar()

    def init(self,command_sequence):
        self.command_sequence = command_sequence
        self.command_sequence_size = len(self.command_sequence)
        self.init_ringbuffer()

    def init_ringbuffer(self):
        if not self.command_sequence_ptr < self.command_sequence_size:
            print "NO DATA FOUND"
            return -1
        self.ringbuffer_box[7] = self.wheel_canvas.create_rectangle(self.width / 6, self.height * 9 / 22,
                                                                    self.width * 5 / 6, self.height * 13 / 22,
                                                                    tags='MEM')
        self.ringbuffer_data[7] = self.wheel_canvas.create_text(self.width / 2, self.height / 2,
                                                                text=self.command_sequence[self.command_sequence_ptr],
                                                                tags='MEM',
                                                                font=('Helvetica', self.fs_data_down[0]))

        self.command_sequence_ptr += 1
        for i in range(6, 0, -1):
            if not self.command_sequence_ptr < self.command_sequence_size:
                width = 0
                text = ''
            else:
                width = 1
                text = self.command_sequence[self.command_sequence_ptr]
            self.ringbuffer_box[i] = self.wheel_canvas.create_rectangle(self.width * 3 / 12,
                                                                        self.height * (2 * i - 5) / 22,
                                                                        self.width * 9 / 12,
                                                                        self.height * (2 * i - 3) / 22,
                                                                        tags='MEM', width = width)
            self.ringbuffer_data[i] = self.wheel_canvas.create_text(self.width / 2, self.height * (2 * i - 4) / 22,
                                                                    text=text, tags='MEM',
                                                                    font=('Helvetica', self.fs_data_up[0]))
            self.command_sequence_ptr += 1

        for i in range(14, 7, -1):
            self.ringbuffer_box[i] = self.wheel_canvas.create_rectangle(self.width * 3 / 12,
                                                                        self.height * (2 * i - 3) / 22,
                                                                        self.width * 9 / 12,
                                                                        self.height * (2 * i - 1) / 22,
                                                                        tags='MEM', width=0)
            self.ringbuffer_data[i] = self.wheel_canvas.create_text(self.width / 2, self.height * (2 * i + 1) / 22,
                                                                    text='', tags='MEM',
                                                                    font=('Helvetica', self.fs_data_up[0]))
            self.command_sequence_ptr += 1

        self.command_sequence_ptr = 0

    def next_command(self):
        self.target += 1
        self.wheel_done.set(0)
        self.animate_wheel()
        if self.wheel_done.get() == 0:
            self.master.wait_variable(self.wheel_done)

    def set_flow(self, color):
        self.cable_color = color
        self.flow_done.set(0)
        self.animate_flow()
        if self.flow_done.get() == 0:
            self.master.wait_variable(self.flow_done)

    def animate_wheel(self):
        if self.command_sequence_ptr < self.target:
            next_cell = self.cycle(self.ringbuffer_ptr, (self.ringbuffer_ptr - 1) % len(self.ringbuffer_box))

            if (next_cell[1] + next_cell[3]) / 2 < self.height / 2:
                self.master.after(10, self.animate_wheel)
            else:
                self.reset_animation()
                # reset vars, delete/insert
                self.master.after(50, self.animate_wheel)
        else:
            self.wheel_done.set(1)

    def animate_flow(self):
        try:
            self.wheel_canvas.itemconfigure(next(self.iterator), fill=self.cable_color)
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

    def reset_animation(self):
        self.fs_data_up[0] = self.font_size * 3
        self.fs_data_down[0] = self.font_size * 5
        self.shrunk = False
        self.enlarged = False
        self.add_cell((self.ringbuffer_ptr + 8) % len(self.ringbuffer_box), self.command_sequence_ptr + 7)
        self.delete_cell((self.ringbuffer_ptr + 7) % len(self.ringbuffer_box))
        self.ringbuffer_ptr = (self.ringbuffer_ptr - 1) % len(self.ringbuffer_box)
        self.command_sequence_ptr += 1

    def delete_cell(self, ring_ptr):
        self.wheel_canvas.delete(self.ringbuffer_box[ring_ptr])
        self.wheel_canvas.delete(self.ringbuffer_data[ring_ptr])

    def add_cell(self, ring_ptr, cmd_ptr):
        if cmd_ptr < 0 or cmd_ptr >= self.command_sequence_size:
            width = 0
            data = ''
        else:
            width = 1
            data = self.command_sequence[cmd_ptr]
        next_cell = self.wheel_canvas.coords(self.ringbuffer_box[(ring_ptr + 1) % len(self.ringbuffer_box)])
        h1 = self.height * -3 / 22
        h2 = next_cell[1]
        self.ringbuffer_box[ring_ptr] = self.wheel_canvas.create_rectangle(self.width * 3 / 12, h1,
                                                                           self.width * 9 / 12, h2,
                                                                           tags='MEM', width=width)
        self.ringbuffer_data[ring_ptr] = self.wheel_canvas.create_text(self.width / 2, (h2 + h1) / 2,
                                                                       text=data, tags='MEM',
                                                                       font=('Helvetica', self.fs_data_up[0]))

    def resize_text(self, text, target, direction, up, down, x0, x1, y0, y1):
        if direction > 0 and up[0] < target:
            up[0] += direction
            self.wheel_canvas.itemconfigure(text, font=('Helvetica', int(up[0])))
        if direction < 0 and down[0] > target:
            down[0] += direction
            self.wheel_canvas.itemconfigure(text, font=('Helvetica', int(down[0])))
        self.wheel_canvas.coords(text, (x0 + x1) / 2, (y0 + y1) / 2)

    def cycle(self, ptr, ptr_next):
        speed = 1
        self.wheel_canvas.move('MEM', 0, speed)
        if not self.shrunk:
            self.shrunk = self.resize_rectangle((-1 * speed), self.width * 6 / 12, self.height * 2 / 22,
                                                operator.gt, ptr)
            current_pos = self.wheel_canvas.coords(self.ringbuffer_box[ptr])
            self.resize_text(self.ringbuffer_data[ptr],
                             self.font_size * 3, -1,
                             self.fs_data_up,
                             self.fs_data_down,
                             current_pos[0], current_pos[2],
                             current_pos[1], current_pos[3])
        if not self.enlarged:
            self.enlarged = self.resize_rectangle(speed, self.width * 4 / 6, self.height * 4 / 22,
                                                  operator.lt, ptr_next)
            current_pos = self.wheel_canvas.coords(self.ringbuffer_box[ptr_next])
            self.resize_text(self.ringbuffer_data[ptr_next],
                             self.font_size * 5, 1,
                             self.fs_data_up,
                             self.fs_data_down,
                             current_pos[0], current_pos[2],
                             current_pos[1], current_pos[3])
        return self.wheel_canvas.coords(self.ringbuffer_box[ptr_next % len(self.ringbuffer_box)])

    # smaller: resize_rectangle(-1,target_x,target_y, >, ptr, DOWN
    # taller: resize_rectangle(1,target_x,target_y, <, ptr, UP
    def resize_rectangle(self, amount, target_x, target_y, op, ptr):
        current_pos = self.wheel_canvas.coords(self.ringbuffer_box[ptr])
        if op((current_pos[2] - current_pos[0]), target_x):
            self.wheel_canvas.coords(self.ringbuffer_box[ptr], current_pos[0] - (2 * amount), current_pos[1],
                                     current_pos[2] + (2 * amount), current_pos[3])

        current_pos = self.wheel_canvas.coords(self.ringbuffer_box[ptr])
        if op((current_pos[3] - current_pos[1]), target_y):
            self.wheel_canvas.coords(self.ringbuffer_box[ptr], current_pos[0], current_pos[1] - amount, current_pos[2],
                                     current_pos[3] + amount)
        current_pos = self.wheel_canvas.coords(self.ringbuffer_box[ptr])
        if op((current_pos[3] - current_pos[1]), target_y):
            self.wheel_canvas.coords(self.ringbuffer_box[ptr], current_pos[0], current_pos[1] - amount, current_pos[2],
                                     current_pos[3] + amount)

        self.wheel_canvas.move(self.ringbuffer_box[ptr], 0, abs(amount) * 2)

        if not op((current_pos[3] - current_pos[1]), target_y):
            next_box = self.wheel_canvas.coords(self.ringbuffer_box[(ptr + 1) % len(self.ringbuffer_box)])
            prev_box = self.wheel_canvas.coords(self.ringbuffer_box[(ptr - 1) % len(self.ringbuffer_box)])
            if amount > 0:
                self.wheel_canvas.coords(self.ringbuffer_box[ptr], self.width / 6, prev_box[3], self.width * 5 / 6,
                                         next_box[1])
            elif amount < 0:
                self.wheel_canvas.coords(self.ringbuffer_box[ptr], next_box[0], prev_box[3], next_box[2], next_box[1])
            return True
        return False

    def create_line(self, start_width, start_height, end_width, end_height, seg_len_w, seg_len_h, index):
        i = 0
        j = 0
        while abs(i + seg_len_w) <= end_width - start_width and abs(j + seg_len_h) <= end_height - start_height:
            self.lines[index].append(self.wheel_canvas.create_line(start_width + i, start_height + j,
                                                                   start_width + (i + seg_len_w),
                                                                   start_height + (j + seg_len_h), width=self.arrow_width))
            i += seg_len_w
            j += seg_len_h
        self.lines[index].append(
            self.wheel_canvas.create_line(start_width + i, start_height + j, end_width, end_height, width=self.arrow_width))
