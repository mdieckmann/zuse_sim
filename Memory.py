import Tkinter as Tk
import operator
import re


class Memory(object):
    def __init__(self, master, width, height, border):
        self.height = height * 15 / 17
        self.width = width * 2 / 18
        self.master = master
        self.font_size = 8
        self.fs_ix_up = [self.font_size]
        self.fs_ix_down = [self.font_size + (self.font_size / 2)]
        self.fs_data_up = [self.font_size * 3]
        self.fs_data_down = [self.font_size * 5]

        self.memory_canvas = Tk.Canvas(master, bg="white", width=self.width, height=self.height, bd=border,
                                       highlightthickness=border)
        self.memory_canvas.grid(row=1, column=1, rowspan=15, columnspan=2)

        self.memory_canvas.create_polygon(self.width / 12, self.height * 15 / 32,
                                          self.width / 12, self.height * 17 / 32,
                                          self.width / 6, self.height / 2, fill="White", outline="Black")

        self.memory_canvas.create_polygon(self.width * 11 / 12, self.height * 15 / 32,
                                          self.width * 11 / 12, self.height * 17 / 32,
                                          self.width * 5 / 6, self.height / 2, fill="White", outline="Black")

        # ringbuffer[8] is active, ringbuffer[7] is enlargen, ringbuffer[16] is delete, ringbuffer[0] is create
        self.ringbuffer_box = [None] * 19
        self.ringbuffer_index = [None] * 19
        self.ringbuffer_data = [None] * 19
        self.memory = []
        self.memory_ptr = 0
        self.ringbuffer_ptr = 9
        self.memory_size = 0
        self.shrunk = False
        self.enlarged = False
        self.target = 0
        self.color = None
        self.direction = None
        self.color_blink_done = Tk.BooleanVar()
        self.done = Tk.BooleanVar()

    def init(self, preset, command_sequence):
        self.additional_memory_size = len(preset)
        for command in command_sequence:
            if re.match('STORE [0-9]+', command) and int(command[6:]) > self.additional_memory_size:
                self.additional_memory_size = int(command[6:])
            elif re.match('LOAD [0-9]+', command) and int(command[5:]) > self.additional_memory_size:
                self.additional_memory_size = int(command[5:])
        self.init_memory(preset)
        self.init_ringbuffer()
        self.memory_canvas.tag_bind('BIND', '<ButtonPress-1>', self.flip_memory_cell)
        self.memory_canvas.bind_all('<ButtonPress-5>', self.scroll_down)
        self.memory_canvas.bind_all('<ButtonPress-4>', self.scroll_up)

    def init_memory(self, preset):
        for entry in preset:
            self.memory.append(int(entry))
        self.memory_size = len(self.memory)
        self.memory_ptr = self.memory_size / 2

    def init_additional_memory(self):
        i = self.memory_size - self.memory_ptr
        while self.memory_size < self.additional_memory_size + 1:
            if i < 9:
                width = 1
                index = 'x%d' % self.memory_size
                data = '0'
                next_cell = self.memory_canvas.coords(self.ringbuffer_box[(self.ringbuffer_ptr - i + 1) % len(self.ringbuffer_box)])
                if i == 8:
                    h1 = self.height * -3 / 30
                else:
                    prev_cell = self.memory_canvas.coords(self.ringbuffer_box[(self.ringbuffer_ptr - i - 1) % len(self.ringbuffer_box)])
                    h1 = prev_cell[3]
                h2 = next_cell[1]
                self.ringbuffer_box[self.ringbuffer_ptr - i] = self.memory_canvas.create_rectangle(self.width * 3 / 12, h1,
                                                                                                   self.width * 9 / 12, h2,
                                                                                                   tags='MEM', width=width)
                self.ringbuffer_index[self.ringbuffer_ptr - i] = self.memory_canvas.create_text(self.width * 9 / 12, h2,
                                                                                                anchor=Tk.SE, text=index, tags='MEM',
                                                                                                font=('Helvetica', self.fs_ix_up[0]))
                self.ringbuffer_data[self.ringbuffer_ptr - i] = self.memory_canvas.create_text(self.width / 2, (h2 + h1) / 2,
                                                                                               text=data, tags=('MEM','BIND'),
                                                                                               font=('Helvetica', self.fs_data_up[0]))
                i += 1
            self.memory.append(0)
            self.memory_size += 1

    def init_ringbuffer(self):
        if not self.memory_ptr < self.memory_size:
            print "NO DATA FOUND"
            return -1
        self.ringbuffer_box[9] = self.memory_canvas.create_rectangle(self.width / 6, self.height * 13 / 30,
                                                                     self.width * 5 / 6, self.height * 17 / 30,
                                                                     tags='MEM')
        self.ringbuffer_index[9] = self.memory_canvas.create_text(self.width * 5 / 6, self.height * 17 / 30,
                                                                  anchor=Tk.SE, text='x%d' % self.memory_ptr,
                                                                  tags='MEM',
                                                                  font=('Helvetica', self.fs_ix_down[0]))
        self.ringbuffer_data[9] = self.memory_canvas.create_text(self.width / 2, self.height / 2,
                                                                 text='%d' % self.memory[self.memory_ptr], tags=('MEM','BIND'),
                                                                 font=('Helvetica', self.fs_data_down[0]))

        self.memory_ptr += 1
        for i in range(8, 0, -1):
            if self.memory_ptr >= self.memory_size:
                width = 0
                text_ix = ''
                text_data = ''
                tags = 'MEM'
            else:
                width = 1
                text_ix = 'x%d' % self.memory_ptr
                text_data = '%d' % self.memory[self.memory_ptr]
                tags=('MEM','BIND')
            self.ringbuffer_box[i] = self.memory_canvas.create_rectangle(self.width * 3 / 12,
                                                                         self.height * (2 * i - 5) / 30,
                                                                         self.width * 9 / 12,
                                                                         self.height * (2 * i - 3) / 30,
                                                                         tags='MEM', width=width)
            self.ringbuffer_index[i] = self.memory_canvas.create_text(self.width * 9 / 12,
                                                                      self.height * (2 * i - 3) / 30,
                                                                      anchor=Tk.SE, text=text_ix,
                                                                      tags='MEM',
                                                                      font=('Helvetica', self.fs_ix_up[0]))
            self.ringbuffer_data[i] = self.memory_canvas.create_text(self.width / 2, self.height * (2 * i - 4) / 30,
                                                                     text=text_data,
                                                                     tags=tags,
                                                                     font=('Helvetica', self.fs_data_up[0]))
            self.memory_ptr += 1
        self.memory_ptr = 0
        print self.memory_size / 2
        for i in range(18, 9, -1):
            if (i-9) > self.memory_size / 2:
                width = 0
                text_ix = ''
                text_data = ''
                tags = 'MEM'
            else:
                width = 1
                text_ix = 'x%d' % self.memory_ptr
                text_data = '%d' % self.memory[self.memory_ptr]
                tags=('MEM','BIND')
                self.memory_ptr += 1

            self.ringbuffer_box[i] = self.memory_canvas.create_rectangle(self.width * 3 / 12,
                                                                         self.height * (2 * i - 3) / 30,
                                                                         self.width * 9 / 12,
                                                                         self.height * (2 * i - 1) / 30,
                                                                         tags='MEM', width=width)
            self.ringbuffer_index[i] = self.memory_canvas.create_text(self.width * 9 / 12,
                                                                      self.height * (2 * i - 1) / 30,
                                                                      anchor=Tk.SE, text=text_ix, tags='MEM',
                                                                      font=('Helvetica', self.fs_ix_up[0]))
            self.ringbuffer_data[i] = self.memory_canvas.create_text(self.width / 2, self.height * (2 * i - 2) / 30,
                                                                     text=text_data, tags=tags,
                                                                     font=('Helvetica', self.fs_data_up[0]))
        self.memory_ptr = self.memory_size / 2

    def set_target(self, target):
        self.target = target
        self.done.set(0)
        self.animate()
        if self.done.get() == 0:
            self.master.wait_variable(self.done)

    def set_current_cell(self, data):
        self.memory_canvas.itemconfigure(self.ringbuffer_data[self.ringbuffer_ptr], text=data)
        self.memory[self.memory_ptr] = int(data)
        self.toggle_blink()

    def toggle_blink(self):
        self.direction = 'SOLIDIFY'
        self.color = 0xfff
        self.color_blink_done.set(0)
        self.animate_color_blink()
        if self.color_blink_done.get() == 0:
            self.master.wait_variable(self.color_blink_done)

    def animate_color_blink(self):
        color = '#' + str(hex(self.color))[2:5]
        self.memory_canvas.itemconfigure(self.ringbuffer_box[self.ringbuffer_ptr], fill=color)
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

    def animate(self):
        if self.memory_ptr > self.target:
            next_cell = self.cycle('UP', self.ringbuffer_ptr, (self.ringbuffer_ptr + 1) % len(self.ringbuffer_box))
            if (next_cell[1] + next_cell[3]) / 2 > self.height / 2:
                self.master.after(1, self.animate)
            else:
                self.reset_animation('UP')
                # reset vars, delete/insert
                self.master.after(1, self.animate)
        elif self.memory_ptr < self.target:
            next_cell = self.cycle('DOWN', self.ringbuffer_ptr, (self.ringbuffer_ptr - 1) % len(self.ringbuffer_box))

            if (next_cell[1] + next_cell[3]) / 2 < self.height / 2:
                self.master.after(1, self.animate)
            else:
                self.reset_animation('DOWN')
                # reset vars, delete/insert
                self.master.after(1, self.animate)
        else:
            print 'DONE'
            self.done.set(1)

    def reset_animation(self, direction):
        self.fs_ix_up[0] = self.font_size
        self.fs_ix_down[0] = self.font_size + (self.font_size / 2)
        self.fs_data_up[0] = self.font_size * 3
        self.fs_data_down[0] = self.font_size * 5
        self.shrunk = False
        self.enlarged = False
        if direction == 'UP':
            self.add_cell((self.ringbuffer_ptr + 10) % len(self.ringbuffer_box), self.memory_ptr - 10, direction)
            self.delete_cell((self.ringbuffer_ptr + 11) % len(self.ringbuffer_box))
            self.ringbuffer_ptr = (self.ringbuffer_ptr + 1) % len(self.ringbuffer_box)
            self.memory_ptr -= 1
            # delete/insert
        elif direction == 'DOWN':
            self.add_cell((self.ringbuffer_ptr + 10) % len(self.ringbuffer_box), self.memory_ptr + 9, direction)
            self.delete_cell((self.ringbuffer_ptr + 9) % len(self.ringbuffer_box))
            self.ringbuffer_ptr = (self.ringbuffer_ptr - 1) % len(self.ringbuffer_box)
            self.memory_ptr += 1
            # delete/insert

    def delete_cell(self, ring_ptr):
        self.memory_canvas.delete(self.ringbuffer_box[ring_ptr])
        self.memory_canvas.delete(self.ringbuffer_index[ring_ptr])
        self.memory_canvas.delete(self.ringbuffer_data[ring_ptr])

    def add_cell(self, ring_ptr, mem_ptr, direction):
        if mem_ptr < 0 or mem_ptr >= self.memory_size:
            width = 0
            index = ''
            data = ''
        else:
            width = 1
            index = 'x%d' % mem_ptr
            data = '%d' % self.memory[mem_ptr]
        if direction == 'DOWN':
            next_cell = self.memory_canvas.coords(self.ringbuffer_box[(ring_ptr + 1) % len(self.ringbuffer_box)])
            h1 = self.height * -3 / 30
            h2 = next_cell[1]
        elif direction == 'UP':
            prev_cell = self.memory_canvas.coords(self.ringbuffer_box[(ring_ptr - 1) % len(self.ringbuffer_box)])
            h1 = prev_cell[3]
            h2 = self.height * 35 / 30
        self.ringbuffer_box[ring_ptr] = self.memory_canvas.create_rectangle(self.width * 3 / 12, h1,
                                                                            self.width * 9 / 12, h2,
                                                                            tags='MEM', width=width)
        self.ringbuffer_index[ring_ptr] = self.memory_canvas.create_text(self.width * 9 / 12, h2,
                                                                         anchor=Tk.SE, text=index, tags='MEM',
                                                                         font=('Helvetica', self.fs_ix_up[0]))
        self.ringbuffer_data[ring_ptr] = self.memory_canvas.create_text(self.width / 2, (h2 + h1) / 2,
                                                                        text=data, tags=('MEM','BIND'),
                                                                        font=('Helvetica', self.fs_data_up[0]))

    def resize_text(self, text, target, direction, up, down, x0, x1, y0, y1):
        if direction > 0 and up[0] < target:
            up[0] += direction
            self.memory_canvas.itemconfigure(text, font=('Helvetica', int(up[0])))
        if direction < 0 and down[0] > target:
            down[0] += direction
            self.memory_canvas.itemconfigure(text, font=('Helvetica', int(down[0])))
        self.memory_canvas.coords(text, (x0 + x1) / 2, (y0 + y1) / 2)

    def cycle(self, direction, ptr, ptr_next):
        speed = 1
        if direction == 'UP':
            self.memory_canvas.move('MEM', 0, (-1 * speed))
        elif direction == 'DOWN':
            self.memory_canvas.move('MEM', 0, speed)
        if not self.shrunk:
            self.shrunk = self.resize_rectangle((-1 * speed), self.width * 6 / 12, self.height * 2 / 30,
                                                operator.gt, ptr, direction)
            current_pos = self.memory_canvas.coords(self.ringbuffer_box[ptr])
            self.resize_text(self.ringbuffer_index[ptr],
                             self.font_size, -1,
                             self.fs_ix_up,
                             self.fs_ix_down,
                             current_pos[2], current_pos[2],
                             current_pos[3], current_pos[3])
            self.resize_text(self.ringbuffer_data[ptr],
                             self.font_size * 3, -3,
                             self.fs_data_up,
                             self.fs_data_down,
                             current_pos[0], current_pos[2],
                             current_pos[1], current_pos[3])
        if not self.enlarged:
            self.enlarged = self.resize_rectangle(speed, self.width * 4 / 6, self.height * 4 / 30,
                                                  operator.lt, ptr_next, direction)
            current_pos = self.memory_canvas.coords(self.ringbuffer_box[ptr_next])
            self.resize_text(self.ringbuffer_index[ptr_next],
                             self.font_size + (self.font_size / 2), 1,
                             self.fs_ix_up,
                             self.fs_ix_down,
                             current_pos[2], current_pos[2],
                             current_pos[3], current_pos[3])
            self.resize_text(self.ringbuffer_data[ptr_next],
                             self.font_size * 5, 3,
                             self.fs_data_up,
                             self.fs_data_down,
                             current_pos[0], current_pos[2],
                             current_pos[1], current_pos[3])
        return self.memory_canvas.coords(self.ringbuffer_box[ptr_next % len(self.ringbuffer_box)])

    # smaller: resize_rectangle(-1,target_x,target_y, >, ptr, DOWN
    # taller: resize_rectangle(1,target_x,target_y, <, ptr, UP
    def resize_rectangle(self, amount, target_x, target_y, op, ptr, direction):
        current_pos = self.memory_canvas.coords(self.ringbuffer_box[ptr])
        if op((current_pos[2] - current_pos[0]), target_x):
            self.memory_canvas.coords(self.ringbuffer_box[ptr], current_pos[0] - amount, current_pos[1],
                                      current_pos[2] + amount, current_pos[3])

        current_pos = self.memory_canvas.coords(self.ringbuffer_box[ptr])
        if op((current_pos[3] - current_pos[1]), target_y):
            self.memory_canvas.coords(self.ringbuffer_box[ptr], current_pos[0], current_pos[1] - amount, current_pos[2],
                                      current_pos[3] + amount)
        current_pos = self.memory_canvas.coords(self.ringbuffer_box[ptr])
        if op((current_pos[3] - current_pos[1]), target_y):
            self.memory_canvas.coords(self.ringbuffer_box[ptr], current_pos[0], current_pos[1] - amount, current_pos[2],
                                      current_pos[3] + amount)

        if direction == 'DOWN':
            self.memory_canvas.move(self.ringbuffer_box[ptr], 0, abs(amount) * 2)
        elif direction == 'UP':
            self.memory_canvas.move(self.ringbuffer_box[ptr], 0, abs(amount) * -2)

        if not op((current_pos[3] - current_pos[1]), target_y):
            next_box = self.memory_canvas.coords(self.ringbuffer_box[(ptr + 1) % len(self.ringbuffer_box)])
            prev_box = self.memory_canvas.coords(self.ringbuffer_box[(ptr - 1) % len(self.ringbuffer_box)])
            if amount > 0:
                self.memory_canvas.coords(self.ringbuffer_box[ptr], self.width / 6, prev_box[3], self.width * 5 / 6,
                                          next_box[1])
            elif amount < 0 and direction == 'DOWN':
                self.memory_canvas.coords(self.ringbuffer_box[ptr], next_box[0], prev_box[3], next_box[2], next_box[1])
            elif amount < 0 and direction == 'UP':
                self.memory_canvas.coords(self.ringbuffer_box[ptr], prev_box[0], prev_box[3], prev_box[2], next_box[1])
            return True
        return False

    def scroll_down(self,event):
        self.memory_canvas.unbind_all('<ButtonPress-4>')
        if self.memory_ptr > 0:
            target = self.memory_ptr - 1
            self.set_target(target)
        self.memory_canvas.bind_all('<ButtonPress-4>', self.scroll_up)

    def scroll_up(self,event):
        self.memory_canvas.unbind_all('<ButtonPress-5>')
        if self.memory_ptr < self.memory_size -1:
            target = self.memory_ptr + 1
            self.set_target(target)
        self.memory_canvas.bind_all('<ButtonPress-5>', self.scroll_down)

    def flip_memory_cell(self, event):

        if self.memory_canvas.itemcget(Tk.CURRENT,'text') == '0':
            text = '1'
        else:
            text = '0'
        self.memory_canvas.itemconfigure(Tk.CURRENT,text=text)
        id_current = self.memory_canvas.find_withtag(Tk.CURRENT)[0]
        id_selected = self.ringbuffer_data[self.ringbuffer_ptr]
        diff = self.ringbuffer_data.index(id_current) - self.ringbuffer_data.index(id_selected)
        self.memory[self.memory_ptr - diff] = int(text)
        print self.memory
